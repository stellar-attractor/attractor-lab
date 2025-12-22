from __future__ import annotations

from pathlib import Path
import nbformat


def _tags(cell) -> set[str]:
    md = cell.get("metadata", {}) or {}
    return set(md.get("tags", []) or [])


def _preview(text: str, n: int = 80) -> str:
    t = (text or "").strip().replace("\n", " ")
    return (t[:n] + "…") if len(t) > n else t


def ipynb_to_markdown(ipynb_path: Path, md_out: Path) -> None:
    """
    Loose mode:
      - exports all markdown/raw cells in order
      - skips any cell tagged 'tex:skip'
      - ignores code cells by default
      - if a code cell is tagged 'tex:code', exports it as fenced code block
    Additionally prints a diagnostic summary of what was exported/skipped.
    """
    nb = nbformat.read(str(ipynb_path), as_version=4)

    chunks: list[str] = []

    exported_md = 0
    exported_raw = 0
    exported_code = 0
    skipped_by_tag = 0
    ignored_code = 0
    ignored_other = 0

    skipped_cells_info = []
    ignored_code_info = []

    for idx, cell in enumerate(nb.cells):
        tags = _tags(cell)

        if "tex:skip" in tags:
            skipped_by_tag += 1
            skipped_cells_info.append(
                (idx, cell.cell_type, sorted(tags), _preview(cell.source))
            )
            continue

        if cell.cell_type == "markdown":
            txt = cell.source.rstrip()
            if txt:
                chunks.append(txt)
            chunks.append("")
            exported_md += 1

        elif cell.cell_type == "raw":
            txt = cell.source.rstrip()
            if txt:
                chunks.append(txt)
            chunks.append("")
            exported_raw += 1

        elif cell.cell_type == "code":
            if "tex:code" in tags:
                code = cell.source.rstrip("\n")
                chunks.append("```python")
                chunks.append(code)
                chunks.append("```")
                chunks.append("")
                exported_code += 1
            else:
                ignored_code += 1
                ignored_code_info.append(
                    (idx, cell.cell_type, sorted(tags), _preview(cell.source))
                )

        else:
            ignored_other += 1

    md_out.parent.mkdir(parents=True, exist_ok=True)
    md_out.write_text("\n".join(chunks).rstrip() + "\n", encoding="utf-8")

    print(f"MD exported: {md_out}")
    print("---- ipynb_to_md diagnostics ----")
    print(f"Notebook: {ipynb_path}")
    print(f"Exported: markdown={exported_md}, raw={exported_raw}, code(tex:code)={exported_code}")
    print(f"Skipped:  tex:skip={skipped_by_tag}")
    print(f"Ignored:  code(without tex:code)={ignored_code}, other={ignored_other}")

    if skipped_cells_info:
        print("\nSkipped cells (tex:skip):")
        for idx, ctype, tags, prev in skipped_cells_info[:20]:
            print(f" - #{idx:03d} [{ctype}] tags={tags} :: {prev}")

    # This is likely your RU problem:
    if ignored_code_info:
        print("\nIgnored code cells (no tex:code tag):")
        for idx, ctype, tags, prev in ignored_code_info[:20]:
            print(f" - #{idx:03d} [{ctype}] tags={tags} :: {prev}")