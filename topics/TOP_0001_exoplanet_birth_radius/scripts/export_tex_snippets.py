from __future__ import annotations

from pathlib import Path

from lulab.tex.export_snippets import export_snippets


TOPIC_DIR = Path(__file__).resolve().parents[1]
NOTEBOOKS_DIR = TOPIC_DIR / "notebooks"
OUT_DIR = TOPIC_DIR / "tex" / "snippets"


def main() -> None:
    # One-direction pipeline: ipynb -> tex/snippets/*.tex
    notebooks = [
        NOTEBOOKS_DIR / "CHR_EN.ipynb",
        NOTEBOOKS_DIR / "CHR_RU.ipynb",
    ]

    exported = export_snippets(notebooks, OUT_DIR)

    print(f"Exported snippets: {len(exported)}")
    for s in exported:
        rel = s.out_path.relative_to(TOPIC_DIR)
        print(f" - {rel}  (from {s.source_notebook.name} cell #{s.cell_index}: tex:snippet={s.name})")


if __name__ == "__main__":
    main()