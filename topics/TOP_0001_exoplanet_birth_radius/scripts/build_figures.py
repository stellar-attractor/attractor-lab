from pathlib import Path

from lulab.io.loaders import load_topic_dataset
from lulab.viz.plots import plot_metallicity_gradient
from lulab.viz.export import save_figure


TOPIC_DIR = Path(__file__).resolve().parents[1]
OUT = TOPIC_DIR / "figures"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    df = load_topic_dataset(TOPIC_DIR)
    fig, ax = plot_metallicity_gradient(df)
    save_figure(fig, OUT / "FIG_001_metallicity_gradient", formats=("pdf", "png"))
    print("Saved FIG_001 to:", OUT)


if __name__ == "__main__":
    main()