from typing import List, Dict
from langchain.tools import tool

# ────────────────────────────────
#  Search & lesson insight
# ────────────────────────────────


@tool
def search_lesson(
    lesson_name: str = "",
    lesson_level: str = "",
    lesson_duration: str = "",
    lesson_reward: str = "",
    lesson_description: str = "",
    lesson_name_operator: str = "",
    lesson_level_operator: str = "",
    lesson_duration_operator: str = "",
    lesson_reward_operator: str = "",
) -> List[Dict[str, str]]:
    """
    Flexible query across the academy’s lesson catalogue.

    Parameters
    ----------
    lesson_name : str, optional
        Exact or partial lesson titles to match.
    lesson_level : str, optional
        Desired difficulty (e.g., "Beginner", "Advanced").
    lesson_duration : str, optional
        Target duration string (e.g., "3 hours", "2 days").
    lesson_reward : str, optional
        Expected reward or outcome (e.g., "Certificate").
    lesson_description : str, optional
        Keywords or phrases that should appear in the description.
    lesson_name_operator : str, optional
        Comparison operator for lesson_name (e.g., "other than").
    lesson_level_operator : str, optional
        Operator for lesson_level (e.g., "or above", "or below").
    lesson_duration_operator : str, optional
        Operator for lesson_duration (e.g., "or less", "longest").
    lesson_reward_operator : str, optional
        Operator for lesson_reward (e.g., "highest", "low").

    Returns
    -------
    List[Dict[str, str]]
        Matching lessons with a brief justification for each.
    """
    pass


@tool
def check_basic_info(lesson_name: str) -> List[Dict[str, str]]:
    """
    Retrieve level, duration, reward, and a short summary of a lesson.

    Parameters
    ----------
    lesson_name : str
        Exact title of the lesson to inspect.

    Returns
    -------
    List[Dict[str, str]]
        A single-item list containing the core information.
    """
    pass


@tool
def check_lesson_full_status(lesson_name: str) -> bool:
    """
    Determine whether a lesson is currently at capacity.

    Parameters
    ----------
    lesson_name : str
        Exact title of the lesson to check.

    Returns
    -------
    bool
        True  → lesson is full.
        False → seats are available.
    """
    pass


# ────────────────────────────────
#  Daily operations (all zero-arg)
# ────────────────────────────────


@tool
def get_today_schedule() -> List[Dict[str, str]]:
    """
    Return the academy’s timetable for today.

    Returns
    -------
    List[Dict[str, str]]
        Each dict contains `lesson` and `time`.
    """
    pass


@tool
def show_material_list() -> List[str]:
    """
    List materials recommended for whatever lesson is in focus.

    Returns
    -------
    List[str]
        Simple list of material names.
    """
    pass


@tool
def get_live_demo_schedule() -> List[Dict[str, str]]:
    """
    Retrieve today’s live demo timetable.

    Returns
    -------
    List[Dict[str, str]]
        Each dict contains `demo_topic` and `time`.
    """
    pass


@tool
def show_gallery_exhibits() -> List[str]:
    """
    List currently active gallery exhibits within the academy.

    Returns
    -------
    List[str]
        Titles of exhibitions.
    """
    pass


@tool
def get_material_stock() -> List[Dict[str, str]]:
    """
    Report remaining stock levels for common studio supplies.

    Returns
    -------
    List[Dict[str, str]]
        Each dict contains `item`, `quantity`, and `units`.
    """
    pass


@tool
def submit_portfolio_feedback() -> str:
    """
    Submit tutor feedback for the active student’s portfolio.

    Returns
    -------
    str
        Confirmation message upon successful submission.
    """
    pass


# Register all tools
all_functions = [
    search_lesson,
    check_basic_info,
    check_lesson_full_status,
    get_today_schedule,
    show_material_list,
    get_live_demo_schedule,
    show_gallery_exhibits,
    get_material_stock,
    submit_portfolio_feedback,
]

tool_functions_0009aug = {
    "function_registry": {
        f.name: {
            "name": f.name,
            "description": f.description,
            "args": f.args,
        }
        for f in all_functions
    }
}
