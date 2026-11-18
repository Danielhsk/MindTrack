# Reportes del experimento · MindTrack

Generados por `python scripts/train_and_export.py`.

## Tablas CSV

| Archivo | Contenido |
|---------|-----------|
| `comparison_validation.csv` | LR, RF, XGB en validación (umbral calibrado, recall ≥ 0.85) |
| `comparison_test.csv` | Los **tres** modelos en test (mismo τ de validación, sin re-ajuste) |
| `evaluation_test_all_models.csv` | Igual que `comparison_test.csv` (formato export) |
| `evaluation_test_xgboost.csv` | Fila del **modelo de producción** actual (legacy nombre; ver `Modelo` columna) |
| `evaluation_test_production.csv` | Fila del ganador en test (alias recomendado) |

## Figuras (`figures/`)

| PNG | Partición |
|-----|-----------|
| `metrics_validation.png`, `fn_fp_validation.png`, `pr_curves_validation.png`, `confusion_validation.png`, `heatmap_validation.png` | Validation |
| `metrics_test.png`, `fn_fp_test.png`, `heatmap_test.png` | Test |

## Criterio de producción

Documentado en `models/metadata.json` → `selection_criteria`:

1. Recall (clase 1) ≥ 0.85 en **test**
2. Entre quienes cumplen: **F1 → PR-AUC → precisión → menos FP → menos FN**

Última corrida (seed 42): líder en validation = Logistic Regression; producción en test = **XGBoost**.