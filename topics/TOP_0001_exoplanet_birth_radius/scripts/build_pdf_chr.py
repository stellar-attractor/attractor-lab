from __future__ import annotations

from pathlib import Path
import os
import subprocess
import sys

from lulab.tex.export import export_tex_snippets


TOPIC_DIR = Path(__file__).resolve().parents[1]
REPO_DIR = TOPIC_DIR.parents[1]  # TOPIC_DIR -> topics -> repo root

NB = TOPIC_DIR / "notebooks" / "CHR.ipynb"   # если писал в SANDBOX — поменяй здесь
SNIPPETS_DIR = TOPIC_DIR / "tex" / "snippets"
TEX_DIR = TOPIC_DIR / "tex"
BUILD_DIR = TOPIC_DIR / "build"


def run(cmd: list[str], cwd: Path | None = None, env: dict[str, str] | None = None) -> None:
    print("+", " ".join(map(str, cmd)))
    subprocess.run(cmd, cwd=str(cwd) if cwd else None, env=env, check=True)


def main() -> None:
    # 1) Export snippets from notebook -> tex/snippets/*.tex
    written = export_tex_snippets(NB, SNIPPETS_DIR)
    print(f"Exported snippets: {len(written)}")
    for p in written:
        try:
            print(" -", p.relative_to(TOPIC_DIR))
        except Exception:
            print(" -", p)

    BUILD_DIR.mkdir(parents=True, exist_ok=True)

    # 2) Make LaTeX see lulab/tex (where preamble.tex lives)
    core_tex = (REPO_DIR / "core" / "src" / "lulab" / "tex").resolve()
    if not (core_tex / "preamble.tex").exists():
        raise FileNotFoundError(f"preamble.tex not found at: {core_tex / 'preamble.tex'}")

    env = os.environ.copy()
    # trailing ":" keeps default TeX search paths
    env["TEXINPUTS"] = f"{core_tex}:{env.get('TEXINPUTS', '')}"

    print("Using TEXINPUTS:", env["TEXINPUTS"])

    # 3) Clean previous artifacts (optional but helps)
    for ext in ["aux", "log", "out", "toc", "fls", "fdb_latexmk"]:
        p = BUILD_DIR / f"CHR.{ext}"
        if p.exists():
            p.unlink()

    # 4) Build PDF (two passes for refs; harmless for simple docs)
    try:
        run(
            ["pdflatex", "-interaction=nonstopmode", "-halt-on-error",
             f"-output-directory={BUILD_DIR}", "CHR.tex"],
            cwd=TEX_DIR,
            env=env,
        )
        run(
            ["pdflatex", "-interaction=nonstopmode", "-halt-on-error",
             f"-output-directory={BUILD_DIR}", "CHR.tex"],
            cwd=TEX_DIR,
            env=env,
        )
    except subprocess.CalledProcessError:
        print("\nBuild failed. Check log:", BUILD_DIR / "CHR.log", file=sys.stderr)
        raise

    pdf = BUILD_DIR / "CHR.pdf"
    print("OK:", pdf)
    subprocess.run(["open", pdf])


if __name__ == "__main__":
    main()