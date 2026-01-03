# lulab/io/save_figure.py
from __future__ import annotations

from pathlib import Path
from typing import Optional

import matplotlib.pyplot as plt

from lulab.io.paths import figures_dir
from lulab.io.theme import THEME


def save_fig(
    name: str,
    *,
    topic: str,
    lang: str = "en",
    fig=None,
    dpi: int = 200,
    transparent: bool = False,
) -> Path:
    """
    Save a matplotlib figure into figures/<lang>/ of a given topic,
    respecting the active light/dark theme.

    Parameters
    ----------
    name : str
        Figure base name (without extension).
    topic : str
        Topic ID, e.g. 'TOP_0001_exoplanet_birth_radius'.
    lang : {'en','ru'}
        Language subfolder.
    fig : matplotlib.figure.Figure, optional
        Figure to save (defaults to current figure).
    dpi : int
        Output DPI.
    transparent : bool
        Force transparent background (overrides theme).

    Returns
    -------
    Path
        Path to saved figure.
    """
    if fig is None:
        fig = plt.gcf()

    out_dir = figures_dir(topic, lang=lang, create=True)
    out_path = out_dir / f"{name}.png"

    # Respect theme background unless explicitly transparent
    facecolor = (
        "none"
        if transparent
        else plt.rcParams.get("figure.facecolor", "white")
    )

    fig.savefig(
        out_path,
        dpi=dpi,
        bbox_inches="tight",
        facecolor=facecolor,
    )

    print(f"Saved figure: {out_path.resolve()}")
    return out_path