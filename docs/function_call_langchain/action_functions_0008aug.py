from langchain.tools import tool


@tool
def announce_break() -> None:
    """
    Announce a short break during the lesson. Useful for long sessions.
    Returns:
    -------
    None
    """
    pass


@tool
def select_request_confirm(lesson_name: str) -> None:
    """
    Confirm whether to select the specified lesson (e.g. Figure Drawing, Still Life Sketching).
    Parameters:
    ----------
    lesson_name: str
        The lesson name.
    Returns:
    -------
    None
    """
    pass


@tool
def select(lesson_name: str) -> None:
    """
    Select the specified lesson for the student.
    Parameters:
    ----------
    lesson_name: str
    Returns:
    -------
    None
    """
    pass


@tool
def start(lesson_name: str) -> None:
    """
    Start the specified lesson.
    Parameters:
    ----------
    lesson_name: str
    Returns:
    -------
    None
    """
    pass


@tool
def show_material_list() -> None:
    """
    Show a list of recommended materials for the current or next lesson.
    Returns:
    -------
    None
    """
    pass


@tool
def get_today_schedule() -> None:
    """
    Display today's lesson schedule for all students.
    Returns:
    -------
    None
    """
    pass


@tool
def submit_portfolio_feedback() -> None:
    """
    Submit tutor feedback on a student’s portfolio. Does not require arguments; works contextually.
    Returns:
    -------
    None
    """
    pass


all_functions = [
    announce_break,
    select_request_confirm,
    select,
    start,
    show_material_list,
    get_today_schedule,
    submit_portfolio_feedback,
]
action_functions_0008aug = {
    "function_registry": {
        f.name: {"name": f.name, "description": f.description, "args": f.args}
        for f in all_functions
    }
}
