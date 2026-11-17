"""Preprocessing pipeline identical to MindTrack Entregable 2 / 3."""

from __future__ import annotations

import pandas as pd

from src.config import (
    BURNOUT_MAP,
    DROP_FIRST_DUMMY,
    ID_COLS,
    LEAKAGE_COLS,
    NOMINAL_COLS,
    ORDINAL_COL,
    TARGET,
)


def drop_leakage_and_ids(data: pd.DataFrame) -> pd.DataFrame:
    cols = [c for c in LEAKAGE_COLS + ID_COLS if c in data.columns]
    return data.drop(columns=cols)


def encode_ordinal(data: pd.DataFrame) -> pd.DataFrame:
    out = data.copy()
    out[ORDINAL_COL] = (
        out[ORDINAL_COL].astype(str).str.strip().str.title().map(BURNOUT_MAP).astype(int)
    )
    return out


def encode_one_hot(data: pd.DataFrame) -> pd.DataFrame:
    return pd.get_dummies(
        data, columns=NOMINAL_COLS, drop_first=DROP_FIRST_DUMMY, dtype=int
    )


def preprocess(data: pd.DataFrame, target: str = TARGET) -> tuple[pd.DataFrame, pd.Series]:
    """Full training preprocess: returns X, y without leakage columns."""
    processed = encode_one_hot(encode_ordinal(drop_leakage_and_ids(data)))
    X = processed.drop(columns=[target])
    y = processed[target].astype(int)
    return X, y


def align_features(X: pd.DataFrame, feature_names: list[str]) -> pd.DataFrame:
    """Ensure inference matrix matches training columns (missing dummies -> 0)."""
    aligned = X.reindex(columns=feature_names, fill_value=0)
    return aligned.astype(float)


def row_from_form(form: dict) -> pd.DataFrame:
    """Build a single raw-row DataFrame from Production form values."""
    return pd.DataFrame([form])


def transform_form_row(form: dict, feature_names: list[str]) -> pd.DataFrame:
    """Preprocess a student form submission for model inference."""
    raw = row_from_form(form)
    # Target not present; create temporary column for shared pipeline then drop
    if TARGET not in raw.columns:
        raw[TARGET] = 0
    X, _ = preprocess(raw)
    return align_features(X, feature_names)