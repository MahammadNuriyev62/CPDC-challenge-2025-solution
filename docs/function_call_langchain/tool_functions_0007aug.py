from typing import List, Dict
from langchain.tools import tool


@tool
def search_lesson(
    lesson_name: str,
    lesson_level: str,
    lesson_duration: str,
    lesson_reward: str,
    lesson_description: str,
    lesson_name_operator: str,
    lesson_level_operator: str,
    lesson_duration_operator: str,
    lesson_reward_operator: str,
) -> List[Dict[str, str]]:
    """
    Search for lessons based on specified criteria, such as level (e.g. Beginner, Intermediate, Advanced), duration (e.g. 2 hours, 3 days, etc.), reward (e.g. Certificate, Portfolio Piece, etc.), and specific features (e.g. sketching, painting techniques, art history, etc.). Returns a list of lesson names along with the reasons for the selection. Returns 'many' when there are multiple applicable items, and 'n/a' when there are none.

    Parameters:
    ----------
    lesson_name: str
        Specified lesson name (e.g. Figure Drawing, Still Life Sketching, Color Theory Basics, etc.). Uses the lesson name mentioned in the conversation. Multiple lessons can be set (e.g. Figure Drawing|Still Life Sketching).

    lesson_level: str
        Specified lesson level (e.g. Beginner, Intermediate, Advanced). Multiple levels can be set (e.g. Beginner|Intermediate).

    lesson_duration: str
        Specified lesson duration (e.g. 2 hours, 3 Days, etc.). Uses the duration(days) of the lesson mentioned in the conversation.

    lesson_reward: str
        Specified lesson reward (e.g. Certificate, Portfolio Piece, etc.). Uses the reward of the lesson mentioned in the conversation.

    lesson_description: str
        Specified lesson characteristics (e.g. sketching, painting techniques, art history, etc.). Uses the characteristics of the lesson mentioned in the conversation.

    lesson_name_operator: str
        Exclusion modifier used with the lesson name specified by lesson_name. Uses 'other than' as the modifier.

    lesson_level_operator: str
        Modifier for comparison and exclusion used to describe the level of the lesson specified by lesson_level. The modifier can be one of the following: or above, or below, more than, less than, most difficult, difficult, average, easy, simplest, other than.

    lesson_duration_operator: str
        Modifier for comparison used to describe the duration of the lesson specified by lesson_duration. The modifier can be one of the following: or more, or less, more than, less than, about, longest, long, average, short, shortest.

    lesson_reward_operator: str
        Modifier for comparison to describe the reward of the lesson specified by lesson_reward. The modifier can be one of the following: or more, or less, more than, less than, about, highest, high, average, low, lowest

    Returns:
    -------
    List[Dict[str, str]]
        A list of lesson names along with the reasons for the selection.
    """

    pass


@tool
def check_basic_info(lesson_name: str) -> List[Dict[str, str]]:
    """
    Check the level, duration, reward, and basic information of a specified lesson (e.g. Figure Drawing, Still Life Sketching, Color Theory Basics, etc.).

    Parameters:
    ----------
    lesson_name : str
        Specified lesson name (e.g. Figure Drawing, Still Life Sketching, Color Theory Basics, etc.). Uses the lesson name mentioned in the conversation.

    Returns:
    -------
    List[Dict[str, str]]
        Outputs the level, duration, reward, and basic information of a specified lesson (e.g. Figure Drawing, Still Life Sketching, Color Theory Basics, etc.).
    """

    pass


@tool
def check_level(lesson_name: str) -> List[Dict[str, str]]:
    """
    Check the level of a specified lesson (e.g. Figure Drawing, Still Life Sketching, Color Theory Basics, etc.).

    Parameters:
    ----------
    lesson_name : str
        Specified lesson name (e.g. Figure Drawing, Still Life Sketching, Color Theory Basics, etc.). Uses the lesson name mentioned in the conversation.

    Returns:
    -------
    List[Dict[str, str]]
        Outputs the level of a specified lesson (e.g. Figure Drawing, Still Life Sketching, Color Theory Basics, etc.).
    """

    pass


@tool
def check_duration(lesson_name: str) -> List[Dict[str, str]]:
    """
    Check the duration (hours) of a specified lesson (e.g. Figure Drawing, Still Life Sketching, Color Theory Basics, etc.).

    Parameters:
    ----------
    lesson_name : str
        Specified lesson name (e.g. Figure Drawing, Still Life Sketching, Color Theory Basics, etc.). Uses the lesson name mentioned in the conversation.

    Returns:
    -------
    List[Dict[str, str]]
        Outputs the duration (hours) of a specified lesson (e.g. Figure Drawing, Still Life Sketching, Color Theory Basics, etc.).
    """

    pass


@tool
def check_reward(lesson_name: str) -> List[Dict[str, str]]:
    """
    Check the reward of a specified lesson (e.g. Figure Drawing, Still Life Sketching, Color Theory Basics, etc.).

    Parameters:
    ----------
    lesson_name : str
        Specified lesson name (e.g. Figure Drawing, Still Life Sketching, Color Theory Basics, etc.). Uses the lesson name mentioned in the conversation.

    Returns:
    -------
    List[Dict[str, str]]
        Outputs the reward of a specified lesson (e.g. Figure Drawing, Still Life Sketching, Color Theory Basics, etc.).
    """

    pass


@tool
def check_description(lesson_name: str) -> List[Dict[str, str]]:
    """
    Check the basic information and additional detailed information of the specified lesson (e.g. Figure Drawing, Still Life Sketching, Color Theory Basics, etc.).

    Parameters:
    ----------
    lesson_name : str
        Specified lesson name (e.g. Figure Drawing, Still Life Sketching, Color Theory Basics, etc.). Uses the lesson name mentioned in the conversation.

    Returns:
    -------
    List[Dict[str, str]]
        Outputs  the basic information and additional detailed information of the specified lesson (e.g. Figure Drawing, Still Life Sketching, Color Theory Basics, etc.).
    """

    pass


all_functions = [
    search_lesson,
    check_basic_info,
    check_level,
    check_duration,
    check_reward,
    check_description,
]
tool_functions_0007aug = {
    "function_registry": {
        f.name: {"name": f.name, "description": f.description, "args": f.args}
        for f in all_functions
    }
}
