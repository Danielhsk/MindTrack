"""Load production model and run inference for a single student."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

import joblib
import numpy as np

from src.config import MODELS_DIR, PRODUCTION_MODEL_KEY
from src.preprocessing import transform_form_row


@lru_cache(maxsize=1)
def load_metadata(path: str | None = None) -> dict:
    meta_path = Path(path) if path else MODELS_DIR / "metadata.json"
    return json.loads(meta_path.read_text(encoding="utf-8"))


@lru_cache(maxsize=1)
def load_production_pipeline(path: str | None = None):
    pipe_path = Path(path) if path else MODELS_DIR / f"pipeline_{PRODUCTION_MODEL_KEY}.joblib"
    return joblib.load(pipe_path)


def probability_to_band(proba: float, threshold: float) -> str:
    """Map probability to BAJO/MODERADO/ALTO relative to the decision threshold."""
    if proba >= threshold:
        return "ALTO"
    if proba >= threshold * 0.5:
        return "MODERADO"
    return "BAJO"


def predict_student(form: dict) -> dict:
    """Run real ML inference with XGBoost + Validation-tuned threshold."""
    meta = load_metadata()
    pipeline = load_production_pipeline()
    features = meta["feature_names"]
    threshold = float(meta["thresholds"][meta["production_model_label"]])

    X = transform_form_row(form, features)
    proba = float(pipeline.predict_proba(X)[:, 1][0])
    predicted = int(proba >= threshold)
    band = probability_to_band(proba, threshold)

    return {
        "probability": proba,
        "predicted_class": predicted,
        "threshold": threshold,
        "risk_band": band,
        "model_key": meta["production_model_key"],
        "model_label": meta["production_model_label"],
        "feature_vector": X.iloc[0].to_dict(),
        "features_used": features,
    }


def clear_model_cache() -> None:
    load_metadata.cache_clear()
    load_production_pipeline.cache_clear()