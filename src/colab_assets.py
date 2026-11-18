"""Static figure catalog for Insight (Colab EDA + ML export PNGs)."""

from __future__ import annotations

from pathlib import Path

from src.config import FIGURES_DIR, ROOT

ASSETS_COLAB_DIR = ROOT / "assets" / "colab"

COLAB_EDA_GALLERY: list[tuple[str, str, str]] = [
    (
        "eda-target-balance.jpeg",
        "Balance de riesgo académico",
        "Proporción de estudiantes con y sin riesgo alto en el dataset (EDA Colab).",
    ),
    (
        "eda-distribution.jpeg",
        "Distribución de variables",
        "Forma general de las variables numéricas antes del modelado.",
    ),
    (
        "eda-histogram.jpeg",
        "Histogramas",
        "Frecuencia de valores en hábitos, sueño y bienestar.",
    ),
    (
        "eda-boxplot.jpeg",
        "Boxplots (1)",
        "Mediana y valores atípicos por variable.",
    ),
    (
        "eda-boxplot-alt.jpeg",
        "Boxplots (2)",
        "Comparación adicional entre grupos del dataset.",
    ),
    (
        "eda-correlation-matrix.jpeg",
        "Matriz de correlación",
        "Relaciones lineales entre variables del estudio.",
    ),
    (
        "eda-academic-risk.jpeg",
        "Riesgo académico (vista EDA)",
        "Exploración visual del outcome Academic_Failure_Risk.",
    ),
]

ML_EXPORT_GALLERY: list[tuple[str, str, str]] = [
    (
        "metrics_validation.png",
        "Métricas en validación",
        "Comparación LR, Random Forest y XGBoost en la partición de validación.",
    ),
    (
        "pr_curves_validation.png",
        "Curvas precision–recall",
        "Capacidad del modelo para priorizar casos en verdadero riesgo.",
    ),
    (
        "confusion_validation.png",
        "Matrices de confusión",
        "Aciertos y errores por modelo en validación.",
    ),
    (
        "fn_fp_validation.png",
        "Falsos negativos y positivos",
        "Trade-off entre no perder alertas y evitar alarmas innecesarias.",
    ),
    (
        "heatmap_validation.png",
        "Heatmap de métricas",
        "Vista compacta de todas las métricas por algoritmo.",
    ),
    (
        "metrics_test.png",
        "Métricas en test",
        "Comparación de los tres modelos en el conjunto de prueba final.",
    ),
    (
        "fn_fp_test.png",
        "FN / FP en test",
        "Errores en prueba con umbrales fijados en validación.",
    ),
    (
        "heatmap_test.png",
        "Heatmap · test",
        "Métricas agregadas en la partición de prueba.",
    ),
]

# Backward-compatible aliases (older imports from src.config)
FIGURES_EXPORT_DIR: Path = FIGURES_DIR