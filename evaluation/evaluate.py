"""
evaluation/evaluate.py

Manual Evaluation Script for RAG Pipeline
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
correct = 0

print("\n==============================")
print("      RAG Evaluation")
print("==============================\n")

for index, item in enumerate(questions, start=1):

    question = item["question"]
    expected = item["expected_answer"]

    print(f"\nQuestion {index}/{len(questions)}")
    print("-" * 60)
    print("Question:")
    print(question)

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

    evaluation = input("\nIs the generated answer correct? (y/n): ").strip().lower()

    if evaluation == "y":
        result = "Correct"
        correct += 1
    else:
        result = "Incorrect"

    results.append({
        "Question": question,
        "Expected Answer": expected,
        "Generated Answer": generated_answer,
        "Response Time (sec)": response_time,
        "Sources": str(sources),
        "Result": result
    })


# Calculate Accuracy
accuracy = (correct / len(questions)) * 100


print("\n====================================")
print("        Evaluation Summary")
print("====================================")
print(f"Total Questions : {len(questions)}")
print(f"Correct Answers : {correct}")
print(f"Accuracy        : {accuracy:.2f}%")
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
    file.write(f"| Correct Answers | {correct} |\n")
    file.write(f"| Accuracy | {accuracy:.2f}% |\n")


print("\nResults saved successfully!")
print("evaluation/results.csv")
print("evaluation/results.json")
print("evaluation/evaluation_matrix.md")
