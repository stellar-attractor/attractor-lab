from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd


def _num(s: pd.Series) -> pd.Series:
    return pd.to_numeric(s, errors="coerce")


def tr(lang: str, key: str) -> str:
    T = {
        "en": {
            "feh": "[Fe/H] (dex)",
            "count": "Count",
            "dist": "Distance (pc)",
            "teff": "Teff (K)",
            "logg": "log g",
            "mass": "Planet mass (Mj)",
            "radius": "Planet radius (R⊕)",
            "period": "Orbital period (days)",

            "title_feh_hist": "Host-star metallicity distribution ([Fe/H])",
            "title_feh_dist": "[Fe/H] vs distance (selection/bias check)",
            "title_feh_teff": "[Fe/H] vs Teff (host-star parameters)",
            "title_feh_logg": "[Fe/H] vs log g (host-star evolutionary stage)",
            "title_feh_mass": "[Fe/H] vs planet mass",
            "title_feh_radius": "[Fe/H] vs planet radius",
            "title_mass_vs_period": "Planet mass vs orbital period",
        },
        "ru": {
            "feh": "[Fe/H] (декс)",
            "count": "Число",
            "dist": "Расстояние (пк)",
            "teff": "Teff (K)",
            "logg": "log g",
            "mass": "Масса планеты (Mj)",
            "radius": "Радиус планеты (R⊕)",
            "period": "Период орбиты (сутки)",

            "title_feh_hist": "Распределение металличности звёзд-хостов ([Fe/H])",
            "title_feh_dist": "[Fe/H] vs расстояние (проверка селекции)",
            "title_feh_teff": "[Fe/H] vs Teff (параметры звёзд-хостов)",
            "title_feh_logg": "[Fe/H] vs log g (эволюционное состояние)",
            "title_feh_mass": "[Fe/H] vs масса планеты",
            "title_feh_radius": "[Fe/H] vs радиус планеты",
            "title_mass_vs_period": "Масса планеты vs период орбиты",
        },
    }
    d = T.get(lang, T["en"])
    return d.get(key, key)


def _require_cols(df: pd.DataFrame, cols: list[str]) -> None:
    missing = [c for c in cols if c not in df.columns]
    if missing:
        raise KeyError(f"Missing required columns: {missing}")


def _distance_pc(df: pd.DataFrame) -> pd.Series:
    # Prefer NEA distance; fallback to SWEET-Cat distance.
    if "sy_dist" in df.columns:
        s = _num(df["sy_dist"])
        if s.notna().any():
            return s
    if "Distance" in df.columns:
        return _num(df["Distance"])
    return pd.Series([pd.NA] * len(df))


def _planet_mass_mj(df: pd.DataFrame) -> pd.Series:
    # Prefer best mass if present and not empty
    if "pl_bmassj" in df.columns:
        mj = _num(df["pl_bmassj"])
        if mj.notna().any():
            return mj
    if "pl_massj" in df.columns:
        return _num(df["pl_massj"])
    return pd.Series([pd.NA] * len(df))


def plot_feh_histogram(df: pd.DataFrame, bins: int = 35, lang: str = "en"):
    _require_cols(df, ["[Fe/H]"])
    feh = _num(df["[Fe/H]"]).dropna()

    fig, ax = plt.subplots()
    ax.hist(feh, bins=bins)
    ax.set_xlabel(tr(lang, "feh"))
    ax.set_ylabel(tr(lang, "count"))
    ax.set_title(tr(lang, "title_feh_hist"))
    ax.grid(True, alpha=0.3)
    return fig, ax


def plot_feh_vs_distance(df: pd.DataFrame, lang: str = "en"):
    _require_cols(df, ["[Fe/H]"])
    feh = _num(df["[Fe/H]"])
    dist = _distance_pc(df)

    m = feh.notna() & dist.notna()

    fig, ax = plt.subplots()
    ax.scatter(dist[m], feh[m], s=10)
    ax.set_xlabel(tr(lang, "dist"))
    ax.set_ylabel(tr(lang, "feh"))
    ax.set_title(tr(lang, "title_feh_dist"))
    ax.grid(True, alpha=0.3)
    return fig, ax


def plot_feh_vs_teff(df: pd.DataFrame, lang: str = "en"):
    _require_cols(df, ["[Fe/H]", "Teff"])
    feh = _num(df["[Fe/H]"])
    teff = _num(df["Teff"])

    m = feh.notna() & teff.notna()

    fig, ax = plt.subplots()
    ax.scatter(teff[m], feh[m], s=10)
    ax.set_xlabel(tr(lang, "teff"))
    ax.set_ylabel(tr(lang, "feh"))
    ax.set_title(tr(lang, "title_feh_teff"))
    ax.grid(True, alpha=0.3)
    return fig, ax


def plot_feh_vs_logg(df: pd.DataFrame, lang: str = "en"):
    _require_cols(df, ["[Fe/H]", "Logg"])
    feh = _num(df["[Fe/H]"])
    logg = _num(df["Logg"])

    m = feh.notna() & logg.notna()

    fig, ax = plt.subplots()
    ax.scatter(logg[m], feh[m], s=10)
    ax.set_xlabel(tr(lang, "logg"))
    ax.set_ylabel(tr(lang, "feh"))
    ax.set_title(tr(lang, "title_feh_logg"))
    ax.grid(True, alpha=0.3)
    return fig, ax


def plot_feh_vs_planet_mass(df: pd.DataFrame, lang: str = "en"):
    _require_cols(df, ["[Fe/H]"])
    feh = _num(df["[Fe/H]"])
    mj = _planet_mass_mj(df)

    m = feh.notna() & mj.notna()

    fig, ax = plt.subplots()
    ax.scatter(mj[m], feh[m], s=10)
    ax.set_xlabel(tr(lang, "mass"))
    ax.set_ylabel(tr(lang, "feh"))
    ax.set_title(tr(lang, "title_feh_mass"))
    ax.grid(True, alpha=0.3)
    return fig, ax


def plot_feh_vs_planet_radius(df: pd.DataFrame, lang: str = "en"):
    _require_cols(df, ["[Fe/H]", "pl_rade"])
    feh = _num(df["[Fe/H]"])
    rade = _num(df["pl_rade"])

    m = feh.notna() & rade.notna()

    fig, ax = plt.subplots()
    ax.scatter(rade[m], feh[m], s=10)
    ax.set_xlabel(tr(lang, "radius"))
    ax.set_ylabel(tr(lang, "feh"))
    ax.set_title(tr(lang, "title_feh_radius"))
    ax.grid(True, alpha=0.3)
    return fig, ax


def plot_period_vs_mass(df: pd.DataFrame, lang: str = "en"):
    _require_cols(df, ["pl_orbper"])
    per = _num(df["pl_orbper"])
    mj = _planet_mass_mj(df)

    m = per.notna() & mj.notna()

    fig, ax = plt.subplots()
    ax.scatter(per[m], mj[m], s=10)
    ax.set_xlabel(tr(lang, "period"))
    ax.set_ylabel(tr(lang, "mass"))
    ax.set_title(tr(lang, "title_mass_vs_period"))
    ax.set_xscale("log")
    ax.grid(True, alpha=0.3)
    return fig, ax