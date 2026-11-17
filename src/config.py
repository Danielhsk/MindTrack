"""Shared constants for MindTrack (aligned with Entregable 2 / 3 notebooks)."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

RANDOM_STATE = 42
RECALL_TARGET = 0.85

DATA_FILENAME = "academic_risk_dataset.csv"
DATA_PATH = ROOT / "data" / DATA_FILENAME
MODELS_DIR = ROOT / "models"
REPORTS_DIR = ROOT / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"
ASSETS_COLAB_DIR = ROOT / "assets" / "colab"

# Static exports from Google Colab notebooks (Insight · Huella de datos)
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

# PNG generadas al exportar el experimento (Entregable 3 / train_and_export)
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
]

TARGET = "Academic_Failure_Risk"
ID_COLS = ["Student_ID"]
LEAKAGE_COLS = ["Academic_Performance_Score"]  # excluded from ML (preventive / anti-leakage)
NOMINAL_COLS = ["Gender", "Education_Level"]
ORDINAL_COL = "Burnout_Level"
BURNOUT_ORDER = ["Low", "Moderate", "High", "Severe"]
BURNOUT_MAP = {level: code for code, level in enumerate(BURNOUT_ORDER)}
DROP_FIRST_DUMMY = True
EXPECTED_N_FEATURES = 13

PRODUCTION_MODEL_KEY = "xgboost"
MODEL_LABELS = {
    "logistic_regression": "Logistic Regression",
    "random_forest": "Random Forest",
    "xgboost": "XGBoost",
}

# Form / production feature inputs (no Academic_Performance_Score)
FORM_NUMERIC = [
    "Age",
    "Daily_Social_Media_Hours",
    "Daily_AI_Tool_Usage_Hours",
    "Sleep_Hours",
    "Physical_Activity_Hours",
    "Mental_Health_Score",
    "Physical_Health_Score",
    "Social_Isolation_Score",
]
FORM_CATEGORICAL = {
    "Gender": ["Male", "Female", "Non-binary"],
    "Education_Level": ["High School", "College", "University"],
    "Burnout_Level": BURNOUT_ORDER,
}

# Rule-engine thresholds (justified from EDA / slide profiles)
RULE_THRESHOLDS = {
    "Sleep_Hours": {"max_ok": 6.0, "direction": "low"},
    "Daily_Social_Media_Hours": {"min_ok": 6.5, "direction": "high"},
    "Physical_Activity_Hours": {"max_ok": 0.5, "direction": "low"},
    "Mental_Health_Score": {"max_ok": 65.0, "direction": "low"},
    "Social_Isolation_Score": {"min_ok": 5.5, "direction": "high"},
    "Burnout_Level": {"severe_codes": ["High", "Severe"]},
}

# UI palette (MindTrack)
COLORS = {
    "navy": "#1F3A5F",
    "slate": "#475569",
    "mist": "#94A3B8",
    "bg": "#F8FAFC",
    "white": "#FFFFFF",
    "ink": "#0F172A",
    "accent": "#B45309",
    "ok": "#15803D",
    "border": "#E2E8F0",
    "sky": "#0EA5E9",
    "violet": "#6366F1",
    "amber": "#F59E0B",
    "mint": "#14B8A6",
    # Sidebar wellness palette (v2.3)
    "side_deep": "#1A2E2D",
    "side_mid": "#243B3A",
    "side_mist": "#94B8B4",
    "calm_teal": "#5EEAD4",
    "calm_sage": "#A7F3D0",
    "calm_sea": "#99F6E4",
}