import json
import re
import os
from typing import Dict, Any, List, Optional
from huggingface_hub.utils import EntryNotFoundError
from huggingface_hub import snapshot_download

SUCCESS_ACTION_CALL_MESSAGE = "The action was successfully executed."


_JSON_PRIMITIVES = {
    "str": "string",
    "string": "string",
    "int": "integer",
    "integer": "integer",
    "float": "number",
    "double": "number",
    "number": "number",
    "bool": "boolean",
    "boolean": "boolean",
    "dict": "object",
    "mapping": "object",
    "object": "object",
    "list": "array",
    "array": "array",
    "sequence": "array",
}


def _clean(tok: str) -> str:
    return tok.strip().lower().rstrip(".,;")


def _py_to_json(type_str: str) -> Dict[str, Any]:
    t = _clean(type_str)
    if not t:
        return {"type": "string"}

    m = re.match(r"optional\[(.+)\]$", t)
    if m:  # Optional[…]
        t = m.group(1)

    for prefix in ("list", "sequence", "array"):
        if t.startswith(f"{prefix}["):  # list[int]
            inner = t[len(prefix) + 1 : -1]
            return {"type": "array", "items": _py_to_json(inner)}
        if t.startswith(f"{prefix} of "):  # list of int
            inner = t[len(prefix) + 4 :].strip()
            return {"type": "array", "items": _py_to_json(inner)}

    return {"type": _JSON_PRIMITIVES.get(t.split()[0], "string")}


def _squash(text: str) -> str:
    """Collapse _any_ whitespace run to a single space, strip ends."""
    return re.sub(r"\s+", " ", text).strip()


def docstring_to_schema(docstring: str, func_name: str) -> Dict[str, Any]:
    """
    Convert a Google/Numpy-style docstring into an OpenAI
    function-calling schema. Guarantees that multi-line chunks
    (both the top description and per-param descriptions) are
    joined with **exactly one space**.
    """
    p_hdr = re.compile(r"\n\s*Parameters?\s*:?\s*(?:\n[-\s]{2,})?", re.I)
    r_hdr = re.compile(r"\n\s*Returns?\s*:?\s*(?:\n[-\s]{2,})?", re.I)

    p_match = p_hdr.search(docstring)
    if p_match:
        raw_desc = docstring[: p_match.start()]
        params_block = docstring[p_match.end() :]
    else:
        raw_desc, params_block = docstring, ""

    r_match = r_hdr.search(params_block)
    if r_match:
        params_block = params_block[: r_match.start()]

    description = _squash(raw_desc)

    param_line = re.compile(r"^\s*(\w+)\s*:\s*([^\n]+)", re.M)
    properties: Dict[str, Dict[str, Any]] = {}
    required: List[str] = []

    current: Optional[str] = None
    cur_type: Optional[str] = None
    cur_desc: List[str] = []

    def flush() -> None:
        nonlocal current, cur_type, cur_desc
        if current is None:
            return
        entry = _py_to_json(cur_type or "")
        entry["description"] = _squash(" ".join(cur_desc))
        properties[current] = entry
        required.append(current)

    for line in params_block.splitlines():
        m = param_line.match(line)
        if m:
            flush()
            current, cur_type = m.groups()
            cur_desc = []
        elif current and line.strip():
            cur_desc.append(line.strip())

    flush()

    schema: Dict[str, Any] = {"name": func_name, "description": description}
    if properties:
        schema["parameters"] = {"type": "object", "properties": properties}
        # Add `"required": required` if you need it
    else:
        schema["parameters"] = {}

    return schema


def format_calls(calls):
    """
    Convert a list of call-descriptions into a string like:
    <tool_call>
    {"name": "{function_name}", "arguments": {"{parameter}": "{item_name}"}}
    </tool_call>
    """
    parts = []
    for call in calls:
        name = call["name"]
        params = call.get("parameters", {})
        call = {
            "name": name,
            "arguments": params,
        }
        parts += [f"<tool_call>\n{json.dumps(call, ensure_ascii=False)}\n</tool_call>"]

    return "\n".join(parts)


def format_response(response):
    """
    Convert a response dict into a string like:
    <tool_response>
    {"name": "{function_name}", "return": {return_value}}
    </tool_response>
    """
    parts = []
    for call in response:
        name = call["name"]
        return_value = call.get("return", {})
        call = {
            "name": name,
            "arguments": call.get("parameters", {}),
            "return": return_value if return_value else SUCCESS_ACTION_CALL_MESSAGE,
        }
        parts += [
            f"<tool_response>\n{json.dumps(call, ensure_ascii=False)}\n</tool_response>"
        ]

    return "\n".join(parts)


def get_model_path(repo_id: str, revision: str = "main") -> str:
    # check if we're in colab
    if "COLAB_GPU" in os.environ:
        return repo_id

    # revision is important if specified in your aicrowd.json
    # It defaults to 'main' in snapshot_download if not provided
    revision_from_aicrowd_json = revision  # Get this from your aicrowd.json

    local_model_path = None
    try:
        # This will attempt to find the model in the local Hugging Face cache.
        # local_files_only=True ensures it doesn't try to download.
        # If the AICROWD platform pre-downloaded it to the standard cache, this will work.
        print(
            f"Attempting to locate model '{repo_id}' (revision: {revision_from_aicrowd_json}) locally..."
        )
        local_model_path = snapshot_download(
            repo_id,
            revision=revision_from_aicrowd_json,
            local_files_only=True,
            # token=True, # or os.environ.get("HF_TOKEN")
            # Usually not needed if local_files_only=True and files are present
            # but include if AICROWD environment might require it for cache access.
            # The `token` from aicrowd.json is for the platform's download step.
        )
        print(f"Model '{repo_id}' found locally at: {local_model_path}")

    except FileNotFoundError:  # Older huggingface_hub versions
        print(
            f"Model '{repo_id}' not found in local cache (FileNotFoundError). This is unexpected if AICROWD pre-downloaded it."
        )
        # Handle error appropriately - this shouldn't happen if aicrowd.json worked
        raise
    except EntryNotFoundError:  # Newer huggingface_hub versions
        print(
            f"Model '{repo_id}' not found in local cache (EntryNotFoundError). This is unexpected if AICROWD pre-downloaded it."
        )
        # Handle error appropriately
        raise
    except Exception as e:
        print(
            f"An unexpected error occurred while trying to locate the model locally: {e}"
        )
        # You might want to see if the Hugging Face cache path is standard
        # default_cache_path = HfFileSystem().hf_hub_cache
        # print(f"Default Hugging Face cache path: {default_cache_path}")
        raise

    # Now use the resolved local_model_path with Unsloth
    print(f"Loading model from local path: {local_model_path}")

    return local_model_path  # This is the path to use with Unsloth or other tools
