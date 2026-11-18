"""Diagrama del pipeline XGBoost MindTrack (PRD)."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "assets" / "pipeline_mindtrack_xgboost.png"
NAVY = "#1F3A5F"
SLATE = "#475569"
ACCENT = "#B45309"
BG = "#F8FAFC"
MINT = "#E2E8F0"


def box(ax, xy, w, h, title, lines, face=MINT, title_color=NAVY):
    x, y = xy
    rect = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.02,rounding_size=0.08",
        linewidth=1.2,
        edgecolor=NAVY,
        facecolor=face,
    )
    ax.add_patch(rect)
    ax.text(x + w / 2, y + h - 0.35, title, ha="center", va="top", fontsize=11, fontweight="bold", color=title_color)
    body = "\n".join(lines)
    ax.text(x + w / 2, y + h / 2 - 0.15, body, ha="center", va="center", fontsize=9, color=SLATE, linespacing=1.35)


def arrow(ax, start, end):
    arr = FancyArrowPatch(
        start,
        end,
        arrowstyle="-|>",
        mutation_scale=12,
        linewidth=1.4,
        color=NAVY,
        shrinkA=4,
        shrinkB=4,
    )
    ax.add_patch(arr)


def main() -> None:
    fig, ax = plt.subplots(figsize=(11, 14))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 16)
    ax.axis("off")
    fig.patch.set_facecolor(BG)

    ax.text(
        5,
        15.35,
        "Pipeline de predicción MindTrack (producción · XGBoost)",
        ha="center",
        fontsize=15,
        fontweight="bold",
        color=NAVY,
    )
    ax.text(
        5,
        14.85,
        "Formulario → preprocesamiento → pipeline_xgboost.joblib → umbral → salida PRD",
        ha="center",
        fontsize=10,
        color=SLATE,
    )

    # Row 1 — UI
    box(
        ax,
        (1.2, 12.6),
        7.6,
        1.55,
        "1. Entrada (Streamlit PRD)",
        [
            "Formulario estudiante (11 campos en español)",
            "Sin Student_ID ni Academic_Performance_Score",
        ],
        face="#DBEAFE",
    )

    # Row 2 — preprocess
    box(
        ax,
        (1.2, 9.6),
        7.6,
        2.35,
        "2. Preprocesamiento (src/preprocessing.py)",
        [
            "Ordinal: Burnout_Level → 0 (Low) … 3 (Severe)",
            "One-hot: Gender, Education_Level (drop_first)",
            "align_features → vector de 13 columnas",
        ],
    )

    # Row 3 — joblib pipeline
    box(
        ax,
        (1.2, 5.9),
        7.6,
        3.1,
        "3. Artefacto models/pipeline_xgboost.joblib",
        [
            "sklearn Pipeline → paso único: model",
            "XGBClassifier (300 árboles, max_depth=5, lr=0.05)",
            "scale_pos_weight · entrenado en 70 % train",
            "Salida: P(riesgo) = predict_proba[:, 1]",
        ],
        face="#FEF3C7",
    )

    # Row 4 — threshold
    box(
        ax,
        (1.2, 3.35),
        7.6,
        1.9,
        "4. Decisión (metadata.json)",
        [
            "Umbral τ ≈ 0,728 (calibrado en validación, recall ≥ 0,85)",
            "Si P ≥ τ → alerta (clase 1) · Bandas BAJO / MODERADO / ALTO",
        ],
        face="#DCFCE7",
    )

    # Row 5 — outputs
    box(
        ax,
        (1.2, 0.55),
        7.6,
        2.35,
        "5. Salidas visibles al usuario",
        [
            "SHAP (TreeExplainer) → barras «Factores que empujan el estado»",
            "Reglas → recomendaciones · Conclusión textual",
            "Segunda opinión: LR + RF + XGB (solo informativa)",
        ],
        face="#F1F5F9",
    )

    arrow(ax, (5, 12.6), (5, 11.95))
    arrow(ax, (5, 9.6), (5, 9.0))
    arrow(ax, (5, 5.9), (5, 5.25))
    arrow(ax, (5, 3.35), (5, 2.9))

  # Side note joblib
    note = FancyBboxPatch(
        (0.35, 6.2),
        0.08,
        2.5,
        boxstyle="square,pad=0",
        facecolor=ACCENT,
        edgecolor=ACCENT,
    )
    ax.add_patch(note)
    ax.text(
        0.15,
        7.45,
        "joblib",
        rotation=90,
        va="center",
        ha="center",
        fontsize=8,
        color="white",
        fontweight="bold",
    )

    legend_handles = [
        mpatches.Patch(facecolor="#DBEAFE", edgecolor=NAVY, label="Interfaz"),
        mpatches.Patch(facecolor=MINT, edgecolor=NAVY, label="Transformación"),
        mpatches.Patch(facecolor="#FEF3C7", edgecolor=NAVY, label="Modelo entrenado"),
        mpatches.Patch(facecolor="#DCFCE7", edgecolor=NAVY, label="Regla de negocio"),
    ]
    ax.legend(handles=legend_handles, loc="lower right", frameon=True, fontsize=8)

    ax.text(
        5,
        0.15,
        "Entrenamiento offline: scripts/train_and_export.py · No se reentrena en la app en vivo",
        ha="center",
        fontsize=8.5,
        color=SLATE,
        style="italic",
    )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(OUT, dpi=160, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print(f"Diagrama guardado: {OUT}")


if __name__ == "__main__":
    main()