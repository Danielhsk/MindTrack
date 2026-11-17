"""Lightweight feature contribution for a single prediction (Production)."""

from __future__ import annotations

import numpy as np
import pandas as pd

from src.predict import load_metadata, load_production_pipeline
from src.preprocessing import transform_form_row


def top_contributions(form: dict, k: int = 8) -> pd.DataFrame:
    """Return top-k feature contributions for the production model.

    Prefer Tree/Linear SHAP when available; fall back to model-native importances
    or absolute standardized coefficients × feature values.
    """
    meta = load_metadata()
    pipe = load_production_pipeline()
    features = meta["feature_names"]
    X = transform_form_row(form, features)

    model = pipe.named_steps["model"]
    model_name = type(model).__name__

    try:
        import shap

        if "XGB" in model_name or "Forest" in model_name or "Tree" in model_name:
            explainer = shap.TreeExplainer(model)
            values = np.asarray(explainer.shap_values(X)).reshape(-1)
        elif "Logistic" in model_name:
            # Pipeline may include scaler
            Xs = pipe.named_steps["scaler"].transform(X) if "scaler" in pipe.named_steps else X.values
            explainer = shap.LinearExplainer(model, Xs, feature_perturbation="interventional")
            values = np.asarray(explainer.shap_values(Xs)).reshape(-1)
        else:
            raise RuntimeError("unsupported")
        method = "SHAP"
    except Exception:
        # Fallback: importance * |z-scored feature| magnitude signal
        if hasattr(model, "feature_importances_"):
            base = np.asarray(model.feature_importances_, dtype=float)
            values = base * np.abs(X.values.reshape(-1))
            method = "importance × |feature|"
        elif hasattr(model, "coef_"):
            coef = np.asarray(model.coef_).reshape(-1)
            Xs = pipe.named_steps["scaler"].transform(X) if "scaler" in pipe.named_steps else X.values
            values = coef * Xs.reshape(-1)
            method = "coef × scaled feature"
        else:
            values = np.zeros(len(features))
            method = "unavailable"

    frame = pd.DataFrame(
        {
            "feature": features,
            "contribution": values,
            "abs_contribution": np.abs(values),
            "value": X.values.reshape(-1),
        }
    ).sort_values("abs_contribution", ascending=False)
    frame["method"] = method
    return frame.head(k).reset_index(drop=True)