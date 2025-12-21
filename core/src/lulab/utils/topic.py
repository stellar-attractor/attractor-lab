from pathlib import Path


def get_topic_dir(start: Path | None = None) -> Path:
    """
    Return the topic directory (TOP_XXXX_*) starting from `start`
    or current working directory.

    A topic directory is identified by:
    - name starting with 'TOP_'
    - presence of 'meta/' directory
    """
    p = (start or Path.cwd()).resolve()

    for candidate in [p, *p.parents]:
        if candidate.name.startswith("TOP_") and (candidate / "meta").exists():
            return candidate

    raise RuntimeError(
        f"Could not locate topic directory starting from {p}"
    )


def topic_paths(topic_dir: Path) -> dict[str, Path]:
    """
    Return canonical paths inside a topic directory.
    """
    return {
        "topic": topic_dir,
        "meta": topic_dir / "meta",
        "sources": topic_dir / "sources",
        "data_raw": topic_dir / "data" / "raw",
        "data_interim": topic_dir / "data" / "interim",
        "data_processed": topic_dir / "data" / "processed",
        "notebooks": topic_dir / "notebooks",
        "scripts": topic_dir / "scripts",
        "figures": topic_dir / "figures",
        "tables": topic_dir / "tables",
        "tex": topic_dir / "tex",
    }