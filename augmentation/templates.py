from jijna2 import Template


aggressive_template = Template(
    """
Having this

```json
{{ example }}
```

Augment this example by paraphrasing the following fields:

- worldview (change to happening in {{ worldview }})
- role (change to {{ role }})
- persona (change according to worldview and role)
- knowledge (change according to worldview and role)
- state (change according to worldview and role)
- functions (slightly different function name and parameters)
- messages (paraphrase according to the worldview, persona, role, knowledge, state, functions, but keep the structure and ideas 1:1)

NOTE: 
- make sure that messages alternate between user and assistant. There should never be two user messages or two assistant messages in a row.
- make sure assistant are aligned with the worldview, persona, role, knowledge, state, and functions.
- keep json structure 1:1. This is for data augmentation to enhance my LLM.
"""
)

template = Template("""\
Having this

```json
{{ example }}
```

Augment this example by paraphrasing (worldview, role, persona, state, function_names, function_arguments, add new items in knowledge and use them in conversation).
Keep all ideas and conversation flow 1:1.
When calling tools, change arguments (different items, item names, types, prices, item descriptions according to dialogue, etc)
VERY IMPORTANT: All tool arguments must come strictly from dialogue, same as they appear in the messages, with minimum changes. Triple check that part!\
""")
