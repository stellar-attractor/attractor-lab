from pathlib import Path
import matplotlib.pyplot as plt
from lulab.io.paths import get_topic_root

# --- figure output directory ---
topic_root = get_topic_root("TOP_0001_exoplanet_birth_radius")
FIG_DIR = topic_root / "figures/en"
FIG_DIR.mkdir(parents=True, exist_ok=True)

def save_fig(name, fig=None, dpi=200):
    """
    Save matplotlib figure into FIG_DIR with consistent naming.
    """
    if fig is None:
        fig = plt.gcf()
    out = FIG_DIR / f"{name}.png"
    fig.savefig(out, dpi=dpi, bbox_inches="tight")
    print(f"Saved figure: {out.resolve()}")