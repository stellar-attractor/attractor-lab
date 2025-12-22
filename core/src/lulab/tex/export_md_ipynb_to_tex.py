from __future__ import annotations

import subprocess
from pathlib import Path


def export_ipynb_to_tex(
    ipynb: Path,
    tex_out: Path,
    preamble: Path,
    title: str,
    author: str = "Attractor Lab",
):
    tex_out.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        "pandoc",
        str(ipynb),
        "-f", "ipynb",
        "-t", "latex",
        "--standalone",
        f"--include-in-header={preamble}",
        f"--metadata=title:{title}",
        f"--metadata=author:{author}",
        "-o", str(tex_out),
    ]

    print("+", " ".join(cmd))
    subprocess.run(cmd, check=True)