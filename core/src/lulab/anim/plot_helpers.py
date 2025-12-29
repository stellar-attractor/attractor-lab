"""
plot_helpers.py
Common plotting helpers for Stellar Attractor animations.

Depends on anim_defaults.py for theme and paths.
Provides:
- make_fig / make_ax
- common axis formatting
- scatter factory
- median curve helper
"""

from __future__ import annotations
from typing import Tuple, Iterable, Optional
import numpy as np
import matplotlib.pyplot as plt

# -------------------------
# Figure / Axes factories
# -------------------------
def make_fig(figsize=(5.6, 4.8), grid_alpha=0.2):
    fig, ax = plt.subplots(figsize=figsize)
    ax.grid(alpha=grid_alpha)
    return fig, ax

def set_common_axes(ax,
                    xlim: Optional[Tuple[float, float]] = None,
                    ylim: Optional[Tuple[float, float]] = None,
                    xlabel: Optional[str] = None,
                    ylabel: Optional[str] = None,
                    title: Optional[str] = None,
                    yticks: Optional[Iterable[float]] = None):
    if xlim is not None:
        ax.set_xlim(*xlim)
    if ylim is not None:
        ax.set_ylim(*ylim)
    if xlabel is not None:
        ax.set_xlabel(xlabel)
    if ylabel is not None:
        ax.set_ylabel(ylabel)
    if title is not None:
        ax.set_title(title)
    if yticks is not None:
        ax.set_yticks(list(yticks))

# -------------------------
# Scatter helpers
# -------------------------
def make_scatter(ax, size=3, alpha=0.15, linewidths=0):
    sc = ax.scatter([], [], s=size, alpha=alpha, linewidths=linewidths)
    return sc

def update_scatter(sc, x, y):
    sc.set_offsets(np.column_stack([x, y]))
    return sc

# -------------------------
# Statistics helpers
# -------------------------
def binned_median(x: np.ndarray, y: np.ndarray,
                  bins: np.ndarray,
                  min_count: int = 200):
    """Return (x_mid, y_median) for bins with at least min_count."""
    x = np.asarray(x); y = np.asarray(y)
    idx = np.digitize(x, bins) - 1
    xm, ym = [], []
    for i in range(len(bins)-1):
        sel = idx == i
        if sel.sum() < min_count:
            continue
        xm.append(0.5*(bins[i] + bins[i+1]))
        ym.append(np.nanmedian(y[sel]))
    return np.array(xm), np.array(ym)

# -------------------------
# Text overlay helper
# -------------------------
def make_corner_text(ax, loc=(0.02, 0.98), ha="left", va="top"):
    return ax.text(loc[0], loc[1], "", transform=ax.transAxes, ha=ha, va=va)
