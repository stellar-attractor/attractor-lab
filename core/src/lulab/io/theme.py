# lulab/io/theme.py
from __future__ import annotations

from typing import Dict, Literal, Optional
import matplotlib.pyplot as plt

Theme = Literal["light", "dark"]

# Default theme (can be overridden per notebook)
THEME: Theme = "dark"

# Optional palette (project-level semantic colors)
COLORS_LIGHT: Dict[str, str] = {
    "toy": "#1f77b4",
    "minchev": "#d62728",
    "single": "#2ca02c",
    "host": "#ff7f0e",
}
COLORS_DARK: Dict[str, str] = {
    "toy": "#4cc9f0",
    "minchev": "#f72585",
    "single": "#7ae582",
    "host": "#ffb703",
}

def get_colors(theme: Optional[Theme] = None) -> Dict[str, str]:
    t = theme or THEME
    return COLORS_DARK if t == "dark" else COLORS_LIGHT


def apply_theme(theme: Theme = "light") -> None:
    """
    Apply a consistent matplotlib theme (light/dark) for both static plots and animations.
    """
    if theme == "light":
        plt.style.use("default")
        plt.rcParams.update({
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "axes.edgecolor": "black",
            "axes.labelcolor": "black",
            "text.color": "black",
            "xtick.color": "black",
            "ytick.color": "black",
            "grid.color": "#cccccc",
            "grid.alpha": 0.6,
            "legend.frameon": False,
        })
        return

    if theme == "dark":
        # baseline + overrides
        try:
            plt.style.use("dark_background")
        except Exception:
            pass
        plt.rcParams.update({
            "figure.facecolor": "#0b0d12",
            "axes.facecolor": "#0f1116",
            "axes.edgecolor": "#e0e0e0",
            "axes.labelcolor": "#e0e0e0",
            "text.color": "#e0e0e0",
            "xtick.color": "#e0e0e0",
            "ytick.color": "#e0e0e0",
            "grid.color": "#444444",
            "grid.alpha": 0.4,
            "legend.frameon": False,
        })
        return

    raise ValueError("theme must be 'light' or 'dark'")


def set_theme(theme: Theme) -> None:
    """
    Set global default THEME and apply it immediately.
    Useful for notebooks: set_theme('light') or set_theme('dark').
    """
    global THEME
    THEME = theme
    apply_theme(THEME)