# Modelos · MindTrack

Artefactos generados por `python scripts/train_and_export.py` (misma lógica que el notebook de comparación).

| Archivo | Descripción |
|---------|-------------|
| `pipeline_logistic_regression.joblib` | Baseline LR (`StandardScaler` + `class_weight='balanced'`) |
| `pipeline_random_forest.joblib` | Random Forest (`class_weight='balanced_subsample'`) |
| `pipeline_xgboost.joblib` | **Modelo de producción** |
| `metadata.json` | Features, umbrales Validation, métricas, timestamp |

## Producción

- Clave: `xgboost`
- Umbral: el de Validation que cumple Recall (C1) ≥ 0.85 con mejor F1 posible
- La app carga únicamente `pipeline_xgboost.joblib` para inferencia en vivo

## Regenerar

```bash
python scripts/train_and_export.py
```

Luego haz commit de `models/` y `reports/` para que el Laboratorio de Streamlit muestre la última corrida versionada.
