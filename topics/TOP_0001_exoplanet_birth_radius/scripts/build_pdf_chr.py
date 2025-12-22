from __future__ import annotations

import subprocess
from pathlib import Path


TOPIC_DIR = Path(__file__).resolve().parents[1]
TEX_DIR = TOPIC_DIR / "tex"
BUILD_DIR = TOPIC_DIR / "build"


def run(cmd: list[str], cwd: Path) -> None:
    print("+", " ".join(cmd))
    subprocess.run(cmd, cwd=str(cwd), check=True)


def build_one(tex_filename: str) -> Path:
    BUILD_DIR.mkdir(parents=True, exist_ok=True)

    cmd = [
        "latexmk",
        "-pdf",
        "-interaction=nonstopmode",
        "-halt-on-error",
        f"-outdir={BUILD_DIR}",
        tex_filename,
    ]
    run(cmd, cwd=TEX_DIR)

    return BUILD_DIR / tex_filename.replace(".tex", ".pdf")


def main() -> None:
    # Expected entrypoints
    targets = ["CHR_RU.tex", "CHR_EN.tex"]

    # sanity checks
    for t in targets:
        p = TEX_DIR / t
        if not p.exists():
            raise FileNotFoundError(
                f"Missing TeX entrypoint: {p}\n"
                f"Create it in {TEX_DIR} and ensure it inputs preamble_ru.tex/preamble_en.tex."
            )

    built = []
    for t in targets:
        built.append(build_one(t))

    print("\nBuilt PDFs:")
    for p in built:
        print(" -", p)


if __name__ == "__main__":
    main()