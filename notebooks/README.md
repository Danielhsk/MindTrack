# Notebooks · MindTrack

Dos entregables **independientes y coherentes** (no se sustituyen):

| # | Archivo | Contenido |
|---|---------|-----------|
| 2 | `MindTrack_EDA_Preprocesamiento.ipynb` | Validación, EDA (diapositivas), preprocesamiento, split 70/15/15, baseline Logistic Regression |
| 3 | `MindTrack_03_Comparacion_Modelos.ipynb` | Comparación LR / RF / XGB, test de los tres, selección de producción |

Constantes compartidas con la app: `random_state=42`, exclusión de `Academic_Performance_Score`, Recall objetivo 0.85.

Salida alineada con el repo: `reports/comparison_validation.csv`, `reports/comparison_test.csv`, `models/metadata.json`.

Para producción y el módulo Laboratorio de Streamlit, preferir regenerar artefactos con:

```bash
python scripts/train_and_export.py
```
