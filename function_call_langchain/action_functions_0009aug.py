from langchain.tools import tool

# ────────────────────────────────
#  Zero-argument helpers
# ────────────────────────────────


@tool
def announce_break() -> None:
    """
    Announce a short break for everyone in the studio.

    Returns
    -------
    None
    """
    pass


@tool
def pause_lesson() -> None:
    """
    Temporarily pause the current lesson (e.g., to adjust lighting or stretch).

    Returns
    -------
    None
    """
    pass


@tool
def resume_lesson() -> None:
    """
    Resume a lesson that was previously paused.

    Returns
    -------
    None
    """
    pass


# ────────────────────────────────
#  Core lesson-flow actions
# ────────────────────────────────


@tool
def select_request_confirm(lesson_name: str) -> None:
    """
    Ask the student to confirm that they really wish to enroll in the given lesson.

    Parameters
    ----------
    lesson_name : str
        Exact title of the lesson to confirm (e.g., "Landscape Painting").

    Returns
    -------
    None
    """
    pass


@tool
def select(lesson_name: str) -> None:
    """
    Officially reserve the lesson slot for the student.

    Parameters
    ----------
    lesson_name : str
        Exact title of the lesson to reserve.

    Returns
    -------
    None
    """
    pass


@tool
def start(lesson_name: str) -> None:
    """
    Begin instruction for the specified lesson.

    Parameters
    ----------
    lesson_name : str
        Exact title of the lesson to start.

    Returns
    -------
    None
    """
    pass


# ────────────────────────────────
#  Demonstrations & feedback
# ────────────────────────────────


@tool
def give_demo(demo_topic: str, materials: str = "") -> None:
    """
    Deliver a live demonstration on a particular topic.

    Parameters
    ----------
    demo_topic : str
        Short title for the demo (e.g., "Capturing Skies").
    materials : str, optional
        Comma-separated list of key materials used in the demo
        (e.g., "Large flat brush, palette knife").  Default is an empty
        string, indicating no specific material list.

    Returns
    -------
    None
    """
    pass


@tool
def log_progress(notes: str) -> None:
    """
    Save brief progress notes for the current student.

    Parameters
    ----------
    notes : str
        Free-form text summarising the student’s progress.

    Returns
    -------
    None
    """
    pass


# ────────────────────────────────
#  Convenience helpers
# ────────────────────────────────


@tool
def show_material_list() -> None:
    """
    Display the recommended materials for the upcoming or active lesson.

    Returns
    -------
    None
    """
    pass


@tool
def get_today_schedule() -> None:
    """
    Show the full lesson timetable for the current day.

    Returns
    -------
    None
    """
    pass


# Register all tools
all_functions = [
    announce_break,
    pause_lesson,
    resume_lesson,
    select_request_confirm,
    select,
    start,
    give_demo,
    log_progress,
    show_material_list,
    get_today_schedule,
]

action_functions_0009aug = {
    "function_registry": {
        f.name: {
            "name": f.name,
            "description": f.description,
            "args": f.args,
        }
        for f in all_functions
    }
}
