# lulab/i18n/plot_text.py
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Literal, Optional

import matplotlib as mpl

try:
    import yaml  # PyYAML
except Exception:  # pragma: no cover
    yaml = None  # type: ignore[assignment]


Lang = Literal["en", "ru"]


# ---------------------------------------------------------------------
# Internal mutable state (kept intentionally simple for notebook use)
# ---------------------------------------------------------------------
_STATE: Dict[str, Any] = {
    "lang": "en",
    "notebook": None,  # e.g. "ACAP_001"
    "labels": {},      # loaded from topic/i18n/labels.yaml
    "titles": {},      # loaded from topic/i18n/titles.yaml
    "loaded_from": None,  # path for debugging
}


# ---------------------------------------------------------------------
# Public API: language + notebook namespace
# ---------------------------------------------------------------------
def set_lang(lang: Lang) -> None:
    """
    Set current language for plot labels/titles.

    Notes
    -----
    - If 'ru', we also configure Cyrillic-capable fonts.
    """
    lang2 = (lang or "en").strip().lower()
    if lang2 not in ("en", "ru"):
        raise ValueError("lang must be 'en' or 'ru'")
    _STATE["lang"] = lang2

    if lang2 == "ru":
        configure_cyrillic_fonts()


def get_lang() -> Lang:
    return _STATE["lang"]  # type: ignore[return-value]


def set_notebook(notebook_id: Optional[str]) -> None:
    """
    Set current notebook namespace, e.g. 'ACAP_001'.

    This is used to resolve keys inside topic YAML:
      en/ru -> <notebook_id> -> key
    """
    if notebook_id is None:
        _STATE["notebook"] = None
        return
    s = str(notebook_id).strip()
    _STATE["notebook"] = s if s else None


def get_notebook() -> Optional[str]:
    return _STATE.get("notebook")


# ---------------------------------------------------------------------
# Fonts: Cyrillic support
# ---------------------------------------------------------------------
def configure_cyrillic_fonts(preferred: Optional[list[str]] = None) -> None:
    """
    Configure matplotlib fonts that support Cyrillic. Safe to call multiple times.

    We do not hard-fail if fonts are missing; matplotlib will fall back.
    """
    if preferred is None:
        preferred = [
            "DejaVu Sans",          # usually present; often supports Cyrillic
            "Arial",
            "Liberation Sans",
            "Noto Sans",
            "Noto Sans Display",
            "Roboto",
        ]

    mpl.rcParams["font.family"] = "sans-serif"
    mpl.rcParams["font.sans-serif"] = preferred + mpl.rcParams.get("font.sans-serif", [])
    mpl.rcParams["axes.unicode_minus"] = False


# ---------------------------------------------------------------------
# YAML loading
# ---------------------------------------------------------------------
def _read_yaml(path: Path) -> dict:
    if yaml is None:
        raise RuntimeError(
            "PyYAML is not installed, but YAML i18n loading was requested. "
            "Install with: pip install pyyaml"
        )
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    if not isinstance(data, dict):
        raise ValueError(f"YAML must contain a mapping at top-level: {path}")
    return data


def load_topic_i18n(topic_root: Path, *, strict: bool = False) -> None:
    """
    Load i18n dictionaries from <topic_root>/i18n/.

    Expected files:
      - labels.yaml
      - titles.yaml

    Recommended scalable YAML format:
      en:
        common:
          age_gyr: "Age (Gyr)"
        ACAP_001:
          legend_host_stars: "host stars"
      ru:
        common:
          ...

    Also supported:
      en:
        age_gyr: "Age (Gyr)"         # flat per-lang
      ru:
        ...

    Backward compatible:
      age_gyr:
        en: "Age (Gyr)"
        ru: "..."

    Notes
    -----
    - If files are missing:
        strict=False -> silently keep empty dictionaries
        strict=True  -> raise an error
    - Loaded dictionaries replace current ones.
    """
    topic_root = Path(topic_root)
    i18n_dir = topic_root / "i18n"
    labels_path = i18n_dir / "labels.yaml"
    titles_path = i18n_dir / "titles.yaml"

    labels: dict = {}
    titles: dict = {}

    if labels_path.exists():
        labels = _read_yaml(labels_path)
    elif strict:
        raise FileNotFoundError(f"Missing i18n labels file: {labels_path}")

    if titles_path.exists():
        titles = _read_yaml(titles_path)
    elif strict:
        raise FileNotFoundError(f"Missing i18n titles file: {titles_path}")

    _STATE["labels"] = labels
    _STATE["titles"] = titles
    _STATE["loaded_from"] = str(i18n_dir)


def debug_i18n_state() -> None:
    """Print current i18n state (useful during notebook refactors)."""
    print("lang:", _STATE.get("lang"))
    print("notebook:", _STATE.get("notebook"))
    print("loaded_from:", _STATE.get("loaded_from"))
    print("labels(top-level keys):", len(_STATE.get("labels", {}) or {}))
    print("titles(top-level keys):", len(_STATE.get("titles", {}) or {}))


# ---------------------------------------------------------------------
# Lookup helpers
# ---------------------------------------------------------------------
def _lookup(mapping: dict, key: str, lang: Lang) -> Optional[str]:
    """
    Lookup key in a mapping that can contain:

    NEW scalable topic YAML (recommended):
      en:
        common:
          age_gyr: "Age (Gyr)"
        ACAP_001:
          legend_host_stars: "host stars"
      ru:
        common:
          ...

    Also supports:
      en:
        age_gyr: "Age (Gyr)"          # flat per-lang
      ru:
        ...

    Backward compatible:
      age_gyr:
        en: "Age (Gyr)"
        ru: "..."

    Or:
      key: "..." (already localized/universal)
    """
    if not isinstance(mapping, dict):
        return None

    nb = _STATE.get("notebook")

    # --- Case 1: top-level has en/ru ---
    if "en" in mapping or "ru" in mapping:
        lang_map = mapping.get(lang) or mapping.get("en")
        if not isinstance(lang_map, dict):
            return None

        # 1) notebook namespace (highest priority)
        if nb and isinstance(lang_map.get(nb), dict):
            v = lang_map[nb].get(key)
            if isinstance(v, str) and v.strip():
                return v

        # 2) common namespace (2nd priority)
        if isinstance(lang_map.get("common"), dict):
            v = lang_map["common"].get(key)
            if isinstance(v, str) and v.strip():
                return v

        # 3) flat per-lang (fallback)
        v = lang_map.get(key)
        if isinstance(v, str) and v.strip():
            return v

        return None

    # --- Case 2: old format key -> {en/ru} ---
    if key not in mapping:
        return None

    v = mapping[key]
    if isinstance(v, str):
        return v
    if isinstance(v, dict):
        return v.get(lang) or v.get("en")
    return None


def label(key: str, *, lang: Optional[Lang] = None) -> str:
    """
    Return localized label for a key. Fallback order:
      1) topic YAML labels
      2) key itself
    """
    lang2 = get_lang() if lang is None else lang
    txt = _lookup(_STATE.get("labels", {}) or {}, key, lang2)
    return txt if isinstance(txt, str) and txt.strip() else key


def title(key: str, *, lang: Optional[Lang] = None) -> str:
    """
    Return localized title for a key. Fallback order:
      1) topic YAML titles
      2) key itself
    """
    lang2 = get_lang() if lang is None else lang
    txt = _lookup(_STATE.get("titles", {}) or {}, key, lang2)
    return txt if isinstance(txt, str) and txt.strip() else key


# Convenience aliases (nice in notebooks)
L = label
T = title