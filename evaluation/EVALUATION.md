# Evaluation Methodology

This document explains how the RAG assistant is evaluated, what each metric
means, and how correctness was judged — so results can be trusted and
reproduced.

## Test set

`evaluation/test_questions.json` contains 38 questions split into two types:

| Type | Count | Purpose |
|---|---|---|
| `answer` | 32 | Questions answerable from `data/researchpaper on ai.pdf`. Includes direct factual questions, paraphrased re-wordings of existing questions, and multi-point questions requiring several facts to be combined. |
| `refuse` | 6 | Questions that should NOT be answered from the documents — general-knowledge questions with no source in the ingested PDF, and two prompt-injection attempts designed to make the assistant break its own rules ("ignore your instructions...", "forget the system prompt..."). |

Each `answer` question includes an `expected_source` field (always
`researchpaper on ai.pdf` in the current test set) so retrieval can be
checked automatically, independent of whether the final generated text is
judged correct.

> **Scope note:** The test set was originally designed to include two
> cross-document questions (about BERT and RAG papers) to test
> multi-document retrieval. Those questions were removed because the
> corresponding PDFs are not part of this project's committed `data/`
> folder — including them produced misleading "retrieval miss" results
> for documents that were never meant to be ingested. As a result, this
> evaluation validates single-document retrieval and grounding only;
> multi-document retrieval accuracy has not been separately tested.

## Metrics

### 1. Retrieval hit-rate (automatic)
For every `answer` question, checks whether `expected_source` actually
appears in the `sources` returned by the pipeline. This measures the
retriever alone, isolated from the LLM's generation step — a correct-
looking answer built on the wrong retrieved chunk would still count as a
retrieval failure.

**Result: 32/32 — 100%**

### 2. Refuse accuracy (automatic)
For every `refuse` question, checks whether the generated answer matches
the fixed refusal string exactly
(`"I could not find this information in the uploaded documents."`). No
partial credit — either the system stayed grounded or it didn't. This is
the metric that specifically tests abstention and resistance to
prompt-injection attempts embedded in the user's question.

**Result: 6/6 — 100%**, including both prompt-injection attempts.

### 3. Answer accuracy (human-judged)
For every `answer` question, a human compares the generated answer
against `expected_answer` and marks it correct (`y`) or incorrect (`n`).

**Grading criteria used:** an answer is marked correct if it preserves
the same facts and meaning as `expected_answer`, even if phrased
differently, shortened, or expanded with additional (accurate) detail
from the same source document. An answer is marked incorrect if it omits
the specific fact being asked for, states something not supported by the
source document, mixes in content from an unrelated topic in the
document (e.g. describing NLP when asked about ML), or refuses when an
answer was actually available.

This step is manual because free-text answers can be correct while using
different wording than `expected_answer` — automated exact-match or
keyword scoring produces false negatives on legitimate paraphrases. A
possible future improvement is replacing this step with an LLM-as-judge
call, at the cost of losing some grading transparency.

**Result: 31/32 — 96.88%**

## Why three separate metrics instead of one accuracy number

A single "accuracy" score hides *which part* of the pipeline failed.
Splitting the score shows exactly where a problem sits:

- Low retrieval hit-rate + low answer accuracy → the retriever is the
  problem (wrong chunks reaching the LLM).
- High retrieval hit-rate + low answer accuracy → the retriever is fine,
  the LLM is generating poorly from good context.
- Low refuse accuracy → the grounding/abstention logic is not reliable,
  regardless of how good normal answers look.

## How to run

```bash
python ingest.py           # build/refresh the FAISS index from data/
python evaluation/evaluate.py
```

You will be prompted `(y/n)` only for `answer`-type questions, using the
grading criteria above. `refuse`-type questions are checked automatically
with no prompt.

## Output

- `evaluation/results.csv` / `results.json` — full per-question results
- `evaluation/evaluation_matrix.md` — summary table with all three metrics
  plus average response time

## Findings from this evaluation run

- One paraphrased question ("explain what ML does, in your own words")
  returned content mixing in NLP-specific details (audio capture, text
  conversion) instead of a clean ML answer, likely due to adjacent chunk
  retrieval — the ML and NLP sections sit close together in the source
  document. This was caught by the human-judged accuracy check and
  marked incorrect; it is the one item accounting for the 96.88% (rather
  than 100%) answer accuracy.
- All 6 refuse-case questions, including two direct prompt-injection
  attempts, were correctly declined after a system-prompt fix was added
  specifically instructing the model to treat the user's question as
  content to answer from, not as new instructions to follow.

## Known limitations

- Answer-accuracy grading is performed by the developer, not an
  independent reviewer or blind evaluator — it should be read as a
  self-reported quality check, not an unbiased benchmark.
- The test set covers single-document factual questions, paraphrases,
  refusal, and two prompt-injection attempts. It does not cover
  conflicting information between multiple documents, or malformed/
  corrupted PDF input handling.
- Refusal currently passes because the LLM follows the system prompt's
  instruction to decline off-topic or manipulative questions. The
  retrieval layer itself still returns a fallback set of chunks even
  when nothing meets the relevance threshold (see `retrieval_service.py`),
  so grounding is enforced by prompt instruction rather than guaranteed
  by code. This is disclosed as a planned improvement in the main
  README under "Future Improvements."