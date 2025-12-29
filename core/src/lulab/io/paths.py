from pathlib import Path


def find_project_root(marker="topics") -> Path:
    """
    Walk upwards from current working directory until a folder
    containing `marker` is found.

    Returns
    -------
    Path
        Project root path (parent of `topics`)

    Raises
    ------
    RuntimeError
        If marker folder is not found.
    """
    p = Path.cwd().resolve()
    while p != p.parent:
        if (p / marker).exists():
            return p
        p = p.parent

    raise RuntimeError(
        f"Could not locate project root (folder containing '{marker}'). "
        "Make sure you are inside the attractor-lab repository."
    )


def get_topic_root(topic_name: str) -> Path:
    """
    Return full path to a topic directory.

    Example
    -------
    topic_root = get_topic_root("TOP_0001_exoplanet_birth_radius")
    """
    project_root = find_project_root()
    topic_root = project_root / "topics" / topic_name

    if not topic_root.exists():
        raise RuntimeError(f"Topic directory not found: {topic_root}")

    return topic_root