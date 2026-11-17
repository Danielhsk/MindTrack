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
}