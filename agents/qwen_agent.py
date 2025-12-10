from unsloth import FastLanguageModel
import re
import json
from jinja2 import Template
from agents.utils import (
    SUCCESS_ACTION_CALL_MESSAGE,
    docstring_to_schema,
    get_model_path,
)


ENABLE_LOGS = True


def log(*args, **kwargs):
    if ENABLE_LOGS:
        print(*args, **kwargs)


SYSTEM_PROMPT = Template("""\
{{ role }}

# Metadata

{{ metadata }}

# Tools

You should call one or more functions to assist with the player query.

You are provided with function signatures within <tools></tools> XML tags:
<tools>
{% for item in functions %}
{{- item }}
{% endfor %}{"name": "reply", "description": "Reply to the player", "parameters": {}}
</tools>

For each function call, return a json object with function name and arguments within <tool_call></tool_call> XML tags:
<tool_call>
{"name":"<function-name>","arguments":<args-json-object>}
</tool_call>""")


REPLY_TO_TOOL_CALL_SYSTEM_PROMPT = Template("""\
{{ role }}

# Metadata

{{ metadata }}

# Tools

You are provided with function signatures within <tools></tools> XML tags:
<tools>
{% for item in functions %}
{{- item }}
{% endfor %}</tools>

# Important

- Reply in 1-4 sentences
- Sound natural
- Respect your persona
- Show genuine curiosity
- Ask follow-up questions""")


REPLY_SYSTEM_PROMPT = Template("""\
{{ role }}
    
# Metadata

{{ metadata }}

# Important

- Reply in 1-3 sentences
- Sound natural
- Show genuine curiosity
- Ask follow-up questions""")


def get_tool_calls(input_string: str):
    # Regex pattern to capture JSON objects between <tool_call> tags
    pattern = r"<tool_call>\s*(\{.*?\})\s*</tool_call>"

    # Find all JSON snippets
    matches = re.findall(pattern, input_string, flags=re.DOTALL)

    # Parse each JSON snippet into a Python dict
    parsed = [json.loads(match) for match in matches]

    # Display the resulting list of dicts
    return parsed


def format_message(msg):
    message = {
        "role": "user" if msg["speaker"] == "player" else "assistant",
        "content": msg["text"],
    }
    if msg["target_item"]:
        message["content"] = (
            message["content"]
            + " (Talking about "
            + ", ".join([item["name"] for item in msg["target_item"]])
            + ")"
        )

    return message


def extract_tools(tool_registry, action_registry):
    tool_registry = tool_registry["function_registry"]
    action_registry = action_registry["function_registry"]

    is_action = {}
    tools_schema, actions_schema = [], []
    for registry, schema in [
        (tool_registry, tools_schema),
        (action_registry, actions_schema),
    ]:
        for tool in registry.values():
            tool_name = tool["name"]
            tool_description = tool["description"]
            parsed_tool = docstring_to_schema(tool_description, tool_name)
            schema.append(parsed_tool)

            is_action[tool_name] = registry == action_registry

    return tools_schema + actions_schema, is_action


def process_tool_call_results(results):
    processed_results = []
    for result in results:
        if result["is_action"]:
            processed_results.append(
                {
                    "name": result["name"],
                    "arguments": result["parameters"],
                    "return": SUCCESS_ACTION_CALL_MESSAGE,
                }
            )
            continue
        if result["return"] == [{"information": "n/a"}]:
            continue  # Skip results with 'n/a' information
        processed_results.append(
            {
                "name": result["name"],
                "arguments": result["parameters"],
                "return": result["return"],
            }
        )
    return processed_results


class QwenAgent(object):
    """
    A simple agent implementation for the Sony CPDC challenge.
    """

    def __init__(self, 
            tool_lora_repo_id: str = "nuriyev/qwen3-14B-cpdc-tool-lora",
            tool_lora_revision: str = "490bb07891ce123b9e6d3fe90fced5bb6b6caf2f",
            persona_lora_repo_id: str = "nuriyev/qwen3-14B-cpdc-persona-lora",
            persona_lora_revision: str = "89064cd1fa0695ef50125a45c268153c91dc3d4d",
            base_model_repo_id: str = "unsloth/Qwen3-14B",
            base_model_revision: str = "b8755c0b498d7b538068383748d6dc20397b4d1f",
            max_seq_length: int = 5500,
            load_in_4bit: bool = True,
            load_in_8bit: bool = False,
        ):
        
        lora_tool_path = get_model_path(
            tool_lora_repo_id,
            revision=tool_lora_revision,
            local_files_only=False
        )
        lora_persona_path = get_model_path(
            persona_lora_repo_id,
            revision=persona_lora_revision,
            local_files_only=False
        )
        model_path = get_model_path(
            base_model_repo_id,
            revision=base_model_revision,
            local_files_only=False
        )
        self.model, self.tokenizer = FastLanguageModel.from_pretrained(
            model_name=model_path,
            max_seq_length=max_seq_length,
            load_in_4bit=load_in_4bit,
            load_in_8bit=load_in_8bit,
        )
        FastLanguageModel.for_inference(self.model)
        self.model.load_adapter(
            lora_tool_path,
            adapter_name="lora_tool",
        )
        self.model.load_adapter(
            lora_persona_path,
            adapter_name="lora_persona",
        )
        self.naturalize_reply_to_tool_call = False

        print("Model loaded successfully with Unsloth from local path.")

    def generate(self, messages, **kwargs):
        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=kwargs.get("add_generation_prompt", True),
            enable_thinking=kwargs.get("enable_thinking", False),
        ) + kwargs.get("text", "")
        model = kwargs.get("model", self.model)
        model_inputs = self.tokenizer(text, return_tensors="pt").to(model.device)

        # conduct text completion
        generated_ids = model.generate(
            **model_inputs,
            eos_token_id=kwargs.get("eos_token_id", self.tokenizer.eos_token_id),
            max_new_tokens=kwargs.get("max_new_tokens", 128),
            temperature=kwargs.get("temperature", 0.7),
            top_p=kwargs.get("top_p", 0.8),
            top_k=kwargs.get("top_k", 20),
            min_p=kwargs.get("min_p", 0),
            do_sample=kwargs.get("do_sample", True),
            use_cache=kwargs.get("use_cache", True),
            num_beams=kwargs.get("num_beams", 1),
            suppress_tokens=kwargs.get("suppress_tokens", []),
        )
        output_ids = generated_ids[0][len(model_inputs.input_ids[0]) :].tolist()
        # decode the generated text

        content = self.tokenizer.decode(output_ids, skip_special_tokens=True).strip(
            "\n"
        )
        return content

    def generate_functions_and_responses(
        self,
        tool_registry,
        action_registry,
        worldview,
        persona,
        role,
        knowledge,
        state,
        dialogue,
        executor,
    ):
        """
        Given the background information, perform adequate function calls, and based on the function call results, generate coherent and reasonable responses.
        This agent does the following four steps.
        1. Ask the LLM to generate the necessary functions to call.
        2. Parse the generation to obtain function names and arguments to call.
        3. Call the `executor` to obtain results for the function calls.
        4. Call the LLM to generate responses based on the background information and the function call results.

        Parameters
        ----------
            tool_registry, action_registry: Dict[str, Dict[str, str]] are function registries for tool and action functions,
                from which we can index functions with function names.
                For example, I can index a tool function named 'tool1' via `tool_registry['function_registry']['tool1'][k]`,
                where k can be 'args', 'description', or 'name'.
            worldview: str, the worldview of the current dialogue.
            persona: Dict[str, str], describes the persona of the NPC, e.g. persona['name'], persona['age'], persona['gender'], persona['occupation'].
                See the sample and training datasets for details.
            role: str, the role of the NPC.
            knowledge: Dict[str, Any], contains basic knowledge about the items (e.g. quests, weapons). See the sample and training datasets for details.
            state: Dict[str, str], the time, location, etc. of the current conversation.
            dialogue: List[Dict[str, str]]. It records the previous turns of the dialogue.
                Each dict in the list is of the following format:
                {
                    "speaker": ...,
                    "text": ...,
                    "target_item": ...
                }
            executor: It is a module that can execute function calls I need and record the history of all function calls I make.
                Call the executor with `executor.execute(function_items)`, where `function_items`
                is a list of dictionaries containing all function calls to make.
                Each dictionary in `function_items` should have the following format:
                    {
                        'name': <function_name>,
                        'parameters': {
                            <param_name>: <param_val>,
                            ...
                        }
                    }


        Returns
        ----------
            Dict[str, str] with the following structure.
                {
                    "prompts": Optional. The prompt of the current turn.
                    "final_responses": Your response of the current turn.
                }

        NOTE: You do not need to return the generated function calls. The `executor` will automatically record that.
        """

        functions_schema, is_action = extract_tools(tool_registry, action_registry)

        messages = [format_message(msg) for msg in dialogue]

        metadata = json.dumps(
            {
                "worldview": worldview,
                "persona": persona,
                "knowledge": knowledge,
                "state": state,
            },
            ensure_ascii=False,
        )

        tool_calls = self.get_tool_calls(
            metadata,
            role,
            messages,
            functions_schema,
        )
        try:
            if not tool_calls or tool_calls[0]["name"] != "reply":
                results = executor.execute(
                    [
                        {
                            "name": tc["name"],
                            "parameters": tc.get("arguments", {}) or {},
                        }
                        for tc in tool_calls
                    ]
                )
                log(f"{results = }")
                results = [
                    {**r, "is_action": is_action[r["name"]]} for r in results
                ]  # Convert list of dicts to dict
                processed_results = process_tool_call_results(results)
                log(f"{processed_results = }")
                formatted_tool_response = "\n".join(
                    [
                        f"<tool_response>\n{json.dumps(r, ensure_ascii=False)}\n</tool_response>"
                        for r in processed_results
                    ]
                )
                formatted_tool_request = "\n".join(
                    [
                        f"""<tool_call>\n{
                            json.dumps(
                                {"name": r["name"], "arguments": r["arguments"]},
                                ensure_ascii=False,
                            )
                        }\n</tool_call>"""
                        for r in processed_results
                    ]
                )
                if formatted_tool_request and formatted_tool_response:
                    messages.extend(
                        [
                            {"role": "assistant", "content": formatted_tool_request},
                            {"role": "user", "content": formatted_tool_response},
                        ]
                    )
                    response = self.reply_to_tool_call(
                        metadata=metadata,
                        role=role,
                        messages=messages,
                        functions_schema=functions_schema,
                    )
                    return {"final_responses": response, "tool_calls": tool_calls}
        except Exception as e:
            log(f"Error during executor execution: {e}")

        response = self.reply_with_no_tool_calls(metadata, role, messages)
        return {"final_responses": response, "tool_calls": tool_calls}

    def get_tool_calls(self, metadata, role, messages, functions_schema):
        """
        Get tool calls from the LLM based on the provided metadata, role, and messages.
        """
        system_prompt = SYSTEM_PROMPT.render(
            role=role,
            metadata=metadata,
            functions=[json.dumps(f, ensure_ascii=False) for f in functions_schema],
        )

        messages = [{"role": "system", "content": system_prompt}, *messages]

        self.model.set_adapter("lora_tool")
        response = (
            '<tool_call>\n{"name": "'
            + self.generate(
                messages,
                text='<tool_call>\n{"name": "',
                eos_token_id=[
                    self.tokenizer.eos_token_id,
                    21034,  # 21034 is the `reply` token # TODO: replace with more robust stopping criteria
                ],
            )
        )
        log(f"{response = }")

        tool_calls = get_tool_calls(response)
        return tool_calls

    def reply_with_no_tool_calls(self, metadata, role, messages, **generation_kwargs):
        """
        Generate a reply when there are no tool calls based on the provided metadata, role, and messages.
        """
        system_prompt = REPLY_SYSTEM_PROMPT.render(role=role, metadata=metadata)

        messages = [{"role": "system", "content": system_prompt}, *messages]

        self.model.disable_adapters()
        response = self.generate(messages, **generation_kwargs)
        self.model.enable_adapters()
        log(f"{response = }")

        return response

    def reply_to_tool_call(
        self,
        metadata,
        role,
        messages,
        functions_schema,
    ):
        """
        Generate a reply to the tool call based on the provided metadata, role, and messages.
        """
        system_prompt = REPLY_TO_TOOL_CALL_SYSTEM_PROMPT.render(
            role=role,
            metadata=metadata,
            functions=[
                json.dumps(
                    {"name": f["name"], "description": f["description"]},
                    ensure_ascii=False,
                )
                for f in functions_schema
            ],
        )

        self.model.set_adapter("lora_persona")
        response = self.generate(
            [{"role": "system", "content": system_prompt}, *messages],
            suppress_tokens=[151657, 151658],  # <tool_call>, </tool_call>
            enable_thinking=True,
            text="<think>\nI should integrate all the factual data from <tool_response> to my response. Additionally, I should sound more natural, human-like and respect my persona.\n</think>\n\n",
        )
        log(f"{response = }")

        if self.naturalize_reply_to_tool_call:
            response = self.reply_with_no_tool_calls(
                metadata=metadata,
                role=role,
                messages=messages,
                enable_thinking=True,
                model=self.model,
                text=f"<think>\nI should reply with something like `{response}`, but sounding more natural, human-like and respecting persona.\n</think>\n\n",
            )

        return response
