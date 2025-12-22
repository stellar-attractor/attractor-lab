from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import nbformat


@dataclass(frozen=True)
class DocMeta:
    title: str
    author: str = "Attractor Lab"
    date: str = r"\today"
    preamble: str = "preamble_en.tex"


def _tags(cell) -> set[str]:
    md = cell.get("metadata", {}) or {}
    return set(md.get("tags", []) or [])


def export_tex_document_from_ipynb(
    ipynb_path: Path,
    out_tex_path: Path,
    meta: DocMeta,
) -> None:
    nb = nbformat.read(str(ipynb_path), as_version=4)

    body: list[str] = []

    for cell in nb.cells:
        tags = _tags(cell)

        # Explicit skip
        if "tex:skip" in tags:
            continue

        if cell.cell_type in ("markdown", "raw"):
            body.append(cell.source.rstrip() + "\n\n")

        elif cell.cell_type == "code" and "tex:code" in tags:
            code = cell.source.rstrip() + "\n"
            body.append("\\begin{verbatim}\n")
            body.append(code)
            body.append("\\end{verbatim}\n\n")

        # else: ignore code cells by default

    tex = [
        r"\documentclass[11pt]{article}",
        "",
        r"% AUTO-GENERATED FILE — DO NOT EDIT",
        r"% Source: " + ipynb_path.as_posix(),
        "",
        rf"\input{{{meta.preamble}}}",
        "",
        rf"\title{{{meta.title}}}",
        rf"\author{{{meta.author}}}",
        rf"\date{{{meta.date}}}",
        "",
        r"\begin{document}",
        r"\maketitle",
        "",
        "".join(body).rstrip(),
        "",
        r"\end{document}",
        "",
    ]

    out_tex_path.parent.mkdir(parents=True, exist_ok=True)
    out_tex_path.write_text("\n".join(tex), encoding="utf-8")

    print(f"Generated: {out_tex_path}")