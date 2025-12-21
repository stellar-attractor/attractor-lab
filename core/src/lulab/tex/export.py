from __future__ import annotations

from pathlib import Path
import nbformat


def export_tex_snippets(
    notebook_path: Path,
    out_dir: Path,
    tag_prefix: str = "tex:",
) -> list[Path]:
    """
    Export cells tagged with `tex:<name>` into separate .tex snippet files.

    Example cell tag:  tex:birth_radius  -> out_dir/birth_radius.tex
    """
    notebook_path = Path(notebook_path)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    nb = nbformat.read(notebook_path, as_version=4)
    written: list[Path] = []

    for cell in nb.cells:
        tags = cell.get("metadata", {}).get("tags", []) or []
        tex_tags = [t for t in tags if isinstance(t, str) and t.startswith(tag_prefix)]
        if not tex_tags:
            continue

        name = tex_tags[0][len(tag_prefix):].strip()
        if not name:
            continue

        content = cell.get("source", "")
        if not content.strip():
            continue

        out_path = out_dir / f"{name}.tex"
        out_path.write_text(content.rstrip() + "\n", encoding="utf-8")
        written.append(out_path)

    return written