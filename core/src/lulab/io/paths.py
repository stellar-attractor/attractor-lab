from __future__ import annotations

from pathlib import Path
from typing import Optional


# -----------------------------
# Core: project + topic roots
# -----------------------------
def find_project_root(marker: str = "topics", start: Optional[Path] = None) -> Path:
    """
    Walk upwards from `start` (or current working directory) until a folder
    containing `marker` is found.

    Returns
    -------
    Path
        Project root path (folder that contains `topics/`)

    Raises
    ------
    RuntimeError
        If marker folder is not found.
    """
    p = (Path.cwd() if start is None else Path(start)).resolve()
    while p != p.parent:
        if (p / marker).exists():
            return p
        p = p.parent

    raise RuntimeError(
        f"Could not locate project root (folder containing '{marker}'). "
        "Make sure you are inside the attractor-lab repository."
    )


def get_topic_root(topic_name: str, *, create: bool = False) -> Path:
    """
    Return full path to a topic directory.

    Example
    -------
    topic_root = get_topic_root('TOP_0001_exoplanet_birth_radius')
    """
    project_root = find_project_root()
    topic_root = project_root / "topics" / topic_name

    if create:
        topic_root.mkdir(parents=True, exist_ok=True)

    if not topic_root.exists():
        raise RuntimeError(f"Topic directory not found: {topic_root}")

    return topic_root


# -----------------------------
# Common subfolders inside topic
# -----------------------------
def figures_dir(topic_name: str, *, lang: str = "en", create: bool = True) -> Path:
    """
    Path to figures/<lang> inside a topic.
    """
    lang = (lang or "en").strip().lower()
    if lang not in {"en", "ru"}:
        raise ValueError("lang must be 'en' or 'ru'")
    p = get_topic_root(topic_name) / "figures" / lang
    if create:
        p.mkdir(parents=True, exist_ok=True)
    return p

def data_raw_dir(topic_name: str, *, create: bool = True) -> Path:
    """
    Path to data/raw inside a topic.
    """
    p = get_topic_root(topic_name) / "data" / "raw"
    if create:
        p.mkdir(parents=True, exist_ok=True)
    return p


def data_processed_dir(topic_name: str, *, create: bool = True) -> Path:
    """
    Path to data/processed inside a topic.
    """
    p = get_topic_root(topic_name) / "data" / "processed"
    if create:
        p.mkdir(parents=True, exist_ok=True)
    return p


def animations_dir(topic_name: str, *, create: bool = True) -> Path:
    """
    Path to animations inside a topic.
    """
    p = get_topic_root(topic_name) / "animations"
    if create:
        p.mkdir(parents=True, exist_ok=True)
    return p


# -----------------------------
# Backward-compatible aliases (optional, but nice)
# -----------------------------
def topic_root(topic_name: str, *, create: bool = False) -> Path:
    return get_topic_root(topic_name, create=create)

def fig_dir(topic_name: str, lang: str = "en", *, create: bool = True) -> Path:
    return figures_dir(topic_name, lang=lang, create=create)

def data_raw(topic_name: str, *, create: bool = True) -> Path:
    return data_raw_dir(topic_name, create=create)

def data_processed(topic_name: str, *, create: bool = True) -> Path:
    return data_processed_dir(topic_name, create=create)

def anim_dir(topic_name: str, *, create: bool = True) -> Path:
    return animations_dir(topic_name, create=create)