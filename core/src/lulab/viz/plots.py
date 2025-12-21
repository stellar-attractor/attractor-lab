import matplotlib.pyplot as plt


def plot_metallicity_gradient(df):
    """
    Simple metallicity vs galactocentric radius plot.
    Expects columns: r_kpc, feh, n_planets (optional).
    """
    fig, ax = plt.subplots()
    ax.plot(df["r_kpc"], df["feh"], marker="o")
    ax.set_xlabel("Galactocentric radius, r (kpc)")
    ax.set_ylabel("[Fe/H] (dex)")
    ax.set_title("Synthetic metallicity gradient (pipeline test)")
    ax.grid(True, alpha=0.3)
    return fig, ax