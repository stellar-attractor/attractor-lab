from __future__ import annotations

from pathlib import Path


def save_figure(fig, outbase: Path, formats=("png",), dpi=200) -> list[Path]:
    """
    Save a Matplotlib figure to one or more formats.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
    outbase : Path
        Output path WITHOUT suffix, e.g. OUT / "FIG_001_name"
    formats : tuple
        File formats to save, e.g. ("pdf", "png")
    dpi : int
        DPI for raster formats
    """
    outbase = Path(outbase)
    outbase.parent.mkdir(parents=True, exist_ok=True)

    written: list[Path] = []
    for fmt in formats:
        p = outbase.with_suffix(f".{fmt}")
        fig.savefig(p, dpi=dpi, bbox_inches="tight")
        written.append(p)

    return written