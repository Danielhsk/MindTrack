"""Train LR / Random Forest / XGBoost and export artifacts for the MindTrack app.

Usage (from repo root):
    python scripts/train_and_export.py
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    average_precision_score,
    confusion_matrix,
    f1_score,
    precision_recall_curve,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.config import (  # noqa: E402
    COLORS,
    DATA_PATH,
    FIGURES_DIR,
    MODEL_LABELS,
    MODELS_DIR,
    PRODUCTION_MODEL_KEY,
    RANDOM_STATE,
    RECALL_TARGET,
    REPORTS_DIR,
)
from src.preprocessing import preprocess  # noqa: E402


def stratified_split(X, y):
    X_train, X_temp, y_train, y_temp = train_test_split(
        X, y, test_size=0.30, stratify=y, random_state=RANDOM_STATE
    )
    X_val, X_test, y_val, y_test = train_test_split(
        X_temp, y_temp, test_size=0.50, stratify=y_temp, random_state=RANDOM_STATE
    )
    return X_train, X_val, X_test, y_train, y_val, y_test


def find_threshold(y_true, y_proba, recall_target: float = RECALL_TARGET) -> float:
    precision, recall, thresholds = precision_recall_curve(y_true, y_proba)
    precision, recall = precision[:-1], recall[:-1]
    valid = recall >= recall_target
    if not valid.any():
        return float(thresholds.min())
    f1 = 2 * precision[valid] * recall[valid] / (precision[valid] + recall[valid] + 1e-12)
    return float(thresholds[valid][np.argmax(f1)])


def metrics_row(name: str, y_true, y_proba, threshold: float) -> dict:
    y_pred = (np.asarray(y_proba) >= threshold).astype(int)
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()
    return {
        "Modelo": name,
        "Umbral": threshold,
        "Recall (C1)": recall_score(y_true, y_pred, zero_division=0),
        "Precision (C1)": precision_score(y_true, y_pred, zero_division=0),
        "F1-Score (C1)": f1_score(y_true, y_pred, zero_division=0),
        "PR-AUC": average_precision_score(y_true, y_proba),
        "ROC-AUC": roc_auc_score(y_true, y_proba),
        "FN": int(fn),
        "FP": int(fp),
        "TP": int(tp),
        "TN": int(tn),
        "Cumple Recall": bool(recall_score(y_true, y_pred, zero_division=0) >= RECALL_TARGET),
    }


def build_pipelines(y_train: pd.Series) -> dict:
    scale_pos_weight = float((y_train == 0).sum() / max((y_train == 1).sum(), 1))
    return {
        "logistic_regression": Pipeline(
            [
                ("scaler", StandardScaler()),
                (
                    "model",
                    LogisticRegression(
                        class_weight="balanced",
                        max_iter=1_000,
                        random_state=RANDOM_STATE,
                    ),
                ),
            ]
        ),
        "random_forest": Pipeline(
            [
                (
                    "model",
                    RandomForestClassifier(
                        n_estimators=300,
                        min_samples_leaf=2,
                        class_weight="balanced_subsample",
                        random_state=RANDOM_STATE,
                        n_jobs=-1,
                    ),
                )
            ]
        ),
        "xgboost": Pipeline(
            [
                (
                    "model",
                    XGBClassifier(
                        n_estimators=300,
                        max_depth=5,
                        learning_rate=0.05,
                        subsample=0.9,
                        colsample_bytree=0.9,
                        scale_pos_weight=scale_pos_weight,
                        eval_metric="logloss",
                        random_state=RANDOM_STATE,
                        n_jobs=-1,
                    ),
                )
            ]
        ),
    }


def save_figures(comparison: pd.DataFrame, proba_val: dict, y_val, thresholds: dict) -> None:
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    sns.set_theme(style="whitegrid")

    # Metrics bars
    metrics = ["Recall (C1)", "F1-Score (C1)", "Precision (C1)", "PR-AUC", "ROC-AUC"]
    fig, ax = plt.subplots(figsize=(10, 5))
    comparison[metrics].plot(kind="bar", ax=ax, color=[COLORS["navy"], COLORS["slate"], COLORS["mist"], COLORS["accent"], "#64748B"])
    ax.axhline(RECALL_TARGET, color=COLORS["accent"], linestyle="--", label=f"Recall target {RECALL_TARGET}")
    ax.set_ylim(0, 1.05)
    ax.set_title("Validation metrics · model comparison", fontweight="bold", color=COLORS["navy"])
    ax.legend(frameon=False, fontsize=8)
    plt.xticks(rotation=15)
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "metrics_validation.png", dpi=140)
    plt.close(fig)

    # FN vs FP
    fig, ax = plt.subplots(figsize=(8, 4.5))
    x = np.arange(len(comparison))
    ax.bar(x - 0.2, comparison["FN"], 0.4, label="FN", color=COLORS["accent"])
    ax.bar(x + 0.2, comparison["FP"], 0.4, label="FP", color=COLORS["slate"])
    ax.set_xticks(x)
    ax.set_xticklabels(comparison.index, rotation=10)
    ax.set_title("False Negatives vs False Positives · Validation", fontweight="bold", color=COLORS["navy"])
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "fn_fp_validation.png", dpi=140)
    plt.close(fig)

    # PR curves overlay
    fig, ax = plt.subplots(figsize=(8, 5.5))
    colors = [COLORS["navy"], COLORS["slate"], COLORS["accent"]]
    for (name, proba), color in zip(proba_val.items(), colors):
        p, r, _ = precision_recall_curve(y_val, proba)
        ap = average_precision_score(y_val, proba)
        ax.plot(r, p, color=color, linewidth=2, label=f"{name} · PR-AUC={ap:.3f}")
    ax.axvline(RECALL_TARGET, color=COLORS["accent"], linestyle=":", label="Recall target")
    ax.set_xlabel("Recall")
    ax.set_ylabel("Precision")
    ax.set_title("Precision-Recall curves · Validation", fontweight="bold", color=COLORS["navy"])
    ax.legend(frameon=False, fontsize=8)
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "pr_curves_validation.png", dpi=140)
    plt.close(fig)

    # Confusion matrices
    fig, axes = plt.subplots(1, 3, figsize=(14, 4.2))
    for ax, (name, proba) in zip(axes, proba_val.items()):
        thr = thresholds[name]
        y_pred = (proba >= thr).astype(int)
        ConfusionMatrixDisplay(
            confusion_matrix(y_val, y_pred, labels=[0, 1]),
            display_labels=["No risk", "At risk"],
        ).plot(ax=ax, colorbar=False, values_format="d", cmap="Blues")
        ax.set_title(f"{name}\nthreshold={thr:.3f}", fontsize=10)
    fig.suptitle("Confusion matrices · Validation", fontweight="bold", color=COLORS["navy"], x=0.02, ha="left")
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "confusion_validation.png", dpi=140)
    plt.close(fig)

    # Heatmap
    heat_cols = ["Recall (C1)", "Precision (C1)", "F1-Score (C1)", "PR-AUC", "ROC-AUC"]
    fig, ax = plt.subplots(figsize=(7, 3.6))
    sns.heatmap(comparison[heat_cols], annot=True, fmt=".3f", cmap="YlGnBu", ax=ax)
    ax.set_title("Metrics heatmap · Validation", fontweight="bold", color=COLORS["navy"])
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "heatmap_validation.png", dpi=140)
    plt.close(fig)


def main() -> None:
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(DATA_PATH)
    X, y = preprocess(df)
    X_train, X_val, X_test, y_train, y_val, y_test = stratified_split(X, y)

    pipelines = build_pipelines(y_train)
    fitted = {}
    proba_val = {}
    thresholds = {}
    rows_val = []

    for key, pipe in pipelines.items():
        label = MODEL_LABELS[key]
        print(f"Training {label}...")
        pipe.fit(X_train, y_train)
        fitted[key] = pipe
        proba = pipe.predict_proba(X_val)[:, 1]
        thr = find_threshold(y_val, proba)
        thresholds[label] = thr
        proba_val[label] = proba
        rows_val.append(metrics_row(label, y_val, proba, thr))
        joblib.dump(pipe, MODELS_DIR / f"pipeline_{key}.joblib")

    comparison = pd.DataFrame(rows_val).set_index("Modelo")
    comparison.to_csv(REPORTS_DIR / "comparison_validation.csv")

    # Production model (XGBoost) evaluated on Test with its Validation threshold
    prod_label = MODEL_LABELS[PRODUCTION_MODEL_KEY]
    prod_thr = thresholds[prod_label]
    prod_pipe = fitted[PRODUCTION_MODEL_KEY]
    proba_test = prod_pipe.predict_proba(X_test)[:, 1]
    test_row = metrics_row(prod_label, y_test, proba_test, prod_thr)
    pd.DataFrame([test_row]).to_csv(REPORTS_DIR / "evaluation_test_xgboost.csv", index=False)

    save_figures(comparison, proba_val, y_val, thresholds)

    metadata = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "random_state": RANDOM_STATE,
        "recall_target": RECALL_TARGET,
        "feature_names": X_train.columns.tolist(),
        "production_model_key": PRODUCTION_MODEL_KEY,
        "production_model_label": prod_label,
        "thresholds": {
            MODEL_LABELS[k]: thresholds[MODEL_LABELS[k]] for k in pipelines
        },
        "validation_metrics": comparison.reset_index().to_dict(orient="records"),
        "test_metrics_production": test_row,
        "split": {"train": 0.70, "validation": 0.15, "test": 0.15},
        "notes": (
            "Academic_Performance_Score excluded (data leakage / preventive scenario). "
            "Production UI uses XGBoost. Laboratory visualizes these exported artifacts only."
        ),
    }
    (MODELS_DIR / "metadata.json").write_text(
        json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    print("\n=== Validation comparison ===")
    print(comparison.round(4).to_string())
    print("\n=== Production (XGBoost) Test ===")
    print(pd.Series(test_row).to_string())
    print(f"\nArtifacts written to {MODELS_DIR} and {REPORTS_DIR}")


if __name__ == "__main__":
    main()