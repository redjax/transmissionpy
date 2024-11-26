from __future__ import annotations

from pathlib import Path
import typing as t

from transmissionpy.core.constants import (
    CSV_OUTPUT_DIR,
    DATA_DIR,
    JSON_OUTPUT_DIR,
    OUTPUT_DIR,
    PQ_OUTPUT_DIR,
)

ALL_PATHS: list = [DATA_DIR, OUTPUT_DIR, PQ_OUTPUT_DIR, JSON_OUTPUT_DIR, CSV_OUTPUT_DIR]

def create_app_paths(paths: list = ALL_PATHS):
    for p in paths:
        if not Path(p).exists():
            try:
                Path(p).mkdir(parents=True, exist_ok=True)
            except Exception as exc: 
                raise Exception(f"Unhandled exception creating path '{p}'. Details: {exc}")
