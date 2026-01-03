"""
defaults.py
Shared defaults for Stellar Attractor matplotlib animations.

Extracted & normalized from ANIM_001_EN.ipynb:
- export settings (format, fps, dpi, codecs)
- theme handling (light/dark rcParams)
- project path discovery (topics/.../animations)
- save_animation() helper (MP4/GIF)

Usage in notebooks:
    from lulab.anim.defaults import apply_theme, save_animation, THEME
    from lulab.anim.plot_helpers import make_fig, set_common_axes

    apply_theme(THEME)
    out_base = OUT_DIR / "ANIM_age_feh_boulet"
    save_animation(ani, out_base)
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Literal, Dict

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FFMpegWriter, PillowWriter
# from lulab.io.theme import THEME, apply_theme, get_colors

# COLORS = get_colors(THEME)

# =================================================
# Animation export settings (defaults)
# =================================================
ANIM_FORMAT: Literal["mp4", "gif"] = "gif"   # switch
FPS: int = 24
DPI: int = 150

MP4_CODEC: str = "libx264"
MP4_BITRATE: int = 1800
# keep MP4 broadly compatible
MP4_EXTRA_ARGS = ["-pix_fmt", "yuv420p"]

GIF_WRITER: str = "pillow"
GIF_LOOP: int = 0  # 0 = infinite

# =================================================
# Theme settings
# =================================================
THEME: Literal["light", "dark"] = "dark"

# Optional palette (from notebook)
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
COLORS: Dict[str, str] = COLORS_DARK if THEME == "dark" else COLORS_LIGHT


def apply_theme(theme: Literal["light", "dark"] = "light") -> None:
    """
    Apply a consistent matplotlib theme (light/dark) similar to ANIM_001_EN defaults.
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
    elif theme == "dark":
        # Use dark_background as baseline, then override
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
    else:
        raise ValueError("THEME must be 'light' or 'dark'")


# =================================================
# Project path discovery (as in notebook)
# =================================================
def find_project_root(start: Optional[Path] = None) -> Path:
    """
    Walk up parents until a folder containing 'topics' is found.
    Falls back to current working directory if not found.
    """
    p = (start or Path.cwd()).resolve()
    for _ in range(30):
        if (p / "topics").exists():
            return p
        if p.parent == p:
            break
        p = p.parent
    return (start or Path.cwd()).resolve()


PROJECT_ROOT: Path = find_project_root()
TOPIC_ROOT: Path = PROJECT_ROOT / "topics" / "TOP_0001_exoplanet_birth_radius"
OUT_DIR: Path = TOPIC_ROOT / "animations"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def save_animation(anim, out_path_base: Path, *,
                   fmt: Optional[Literal["mp4", "gif"]] = None,
                   fps: int = FPS,
                   dpi: int = DPI,
                   mp4_codec: str = MP4_CODEC,
                   mp4_bitrate: int = MP4_BITRATE,
                   gif_loop: int = GIF_LOOP) -> Path:
    """
    Save a matplotlib animation as MP4 or GIF.

    Parameters
    ----------
    anim : matplotlib.animation.Animation
        The animation object (e.g., FuncAnimation).
    out_path_base : Path
        Output path without suffix (suffix is added based on format).
    fmt : {'mp4','gif'}, optional
        Overrides ANIM_FORMAT.
    fps, dpi : int
        Export parameters.
    mp4_codec, mp4_bitrate : str/int
        FFmpeg encoder settings.
    gif_loop : int
        GIF loop count. 0 = infinite.
    """
    out_path_base = Path(out_path_base)
    out_path_base.parent.mkdir(parents=True, exist_ok=True)

    fmt2 = (fmt or ANIM_FORMAT).lower()
    if fmt2 == "mp4":
        out_file = out_path_base.with_suffix(".mp4")
        print("Target:", out_file.resolve())
        writer = FFMpegWriter(
            fps=fps,
            codec=mp4_codec,
            bitrate=mp4_bitrate,
            extra_args=MP4_EXTRA_ARGS,
        )
        anim.save(out_file, writer=writer, dpi=dpi)
        print("Saved:", out_file.resolve(), "exists:", out_file.exists())
        return out_file

    if fmt2 == "gif":
        out_file = out_path_base.with_suffix(".gif")
        print("Target:", out_file.resolve())
        # loop isn't supported in some older matplotlibs
        try:
            writer = PillowWriter(fps=fps, loop=gif_loop)
        except TypeError:
            writer = PillowWriter(fps=fps)
        anim.save(out_file, writer=writer, dpi=dpi)
        print("Saved:", out_file.resolve(), "exists:", out_file.exists())
        return out_file

    raise ValueError("fmt/ANIM_FORMAT must be 'mp4' or 'gif'")


def print_env() -> None:
    """Convenience: show key defaults + matplotlib version."""
    print(f"matplotlib: {matplotlib.__version__}")
    print(f"Animation format: {ANIM_FORMAT} | FPS={FPS} | DPI={DPI}")
    print(f"Theme: {THEME}")
    print(f"Project root: {PROJECT_ROOT}")
    print(f"Topic root:   {TOPIC_ROOT}")
    print(f"Animations:   {OUT_DIR}")
