"""
evaluation/evaluate.py

Evaluation Script for RAG Pipeline.

Combines:
- Automatic checks (no human needed): retrieval hit-rate for answerable
  questions, and refusal-correctness for questions that should NOT be
  answered from the documents.
- Manual checks (human judgement): answer quality for answerable questions,
  since "is this phrased correctly" still needs a person to read it.
"""

import json
import csv
import os
import sys

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from rag import RAGPipeline


# Initialize RAG
rag = RAGPipeline()


# Load test questions
with open("evaluation/test_questions.json", "r", encoding="utf-8") as file:
    questions = json.load(file)


results = []

# Separate counters for each type of check
answer_correct = 0       # human-judged, answerable questions only
answer_total = 0

refuse_correct = 0        # auto-checked, refuse-case questions only
refuse_total = 0

retrieval_hits = 0        # auto-checked, answerable questions with a known expected source
retrieval_checked = 0

print("\n==============================")
print("      RAG Evaluation")
print("==============================\n")

for index, item in enumerate(questions, start=1):

    question = item["question"]
    expected = item.get("expected_answer")

    # Defaults to "answer" so old-style entries without this field still work
    expected_behavior = item.get("expected_behavior", "answer")
    expected_source = item.get("expected_source")

    print(f"\nQuestion {index}/{len(questions)}")
    print("-" * 60)
    print("Question:")
    print(question)
    print(f"Expected behavior: {expected_behavior}")

    if expected:
        print("\nExpected Answer:")
        print(expected)

    response = rag.ask(question)

    generated_answer = response["answer"]
    response_time = response["response_time"]
    sources = response["sources"]

    print("\nGenerated Answer:")
    print(generated_answer)

    print("\nSources:")
    print(sources)

    print(f"\nResponse Time: {response_time} sec")

    # --------------------------------------------------------
    # CASE 1: This question should be REFUSED (no answer in the docs)
    # Checked automatically — no human input needed.
    # --------------------------------------------------------
    if expected_behavior == "refuse":

        refuse_total += 1

        refused = "could not find this information" in generated_answer.lower()

        if refused:
            refuse_correct += 1

        print(f"\n[AUTO-CHECK] Correctly refused: {refused}")

        results.append({
            "Question": question,
            "Expected Behavior": "refuse",
            "Expected Answer": expected,
            "Generated Answer": generated_answer,
            "Response Time (sec)": response_time,
            "Sources": str(sources),
            "Retrieval Hit": None,
            "Refused Correctly": refused,
            "Result": "Correct" if refused else "Incorrect",
        })

        continue

    # --------------------------------------------------------
    # CASE 2: This question SHOULD be answered from the documents.
    # Retrieval hit-rate is checked automatically (if expected_source given).
    # Answer quality is still judged by a human.
    # --------------------------------------------------------
    retrieval_hit = None

    if expected_source:
        retrieval_checked += 1

        retrieved_sources = [s.get("source", "") for s in sources]
        retrieval_hit = any(expected_source in src for src in retrieved_sources)

        if retrieval_hit:
            retrieval_hits += 1

        print(f"\n[AUTO-CHECK] Expected source found in retrieved chunks: {retrieval_hit}")

    answer_total += 1

    evaluation = input("\nIs the generated answer correct? (y/n): ").strip().lower()

    is_correct = evaluation == "y"

    if is_correct:
        answer_correct += 1

    results.append({
        "Question": question,
        "Expected Behavior": "answer",
        "Expected Answer": expected,
        "Generated Answer": generated_answer,
        "Response Time (sec)": response_time,
        "Sources": str(sources),
        "Retrieval Hit": retrieval_hit,
        "Refused Correctly": None,
        "Result": "Correct" if is_correct else "Incorrect",
    })


# --------------------------------------------------------
# Calculate metrics (guard against divide-by-zero if a category is empty)
# --------------------------------------------------------
answer_accuracy = (answer_correct / answer_total * 100) if answer_total else 0.0
refuse_accuracy = (refuse_correct / refuse_total * 100) if refuse_total else 0.0
retrieval_hit_rate = (retrieval_hits / retrieval_checked * 100) if retrieval_checked else 0.0

response_times = [r["Response Time (sec)"] for r in results]
avg_response_time = sum(response_times) / len(response_times) if response_times else 0.0


print("\n====================================")
print("        Evaluation Summary")
print("====================================")
print(f"Answerable questions          : {answer_total}")
print(f"  Correct (human-judged)      : {answer_correct}")
print(f"  Answer accuracy             : {answer_accuracy:.2f}%")
print()
print(f"Refuse-case questions         : {refuse_total}")
print(f"  Correctly refused           : {refuse_correct}")
print(f"  Refuse accuracy             : {refuse_accuracy:.2f}%")
print()
print(f"Retrieval-checked questions   : {retrieval_checked}")
print(f"  Expected source found      : {retrieval_hits}")
print(f"  Retrieval hit-rate          : {retrieval_hit_rate:.2f}%")
print()
print(f"Average response time (sec)   : {avg_response_time:.2f}")
print("====================================")


# Save CSV
csv_file = "evaluation/results.csv"

with open(csv_file, "w", newline="", encoding="utf-8") as file:

    writer = csv.DictWriter(
        file,
        fieldnames=results[0].keys()
    )

    writer.writeheader()
    writer.writerows(results)


# Save JSON
json_file = "evaluation/results.json"

with open(json_file, "w", encoding="utf-8") as file:
    json.dump(results, file, indent=4)


# Save Evaluation Metrics
with open("evaluation/evaluation_matrix.md", "w", encoding="utf-8") as file:

    file.write("# Evaluation Results\n\n")

    file.write("| Metric | Value |\n")
    file.write("|--------|-------|\n")
    file.write(f"| Total Questions | {len(questions)} |\n")
    file.write(f"| Answerable Questions | {answer_total} |\n")
    file.write(f"| Answer Accuracy (human-judged) | {answer_accuracy:.2f}% |\n")
    file.write(f"| Refuse-Case Questions | {refuse_total} |\n")
    file.write(f"| Refuse Accuracy (auto-checked) | {refuse_accuracy:.2f}% |\n")
    file.write(f"| Retrieval-Checked Questions | {retrieval_checked} |\n")
    file.write(f"| Retrieval Hit-Rate (auto-checked) | {retrieval_hit_rate:.2f}% |\n")
    file.write(f"| Avg Response Time (sec) | {avg_response_time:.2f} |\n")


print("\nResults saved successfully!")
print("evaluation/results.csv")
print("evaluation/results.json")
print("evaluation/evaluation_matrix.md")
