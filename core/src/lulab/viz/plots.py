import matplotlib.pyplot as plt
import pandas as pd


def plot_feh_histogram(df: pd.DataFrame, bins: int = 30):
    feh_col = "[Fe/H]"
    if feh_col not in df.columns:
        raise KeyError(f"Column not found: {feh_col}")

    feh = pd.to_numeric(df[feh_col], errors="coerce").dropna()

    fig, ax = plt.subplots()
    ax.hist(feh, bins=bins)
    ax.set_xlabel("[Fe/H] (dex)")
    ax.set_ylabel("Count")
    ax.set_title("Host-star metallicity distribution ([Fe/H])")
    ax.grid(True, alpha=0.3)
    return fig, ax