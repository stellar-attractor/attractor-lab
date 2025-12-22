from pathlib import Path

from lulab.io.loaders import load_topic_dataset
from lulab.viz.export import save_figure
from lulab.viz import plots


TOPIC_DIR = Path(__file__).resolve().parents[1]
OUT = TOPIC_DIR / "figures"


def build_set(df, lang: str):
    out_lang = OUT / lang
    out_lang.mkdir(parents=True, exist_ok=True)

    plan = [
        ("FIG_001_feh_histogram", plots.plot_feh_histogram),
        ("FIG_002_feh_vs_distance", plots.plot_feh_vs_distance),
        ("FIG_003_feh_vs_teff", plots.plot_feh_vs_teff),
        ("FIG_004_feh_vs_logg", plots.plot_feh_vs_logg),
        ("FIG_005_feh_vs_planet_mass", plots.plot_feh_vs_planet_mass),
        ("FIG_006_feh_vs_planet_radius", plots.plot_feh_vs_planet_radius),
        ("FIG_007_period_vs_mass", plots.plot_period_vs_mass),
    ]

    for name, fn in plan:
        fig, ax = fn(df, lang=lang)
        save_figure(fig, out_lang / name, formats=("pdf", "png"))
        print(f"Saved [{lang}]: {name}")


def main():
    df = load_topic_dataset(TOPIC_DIR)
    build_set(df, "ru")
    build_set(df, "en")
    print("Done. Figures in:", OUT)


if __name__ == "__main__":
    main()