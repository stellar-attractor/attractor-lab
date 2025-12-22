from __future__ import annotations

import subprocess
from pathlib import Path

TOPIC_DIR = Path(__file__).resolve().parents[1]
NB_DIR = TOPIC_DIR / "notebooks"
TEX_DIR = TOPIC_DIR / "tex"
TMP_DIR = TOPIC_DIR / "_tmp"
BUILD_DIR = TOPIC_DIR / "build"

NB_RU = NB_DIR / "CHR_RU.ipynb"
NB_EN = NB_DIR / "CHR_EN.ipynb"

MD_RU = TMP_DIR / "CHR_RU.md"
MD_EN = TMP_DIR / "CHR_EN.md"
BODY_RU = TMP_DIR / "CHR_RU_body.tex"
BODY_EN = TMP_DIR / "CHR_EN_body.tex"

TPL_RU = TEX_DIR / "CHR_RU.tpl.tex"
TPL_EN = TEX_DIR / "CHR_EN.tpl.tex"


def run(cmd: list[str], cwd: Path | None = None, env: dict | None = None) -> None:
    print("+", " ".join(cmd))
    subprocess.run(cmd, cwd=str(cwd) if cwd else None, env=env, check=True)


def ipynb_to_md(ipynb: Path, md_out: Path) -> None:
    # используем ваш существующий конвертер
    from lulab.tex.ipynb_to_md import ipynb_to_markdown
    ipynb_to_markdown(ipynb, md_out)


def md_to_tex(md_in: Path, tex_out: Path) -> None:
    # pandoc должен быть установлен
    run([
        "pandoc",
        str(md_in),
        "-f", "markdown+tex_math_dollars+tex_math_single_backslash",
        "-t", "latex",
        "-o", str(tex_out),
    ])


def build_pdf(tpl_tex: Path, jobname: str) -> None:
    BUILD_DIR.mkdir(parents=True, exist_ok=True)

    # TEXINPUTS: добавляем папку tex/ (где preamble_*.tex) и core/src/lulab/tex (если надо)
    env = dict(**subprocess.os.environ)
    env["TEXINPUTS"] = f"{TEX_DIR}:{env.get('TEXINPUTS','')}"  # чтобы \input{preamble_ru.tex} находился

    run([
        "latexmk",
        "-pdf",
        "-interaction=nonstopmode",
        "-halt-on-error",
        f"-outdir={BUILD_DIR}",
        f"-jobname={jobname}",
        str(tpl_tex),
    ], cwd=tpl_tex.parent, env=env)


def main() -> None:
    TMP_DIR.mkdir(parents=True, exist_ok=True)

    # 1) ipynb -> md
    ipynb_to_md(NB_RU, MD_RU)
    ipynb_to_md(NB_EN, MD_EN)

    # 2) md -> tex body
    md_to_tex(MD_RU, BODY_RU)
    md_to_tex(MD_EN, BODY_EN)

    # 3) pdf from templates (templates are NEVER modified)
    build_pdf(TPL_RU, "CHR_RU")
    build_pdf(TPL_EN, "CHR_EN")

    print("Done.")
    print("RU:", BUILD_DIR / "CHR_RU.pdf")
    print("EN:", BUILD_DIR / "CHR_EN.pdf")


if __name__ == "__main__":
    main()