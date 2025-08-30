import json
import sys


def check_consecutive_roles(dataset):
    for item in dataset:
        messages = item.get("messages", [])
        last_role = None
        for message in messages:
            if message["role"] == last_role:
                return item
            last_role = message["role"]
    return False


def check_valid_roles(dataset):
    """Check that all roles are either 'user' or 'assistant'"""
    valid_roles = {"user", "assistant"}
    for item in dataset:
        messages = item.get("messages", [])
        for message in messages:
            role = message.get("role")
            if role not in valid_roles:
                return {"item": item, "invalid_role": role}
    return False


def check_for_unicode_characters(dataset):
    # check if anywhere (messages, worldview, etc) in the dataset there is "\u"
    for item in dataset:
        if "\\u" in json.dumps(item, ensure_ascii=False):
            return item
    return False


def check_for_duplicates(dataset):
    contents = set()
    for item in dataset:
        messages = item.get("messages", [])
        joined_messages_content = " ".join(
            [msg["content"] for msg in messages if "content" in msg]
        )
        if joined_messages_content in contents:
            return item
        contents.add(joined_messages_content)
    return False


def check_functions(dataset):
    # check that every function in functions in every entry is dict with name, description and parameters
    for item in dataset:
        functions = item.get("functions", [])
        for function in functions:
            if not isinstance(function, dict):
                return item
            if not all(
                key in function for key in ["name", "description", "parameters"]
            ):
                return item
    return False


with open(sys.argv[1], "r") as fp:
    eval_dataset = json.load(fp)
with open(sys.argv[2], "r") as fp:
    train_dataset = json.load(fp)

dataset = eval_dataset + train_dataset

if item := check_consecutive_roles(dataset):
    print(f"Invalid roles in item: {item}")
if result := check_valid_roles(dataset):
    print(f"Invalid role '{result['invalid_role']}' found in item: {result['item']}")
if item := check_for_duplicates(dataset):
    print(f"Duplicate messages in item: {item}")
if item := check_for_unicode_characters(dataset):
    print(f"Unicode characters found in item: {item}")
if item := check_functions(dataset):
    print(f"Invalid function format in item: {item}")
