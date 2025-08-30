import json
import re
import sys
from typing import List, Dict


def check_roles(messages: List[Dict[str, str]]) -> bool:
    last_role = None
    for message in messages:
        if message["role"] == last_role:
            return False
        last_role = message["role"]
    return True


def check_tags(messages: List[Dict[str, str]]) -> bool:
    tag_stack = []
    valid_tags = {
        "<tool_response>",
        "</tool_response>",
        "<tool_call>",
        "</tool_call>",
        "<tools>",
        "</tools>",
    }

    exceptions = {
        "<function-name>",
        "</function-name>",
        "<function-args>",
        "</function-args>",
        "<args-json-object>",
        "</args-json-object>",
    }

    for message in messages:
        content = message["content"]
        # tags = re.findall(r"</?[^>]+>", content)
        # tag is allowed to contain letters, numbers, underscores, and hyphens, must start with a letter or underscore
        tags = re.findall(r"<\/?[\w-]+>", content)

        for tag in tags:
            # Handle exceptions for function tags
            if tag in exceptions:
                continue

            if tag not in valid_tags:
                print(f"Invalid tag found: {tag} in message: ")
                return False

            if tag.startswith("</"):
                if not tag_stack or tag_stack[-1] != tag.replace("/", ""):
                    return False
                tag_stack.pop()
            else:
                tag_stack.append(tag)
    if tag_stack:
        print(f"Remaining tags in stack: {tag_stack}")
    return len(tag_stack) == 0


def inspect_dataset(dataset_path: str) -> bool:
    with open(dataset_path, "r", encoding="utf-8") as file:
        dataset = json.load(file)

    for entry in dataset:
        messages = entry.get("messages", [])

        if not check_roles(messages):
            print(f"Role check failed for entry: {entry}")
            return False

        if not check_tags(messages):
            print(f"Tag check failed for entry: {entry}")
            return False

    print("Dataset inspection passed.")
    return True


if __name__ == "__main__":
    dataset_path = sys.argv[1]
    if inspect_dataset(dataset_path):
        print("All checks passed.")
    else:
        print("Some checks failed.")
        exit(1)
    exit(0)
