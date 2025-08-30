import json
import re
import sys

# Map JSON Schema types to Python types
TYPE_MAP = {
    "string": str,
    "number": (int, float),
    "object": dict,
    "array": list,
    "boolean": bool,
}

# Regex to capture all <tool_call> blocks with JSON payload
TOOL_CALL_RE = re.compile(r"<tool_call>\s*(\{.*?\})\s*</tool_call>", re.DOTALL)


def load_dataset(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# Extract all tool calls from assistant messages, logging parse errors with entry id and raw block content
def extract_tool_calls(messages, entry_id):
    calls = []
    for msg in messages:
        if msg.get("role") == "assistant":
            content = msg.get("content", "")
            for match in TOOL_CALL_RE.finditer(content):
                block = match.group(0)
                json_part = match.group(1)
                try:
                    calls.append(json.loads(json_part))
                except json.JSONDecodeError as e:
                    # Escape newlines and other special chars, and double quotes
                    escaped = block.encode("unicode_escape").decode("ascii")
                    escaped = escaped.replace('"', '\\"')
                    print(
                        f"[Entry id={entry_id}] ⚠️ Failed to parse JSON in block: {escaped}\nError: {e}"
                    )
    return calls


# Find the function schema by name in the entry's function list
def find_function_schema(functions, name):
    for fn in functions:
        if fn.get("name") == name:
            # Handle cases where parameters may be empty or missing 'properties'
            params = fn.get("parameters", {}) or {}
            return params.get("properties", {})
    return None


# Validate a single tool call against its schema
def check_call(call, schema, entry_id, call_index):
    errors = []
    args = call.get("arguments", {}) or {}
    # Unexpected args
    for arg in args:
        if arg not in schema:
            errors.append(f"  • Unexpected argument '{arg}'")
    # Type-check each provided argument
    for arg, val in args.items():
        expected = schema.get(arg)
        if expected:
            exp_type = expected.get("type")
            py_type = TYPE_MAP.get(exp_type)
            if py_type and not isinstance(val, py_type):
                errors.append(
                    f"  • Argument '{arg}' expects {exp_type} but got {type(val).__name__}"
                )
    if errors:
        print(
            f"[Entry id={entry_id} – call {call_index} to '{call.get('name')}'] issues:"
        )
        for e in errors:
            print(e)


# Main routine
def main(dataset_path):
    data = load_dataset(dataset_path)
    for idx, entry in enumerate(data, start=1):
        entry_id = entry.get("id", idx)
        funcs = entry.get("functions", []) or []
        calls = extract_tool_calls(entry.get("messages", []), entry_id)
        for j, call in enumerate(calls, start=1):
            schema = find_function_schema(funcs, call.get("name"))
            if schema is None:
                print(
                    f"[Entry id={entry_id} – call {j}] Unknown function '{call.get('name')}'"
                )
            else:
                check_call(call, schema, entry_id, j)


if __name__ == "__main__":
    main(sys.argv[1])
