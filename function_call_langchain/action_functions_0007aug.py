from langchain.tools import tool


@tool
def select_request_confirm(lesson_name: str) -> None:
    """
    Confirm whether to select the specified lesson (e.g. Figure Drawing, Still Life Sketching, Color Theory Basics, etc.).

    Parameters:
    ----------
    lesson_name: str
        Specified lesson name (e.g. Figure Drawing, Still Life Sketching, Color Theory Basics, etc.). Uses the lesson name mentioned in the conversation.

    Returns:
    -------
    None
    """

    pass


@tool
def select(lesson_name: str) -> None:
    """
    Select the specified lesson (e.g. Figure Drawing, Still Life Sketching, Color Theory Basics, etc.).

    Parameters:
    ----------
    lesson_name: str
        Specified lesson name (e.g. Figure Drawing, Still Life Sketching, Color Theory Basics, etc.). Uses the lesson name mentioned in the conversation.

    Returns:
    -------
    None
    """

    pass


@tool
def start(lesson_name: str) -> None:
    """
    Start the specified lesson (e.g. Figure Drawing, Still Life Sketching, Color Theory Basics, etc.).

    Parameters:
    ----------
    lesson_name: str
        Specified lesson name (e.g. Figure Drawing, Still Life Sketching, Color Theory Basics, etc.). Uses the lesson name mentioned in the conversation.

    Returns:
    -------
    None
    """

    pass


all_functions = [select_request_confirm, select, start]
action_functions_0007aug = {
    "function_registry": {
        f.name: {"name": f.name, "description": f.description, "args": f.args}
        for f in all_functions
    }
}
