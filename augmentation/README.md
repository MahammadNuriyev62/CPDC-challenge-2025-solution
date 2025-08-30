# Dataset Validation Suite

A comprehensive validation toolkit for conversational AI training datasets with function-calling capabilities. These scripts ensure data quality, consistency, and proper formatting before model training.

## Overview

This suite contains three Python scripts that validate different aspects of conversational datasets:

- **validate_dataset_consistency.py** - Basic consistency and duplicate detection
- **validate_roles_and_tags.py** - Message role alternation and XML tag validation
- **validate_tool_calls.py** - Function call schema validation

## Requirements

- Python 3.6+
- Standard library only (no external dependencies)

## Usage

### validate_dataset_consistency.py

Checks for role alternation, duplicates, Unicode issues, and function format.

```bash
python validate_dataset_consistency.py eval_dataset.json train_dataset.json
```

**What it validates:**

- ✓ Messages alternate between roles (no consecutive same-role messages)
- ✓ All roles are either "user" or "assistant"
- ✓ No duplicate conversation content across dataset
- ✓ No escaped Unicode characters (`\u` sequences)
- ✓ Functions have required fields: `name`, `description`, `parameters`

**Example output:**

```
Invalid roles in item: {"id": 123, "messages": [...]}
Invalid role 'system' found in item: {"id": 789, "messages": [...]}
Duplicate messages in item: {"id": 456, "messages": [...]}
```

### validate_roles_and_tags.py

Validates conversation structure and XML-like tag usage.

```bash
python validate_roles_and_tags.py dataset.json
```

**What it validates:**

- ✓ Proper role alternation in conversations
- ✓ Valid XML tag usage (proper nesting and closing)
- ✓ Only whitelisted tags are used

**Accepted tags:**

- `<tool_response>`, `</tool_response>`
- `<tool_call>`, `</tool_call>`
- `<tools>`, `</tools>`

**Exception tags (allowed but not validated):**

- `<function-name>`, `</function-name>`
- `<function-args>`, `</function-args>`
- `<args-json-object>`, `</args-json-object>`

**Example output:**

```
Invalid tag found: <invalid_tag> in message
Tag check failed for entry: {"id": 789, ...}
Dataset inspection passed.
```

### validate_tool_calls.py

Validates function calls against their defined schemas.

```bash
python validate_tool_calls.py dataset.json
```

**What it validates:**

- ✓ Tool calls can be parsed as valid JSON
- ✓ Called functions exist in the function definitions
- ✓ Arguments match expected schema
- ✓ Argument types are correct

**Example output:**

```
[Entry id=42 – call 1 to 'search_web'] issues:
  • Unexpected argument 'limit'
  • Argument 'query' expects string but got int

[Entry id=99] ⚠️ Failed to parse JSON in block: <tool_call>{invalid json}</tool_call>
Error: Expecting property name enclosed in double quotes
```

## Dataset Format

The expected dataset format is a JSON array of conversation entries:

```json
[
  {
    "id": "unique_id",
    "messages": [
      {
        "role": "user",
        "content": "User message content"
      },
      {
        "role": "assistant",
        "content": "Assistant response with <tool_call>{\"name\": \"function_name\", \"arguments\": {...}}</tool_call>"
      },
      {
        "role": "user",
        "content": "<tool_response>Tool output here</tool_response>"
      }
    ],
    "functions": [
      {
        "name": "function_name",
        "description": "What this function does",
        "parameters": {
          "properties": {
            "param1": { "type": "string" },
            "param2": { "type": "number" }
          }
        }
      }
    ]
  }
]
```

## Validation Strategy

Run all three validators in sequence for comprehensive validation:

```bash
# 1. Check basic consistency
python validate_dataset_consistency.py eval.json train.json

# 2. Validate structure and tags
python validate_roles_and_tags.py train.json # or eval.json

# 3. Validate function calls
python validate_tool_calls.py eval.json # or train.json
```

## Exit Codes

- `0` - All validations passed
- `1` - Validation failures detected

## Common Issues and Solutions

| Issue                          | Solution                                                    |
| ------------------------------ | ----------------------------------------------------------- |
| Consecutive same-role messages | Ensure proper user/assistant alternation                    |
| Unclosed XML tags              | Check all `<tag>` has matching `</tag>`                     |
| Unicode escape sequences       | Decode strings properly before saving dataset               |
| Missing function parameters    | Ensure all functions have name, description, and parameters |
| Type mismatches in tool calls  | Verify arguments match schema types                         |

## Best Practices

1. **Run all validators** before training to catch different issue types
2. **Fix errors incrementally** - address one validator's issues before moving to the next
3. **Validate samples** during dataset creation to catch issues early
4. **Keep backups** before making bulk corrections
5. **Use consistent formatting** for tool calls and responses
