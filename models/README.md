# Modelos · MindTrack

Artefactos generados por `python scripts/train_and_export.py` (misma lógica que el notebook de comparación).

| Archivo | Descripción |
|---------|-------------|
| `pipeline_logistic_regression.joblib` | Baseline LR (`StandardScaler` + `class_weight='balanced'`) |
| `pipeline_random_forest.joblib` | Random Forest (`class_weight='balanced_subsample'`) |
| `pipeline_xgboost.joblib` | XGBoost (candidato boosting) |
| `metadata.json` | Features, umbrales, métricas val./test, **`production_model_key`**, criterio de selección |

## Producción

- Clave actual: `metadata.json` → `production_model_key` (elegida por métricas en **test**)
- Umbral: τ calibrado en validación (sin re-ajuste en test)
- La app carga `pipeline_{production_model_key}.joblib` para inferencia en vivo

Reportes: `reports/comparison_validation.csv` y `reports/comparison_test.csv`

## Regenerar

```bash
python scripts/train_and_export.py
```

Luego haz commit de `models/` y `reports/` para que el Laboratorio de Streamlit muestre la última corrida versionada.
