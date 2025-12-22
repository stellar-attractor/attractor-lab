from pathlib import Path
import pandas as pd


def load_topic_dataset(topic_dir: Path) -> pd.DataFrame:
    topic_dir = Path(topic_dir)

    # prefer real processed dataset if present
    real_path = topic_dir / "data" / "processed" / "sample_planets_real.csv"
    if real_path.exists():
        return pd.read_csv(real_path, low_memory=False)

    # fallback: synthetic
    synth_path = topic_dir / "data" / "processed" / "sample_planets.csv"
    if synth_path.exists():
        return pd.read_csv(synth_path, low_memory=False)

    raise FileNotFoundError("No processed dataset found in data/processed/")