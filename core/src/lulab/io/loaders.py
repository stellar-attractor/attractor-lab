from pathlib import Path
import pandas as pd


def load_topic_dataset(topic_dir: Path, filename: str = "sample_planets.csv") -> pd.DataFrame:
    """
    Load a processed dataset for a topic.
    """
    topic_dir = Path(topic_dir)
    path = topic_dir / "data" / "processed" / filename
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")
    return pd.read_csv(path)