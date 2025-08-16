from typing import List, Dict
from langchain.tools import tool


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
    Search for lessons based on specified criteria.
    All parameters are optional. If none are provided, returns all lessons.
    Returns:
    -------
    List[Dict[str, str]]
    """
    pass


@tool
def check_basic_info(lesson_name: str) -> List[Dict[str, str]]:
    """
    Check the level, duration, reward, and basic info of a specified lesson.
    """
    pass


@tool
def show_material_list() -> List[str]:
    """
    Show a list of materials recommended for the current lesson.
    Returns:
    -------
    List[str]
    """
    pass


@tool
def get_today_schedule() -> List[Dict[str, str]]:
    """
    Display today’s lesson schedule for the academy.
    Returns:
    -------
    List[Dict[str, str]]
    """
    pass


@tool
def submit_portfolio_feedback() -> str:
    """
    Submit tutor feedback for the current student's portfolio, if available in context.
    Returns a short confirmation string.
    """
    pass


@tool
def check_lesson_full_status(lesson_name: str) -> bool:
    """
    Check if a specific lesson is currently full.
    Returns True if full, False otherwise.
    """
    pass


all_functions = [
    search_lesson,
    check_basic_info,
    show_material_list,
    get_today_schedule,
    submit_portfolio_feedback,
    check_lesson_full_status,
]
tool_functions_0008aug = {
    "function_registry": {
        f.name: {"name": f.name, "description": f.description, "args": f.args}
        for f in all_functions
    }
}
