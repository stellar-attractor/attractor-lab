from pathlib import Path

def repo_root() -> Path:
    """
    Return repository root assuming this file lives in core/src/lulab/utils/.
    Works when installed in editable mode from the repo.
    """
    return Path(__file__).resolve().parents[4]