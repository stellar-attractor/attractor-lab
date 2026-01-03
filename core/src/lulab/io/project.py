# lulab/io/project.py
from __future__ import annotations
from pathlib import Path

from .paths import (
    get_topic_root,
    topic_data_raw,
    topic_data_processed,
    topic_figures_dir,
    topic_animations_dir,
)

def topic_root(topic_id: str) -> Path:
    return get_topic_root(topic_id)

def data_raw(topic_id: str, ensure: bool = False) -> Path:
    p = topic_data_raw(topic_id)
    if ensure:
        p.mkdir(parents=True, exist_ok=True)
    return p

def data_processed(topic_id: str, ensure: bool = True) -> Path:
    p = topic_data_processed(topic_id)
    if ensure:
        p.mkdir(parents=True, exist_ok=True)
    return p

def fig_dir(topic_id: str, lang: str = "en", ensure: bool = True) -> Path:
    p = topic_figures_dir(topic_id, lang=lang)
    if ensure:
        p.mkdir(parents=True, exist_ok=True)
    return p

def animations_dir(topic_id: str, ensure: bool = True) -> Path:
    p = topic_animations_dir(topic_id)
    if ensure:
        p.mkdir(parents=True, exist_ok=True)
    return p