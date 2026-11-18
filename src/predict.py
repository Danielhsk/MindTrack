"""Load production model and run inference for a single student."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

import joblib
import numpy as np

from src.config import MODEL_LABELS, MODELS_DIR, PRODUCTION_MODEL_KEY
from src.preprocessing import transform_form_row

PANEL_MODEL_KEYS: tuple[str, ...] = (
    "logistic_regression",
    "random_forest",
    "xgboost",
)


@lru_cache(maxsize=1)
def load_metadata(path: str | None = None) -> dict:
    meta_path = Path(path) if path else MODELS_DIR / "metadata.json"
    return json.loads(meta_path.read_text(encoding="utf-8"))


@lru_cache(maxsize=1)
def load_production_pipeline(path: str | None = None):
    if path:
        return joblib.load(Path(path))
    meta = load_metadata()
    model_key = meta.get("production_model_key", PRODUCTION_MODEL_KEY)
    return joblib.load(MODELS_DIR / f"pipeline_{model_key}.joblib")


@lru_cache(maxsize=len(PANEL_MODEL_KEYS))
def load_panel_pipeline(model_key: str):
    if model_key not in PANEL_MODEL_KEYS:
        raise ValueError(f"Unknown panel model: {model_key}")
    return joblib.load(MODELS_DIR / f"pipeline_{model_key}.joblib")


def probability_to_band(proba: float, threshold: float) -> str:
    """Map probability to BAJO/MODERADO/ALTO relative to the decision threshold."""
    if proba >= threshold:
        return "ALTO"
    if proba >= threshold * 0.5:
        return "MODERADO"
    return "BAJO"


def predict_student(form: dict) -> dict:
    """Run production inference (model from metadata) + validation-tuned threshold."""
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


def panel_opinions(form: dict) -> dict:
    """Second opinion: all three validation-tuned models (informational only)."""
    meta = load_metadata()
    features = meta["feature_names"]
    thresholds = meta["thresholds"]
    X = transform_form_row(form, features)
    opinions: list[dict] = []
    votes_alert = 0
    for key in PANEL_MODEL_KEYS:
        label = MODEL_LABELS[key]
        thr = float(thresholds[label])
        proba = float(load_panel_pipeline(key).predict_proba(X)[:, 1][0])
        would_alert = proba >= thr
        if would_alert:
            votes_alert += 1
        opinions.append(
            {
                "model_key": key,
                "model_label": label,
                "probability": proba,
                "threshold": thr,
                "would_alert": would_alert,
                "is_official": key == PRODUCTION_MODEL_KEY,
            }
        )
    total = len(PANEL_MODEL_KEYS)
    if votes_alert == total:
        agreement_text = "Acuerdo total: los tres marcarían alerta."
    elif votes_alert == 0:
        agreement_text = "Acuerdo total: ninguno marcaría alerta."
    else:
        agreement_text = (
            f"Hay divergencia: {votes_alert} de {total} marcarían alerta "
            f"con su umbral de validación."
        )
    return {
        "opinions": opinions,
        "votes_alert": votes_alert,
        "votes_total": total,
        "agreement_text": agreement_text,
    }


def clear_model_cache() -> None:
    load_metadata.cache_clear()
    load_production_pipeline.cache_clear()
    load_panel_pipeline.cache_clear()