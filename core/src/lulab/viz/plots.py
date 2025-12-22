import matplotlib.pyplot as plt
import pandas as pd


def _num(s: pd.Series) -> pd.Series:
    return pd.to_numeric(s, errors="coerce")


def plot_feh_histogram(df: pd.DataFrame, bins: int = 35):
    feh = _num(df["[Fe/H]"]).dropna()
    fig, ax = plt.subplots()
    ax.hist(feh, bins=bins)
    ax.set_xlabel("[Fe/H] (dex)")
    ax.set_ylabel("Count")
    ax.set_title("Host-star metallicity distribution ([Fe/H])")
    ax.grid(True, alpha=0.3)
    return fig, ax


def plot_feh_vs_distance(df: pd.DataFrame):
    feh = _num(df["[Fe/H]"])
    dist = _num(df["sy_dist"]) if "sy_dist" in df.columns else _num(df["Distance"])
    m = feh.notna() & dist.notna()
    fig, ax = plt.subplots()
    ax.scatter(dist[m], feh[m], s=10)
    ax.set_xlabel("Distance (pc)")
    ax.set_ylabel("[Fe/H] (dex)")
    ax.set_title("[Fe/H] vs distance (selection/bias check)")
    ax.grid(True, alpha=0.3)
    return fig, ax


def plot_feh_vs_teff(df: pd.DataFrame):
    feh = _num(df["[Fe/H]"])
    teff = _num(df["Teff"])
    m = feh.notna() & teff.notna()
    fig, ax = plt.subplots()
    ax.scatter(teff[m], feh[m], s=10)
    ax.set_xlabel("Teff (K)")
    ax.set_ylabel("[Fe/H] (dex)")
    ax.set_title("[Fe/H] vs Teff (host-star parameters)")
    ax.grid(True, alpha=0.3)
    return fig, ax


def plot_feh_vs_logg(df: pd.DataFrame):
    feh = _num(df["[Fe/H]"])
    logg = _num(df["Logg"])
    m = feh.notna() & logg.notna()
    fig, ax = plt.subplots()
    ax.scatter(logg[m], feh[m], s=10)
    ax.set_xlabel("log g")
    ax.set_ylabel("[Fe/H] (dex)")
    ax.set_title("[Fe/H] vs log g (host-star evolutionary stage)")
    ax.grid(True, alpha=0.3)
    return fig, ax


def _planet_mass_mj(df: pd.DataFrame) -> pd.Series:
    if "pl_bmassj" in df.columns:
        mj = _num(df["pl_bmassj"])
        if mj.notna().any():
            return mj
    if "pl_massj" in df.columns:
        return _num(df["pl_massj"])
    return pd.Series([pd.NA] * len(df))


def plot_feh_vs_planet_mass(df: pd.DataFrame):
    feh = _num(df["[Fe/H]"])
    mj = _planet_mass_mj(df)
    m = feh.notna() & mj.notna()
    fig, ax = plt.subplots()
    ax.scatter(mj[m], feh[m], s=10)
    ax.set_xlabel("Planet mass (Mj)")
    ax.set_ylabel("[Fe/H] (dex)")
    ax.set_title("[Fe/H] vs planet mass")
    ax.grid(True, alpha=0.3)
    return fig, ax


def plot_feh_vs_planet_radius(df: pd.DataFrame):
    feh = _num(df["[Fe/H]"])
    rade = _num(df["pl_rade"]) if "pl_rade" in df.columns else pd.Series([pd.NA] * len(df))
    m = feh.notna() & rade.notna()
    fig, ax = plt.subplots()
    ax.scatter(rade[m], feh[m], s=10)
    ax.set_xlabel("Planet radius (R⊕)")
    ax.set_ylabel("[Fe/H] (dex)")
    ax.set_title("[Fe/H] vs planet radius")
    ax.grid(True, alpha=0.3)
    return fig, ax


def plot_period_vs_mass(df: pd.DataFrame):
    per = _num(df["pl_orbper"]) if "pl_orbper" in df.columns else pd.Series([pd.NA] * len(df))
    mj = _planet_mass_mj(df)
    m = per.notna() & mj.notna()
    fig, ax = plt.subplots()
    ax.scatter(per[m], mj[m], s=10)
    ax.set_xlabel("Orbital period (days)")
    ax.set_ylabel("Planet mass (Mj)")
    ax.set_title("Planet mass vs orbital period")
    ax.set_xscale("log")
    ax.grid(True, alpha=0.3)
    return fig, ax