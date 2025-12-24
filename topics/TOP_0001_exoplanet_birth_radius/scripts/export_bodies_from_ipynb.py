from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Iterable

# =============================================================================
# CONFIG
# =============================================================================

TOPIC_DIR = Path(__file__).resolve().parents[1]
NB_DIR = TOPIC_DIR / "notebooks"
OUT_DIR = TOPIC_DIR / "tex" / "_tmp"

OUT_DIR.mkdir(parents=True, exist_ok=True)

# =============================================================================
# Unicode → LaTeX sanitization (for pdfLaTeX)
# =============================================================================

UNICODE_TO_LATEX = {
    # math / relations
    "≠": r"$\neq$",
    "≤": r"$\leq$",
    "≥": r"$\geq$",
    "≈": r"$\approx$",
    "≃": r"$\simeq$",
    "±": r"$\pm$",
    "×": r"$\times$",
    "·": r"$\cdot$",
    "→": r"$\rightarrow$",
    "←": r"$\leftarrow$",
    "↔": r"$\leftrightarrow$",

    # typography
    "—": r"---",
    "–": r"--",
    "…": r"\ldots{}",
    "“": r"``",
    "”": r"''",
    "„": r"``",
    "’": r"'",
    "‘": r"`",

    # rare subscripts
    "₍": r"$_{(}$",
    "₎": r"$_{)}$",

    # greek
    "α": r"$\alpha$",
    "β": r"$\beta$",
    "γ": r"$\gamma$",
    "δ": r"$\delta$",
    "ε": r"$\epsilon$",
    "λ": r"$\lambda$",
    "μ": r"$\mu$",
    "π": r"$\pi$",
    "σ": r"$\sigma$",
    "Ω": r"$\Omega$",

    # emoji
    "📌": r"\textbf{[NOTE]} ",
    "✅": r"\textbf{[OK]} ",
    "⚠️": r"\textbf{[WARN]} ",
    "❗": r"\textbf{[!]} ",
    "🔍": r"\textbf{[CHECK]} ",
    "💡": r"\textbf{[IDEA]} ",
    "👉": r"\(\rightarrow\) ",      # или просто "-> "
    "🌌": r"\textbf{[SPACE]} ",     # или "[COSMOS]"
    "☉": r"\(\odot\)",              # требует amsmath (у тебя он уже есть)

}

LATEX_SPECIALS = {
    "#": r"\#",
    "$": r"\$",
    "%": r"\%",
    "&": r"\&",
    "_": r"\_",
    "{": r"\{",
    "}": r"\}",
    "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
}

# detect math blocks and do not touch them
_MATH_RE = re.compile(r"(\$.*?\$|\\$begin:math:text$\.\+\?\\\\$end:math:text$|\\$begin:math:display$\.\+\?\\\\$end:math:display$)", re.DOTALL)


def sanitize_tex(text: str) -> str:
    """Make text safe for pdfLaTeX without destroying math."""
    parts: list[str] = []
    last = 0
    for m in _MATH_RE.finditer(text):
        parts.append(_sanitize_non_math(text[last:m.start()]))
        parts.append(m.group(0))  # keep math as-is
        last = m.end()
    parts.append(_sanitize_non_math(text[last:]))
    return "".join(parts)


def _sanitize_non_math(t: str) -> str:
    """
    Two-phase:
      1) Replace Unicode tokens with placeholders
      2) Escape LaTeX specials in the remaining text
      3) Restore placeholders as raw LaTeX (do NOT escape them)
    This prevents turning inserted '$...$' into '\$...\$'.
    """
    if not t:
        return t

    placeholders: dict[str, str] = {}
    # Use private sentinel pattern unlikely to appear
    for i, (u, latex) in enumerate(UNICODE_TO_LATEX.items()):
        ph = f"@@U2L{i}@@"
        if u in t:
            t = t.replace(u, ph)
            placeholders[ph] = latex

    # Escape LaTeX specials in the (placeholder-containing) text
    out_chars: list[str] = []
    for ch in t:
        out_chars.append(LATEX_SPECIALS.get(ch, ch))
    t = "".join(out_chars)

    # Restore placeholders (raw LaTeX)
    for ph, latex in placeholders.items():
        t = t.replace(ph, latex)

    return t


# =============================================================================
# Markdown → LaTeX (minimal, controlled)
# =============================================================================

def md_to_tex(md: str) -> str:
    """
    Very conservative Markdown → LaTeX conversion.
    We do NOT try to be Pandoc here — only what's needed.
    """
    lines = md.splitlines()
    out: list[str] = []

    for ln in lines:
        ln = ln.rstrip()

        # headers
        if ln.startswith("### "):
            out.append(r"\subsubsection*{" + sanitize_tex(ln[4:]) + "}")
            continue
        if ln.startswith("## "):
            out.append(r"\subsection*{" + sanitize_tex(ln[3:]) + "}")
            continue
        if ln.startswith("# "):
            out.append(r"\section*{" + sanitize_tex(ln[2:]) + "}")
            continue

        # inline styles (apply BEFORE sanitize)
        ln = re.sub(r"\*\*(.+?)\*\*", r"\\textbf{\1}", ln)
        ln = re.sub(r"\*(.+?)\*", r"\\emph{\1}", ln)

        out.append(sanitize_tex(ln))

    return "\n".join(out)


# =============================================================================
# Notebook processing
# =============================================================================

def iter_notebooks() -> Iterable[Path]:
    for nb in sorted(NB_DIR.glob("*.ipynb")):
        if nb.name.startswith("."):
            continue
        yield nb


def extract_markdown_cells(nb_path: Path) -> str:
    data = json.loads(nb_path.read_text(encoding="utf-8"))
    chunks: list[str] = []

    for cell in data.get("cells", []):
        if cell.get("cell_type") == "markdown":
            src = "".join(cell.get("source", []))
            chunks.append(md_to_tex(src))

    return "\n\n".join(chunks).strip() + "\n"


# =============================================================================
# Main
# =============================================================================

def main() -> None:
    exported = 0

    for nb in iter_notebooks():
        stem = nb.stem
        body_tex = extract_markdown_cells(nb)

        if not body_tex.strip():
            print(f"SKIP (no markdown): {nb.name}")
            continue

        out_path = OUT_DIR / f"{stem}_body.tex"
        out_path.write_text(body_tex, encoding="utf-8")

        print(f"OK: {out_path.name}")
        exported += 1

    print(f"\nExported bodies: {exported}")
    print("Location:", OUT_DIR)


if __name__ == "__main__":
    main()