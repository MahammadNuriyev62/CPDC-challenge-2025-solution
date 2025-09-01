import json
from agents.user_config import UserAgent
from agents.qwen_agent import get_tool_calls
from sentence_transformers import SentenceTransformer
import numpy as np


model = SentenceTransformer("Qwen/Qwen3-Embedding-0.6B")

with open("./results/test_gold.json", "r") as f:
    test_gold = json.load(f)


def preprocess_tool_call(tool_calls):
    tool_calls_lowered = json.loads(json.dumps(tool_calls, ensure_ascii=False).lower())
    tool_calls_sorted_jsons = sorted(
        [json.dumps(j, ensure_ascii=False) for j in tool_calls_lowered]
    )
    tool_calls_sorted = [json.loads(j) for j in tool_calls_sorted_jsons]
    return tool_calls_sorted


def compute_similarity(str1, str2):
    embeddings = model.encode([str1, str2])
    similarity = np.dot(embeddings[0], embeddings[1]) / (
        np.linalg.norm(embeddings[0]) * np.linalg.norm(embeddings[1])
    )
    return float(similarity)


actual = []
gold = []
similarities = []
n_exact_match_total = 0
n_total_correct_functions = 0
n_total_incorrect_functions = 0

if __name__ == "__main__":
    agent = UserAgent()

    for entry in test_gold:
        metadata = {
            "worldview": entry["worldview"],
            "persona": entry["persona"],
            "knowledge": entry["knowledge"],
            "state": entry["state"],
        }
        role = entry["role"]
        functions_schema = entry["functions"]

        messages = []

        metadata = json.dumps(
            metadata,
            ensure_ascii=False,
        )
        for message_id in range(0, len(entry["messages"]) - 1, 2):
            user_message = entry["messages"][message_id]
            assistant_message = entry["messages"][message_id + 1]
            print(f"\n\n{user_message['content'] = }")
            if "<tool_response>" in user_message["content"]:
                response = agent.reply_to_tool_call(
                    metadata=metadata,
                    role=role,
                    messages=[
                        *messages,
                        entry["messages"][message_id - 1],
                        user_message,
                    ],
                    functions_schema=functions_schema,
                )
                print(f"response_actual = {response}")
                response_gold = assistant_message["content"]
                print(f"response_gold   = {response_gold}")
                continue

            messages.append(user_message)
            tool_calls = agent.get_tool_calls(
                metadata=metadata,
                role=role,
                messages=messages,
                functions_schema=functions_schema,
            )
            print(f"tool_calls_actual = {tool_calls}")
            tool_calls_gold = get_tool_calls(assistant_message["content"])
            print(f"tool_calls_gold   = {tool_calls_gold}")

            # Preprocess tool calls
            preprocessed_actual = preprocess_tool_call(tool_calls)
            preprocessed_gold = preprocess_tool_call(tool_calls_gold)

            # Check exact match
            exact_match = preprocessed_actual == preprocessed_gold
            print(f"same? = {exact_match}")
            if exact_match:
                n_exact_match_total += 1

            # Stringify for storage and similarity computation
            actual_str = json.dumps(preprocessed_actual, ensure_ascii=False)
            gold_str = json.dumps(preprocessed_gold, ensure_ascii=False)

            actual.append(actual_str)
            gold.append(gold_str)

            # Compute and store similarity
            similarity = compute_similarity(actual_str, gold_str)
            similarities.append(similarity)
            print(f"similarity = {similarity:.4f}")

            gold_function_names = [f["name"] for f in tool_calls_gold]
            function_names = [f["name"] for f in tool_calls]

            n_correct_functions = len(set(gold_function_names) & set(function_names))
            n_incorrect_functions = len(set(function_names) - set(gold_function_names))
            n_total_correct_functions += n_correct_functions
            n_total_incorrect_functions += n_incorrect_functions

            if not tool_calls and not tool_calls_gold:
                response = agent.reply_to_tool_call(
                    metadata=metadata,
                    role=role,
                    messages=[
                        *messages,
                        entry["messages"][message_id - 1],
                        user_message,
                    ],
                    functions_schema=functions_schema,
                )
                print(f"response_actual = {response}")
                response_gold = assistant_message["content"]
                print(f"response_gold   = {response_gold}")
            if "<tool_call>" not in assistant_message["content"]:
                messages.append(assistant_message)


with open("./results/tool_calls_actual.json", "w") as f:
    json.dump(actual, f, ensure_ascii=False, indent=4)

with open("./results/tool_calls_gold.json", "w") as f:
    json.dump(gold, f, ensure_ascii=False, indent=4)

# Save similarities
with open("./results/similarities.json", "w") as f:
    json.dump(similarities, f, indent=4)

# Compute similarity statistics
avg_similarity = np.mean(similarities) if similarities else 0
min_similarity = np.min(similarities) if similarities else 0
max_similarity = np.max(similarities) if similarities else 0
std_similarity = np.std(similarities) if similarities else 0

print("\n\n\n")
print(f"n_exact_match_total = {n_exact_match_total}")
print(f"n_total_correct_functions = {n_total_correct_functions}")
print(f"n_total_incorrect_functions = {n_total_incorrect_functions}")
print(f"n_total_functions = {n_total_correct_functions + n_total_incorrect_functions}")
print(f"n_total_functions = {len(gold)}")
print(f"n_total_tool_calls = {len(actual)}")
print("\n--- Similarity Statistics ---")
print(f"Average similarity: {avg_similarity:.4f}")
print(f"Min similarity: {min_similarity:.4f}")
print(f"Max similarity: {max_similarity:.4f}")
print(f"Std deviation: {std_similarity:.4f}")
print(f"Similarities >= 0.9: {sum(1 for s in similarities if s >= 0.9)}")
print(f"Similarities >= 0.8: {sum(1 for s in similarities if s >= 0.8)}")
print(f"Similarities >= 0.7: {sum(1 for s in similarities if s >= 0.7)}")
