from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import nbformat


TAG_RE = re.compile(r"^tex:snippet=(.+)$")


@dataclass(frozen=True)
class ExportedSnippet:
    name: str
    out_path: Path
    source_notebook: Path
    cell_index: int


def _cell_tags(cell) -> list[str]:
    md = cell.get("metadata", {}) or {}
    tags = md.get("tags", []) or []
    return list(tags)


def _snippet_name_from_tags(tags: Iterable[str]) -> str | None:
    for t in tags:
        m = TAG_RE.match(t.strip())
        if m:
            return m.group(1).strip()
    return None


def export_snippets_from_notebook(ipynb_path: Path, out_dir: Path) -> list[ExportedSnippet]:
    nb = nbformat.read(str(ipynb_path), as_version=4)

    out_dir.mkdir(parents=True, exist_ok=True)
    exported: list[ExportedSnippet] = []

    for i, cell in enumerate(nb.cells):
        name = _snippet_name_from_tags(_cell_tags(cell))
        if not name:
            continue

        # We treat markdown and raw as TeX text; code cells are ignored for TeX snippets by default.
        if cell.cell_type not in ("markdown", "raw"):
            continue

        content = cell.source
        if not content.endswith("\n"):
            content += "\n"

        out_path = out_dir / f"{name}.tex"
        out_path.write_text(content, encoding="utf-8")

        exported.append(ExportedSnippet(name=name, out_path=out_path, source_notebook=ipynb_path, cell_index=i))

    return exported


def export_snippets(notebooks: list[Path], out_dir: Path) -> list[ExportedSnippet]:
    all_exported: list[ExportedSnippet] = []
    for nb in notebooks:
        if not nb.exists():
            raise FileNotFoundError(f"Notebook not found: {nb}")
        all_exported.extend(export_snippets_from_notebook(nb, out_dir))
    return all_exported