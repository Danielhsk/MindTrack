# Documentación · MindTrack

| Archivo | Contenido |
|---------|-----------|
| [CONTEXT_MASTER_PROJECT.md](CONTEXT_MASTER_PROJECT.md) | Diseño maestro (alcance, RF/RNF, arquitectura) |
| [DOCKER.md](DOCKER.md) | Contenedor Docker / Compose y troubleshooting |
| [pipeline_xgboost_explicacion.md](pipeline_xgboost_explicacion.md) | Flujo de inferencia del motor en producción |
| [Informe_MindTrack_APA7.docx](Informe_MindTrack_APA7.docx) | Informe del proyecto (Word APA 7) |

## Resultados del experimento (referencia rápida)

### Validation (calibración de umbral)

| Modelo | Recall | F1 | FN | FP |
|--------|-------:|---:|---:|---:|
| Logistic Regression | 0.852 | **0.819** | 20 | **31** |
| Random Forest | 0.874 | 0.787 | 17 | 47 |
| XGBoost | 0.859 | 0.789 | 19 | 43 |

### Test (τ de validation, sin re-ajuste)

| Modelo | Recall | F1 | PR-AUC | FN | FP | Producción |
|--------|-------:|---:|-------:|---:|---:|:----------:|
| Logistic Regression | 0.852 | 0.801 | 0.918 | 20 | 37 | — |
| Random Forest | 0.911 | 0.809 | 0.926 | 12 | 46 | — |
| **XGBoost** | **0.881** | **0.824** | **0.933** | 16 | **35** | **Sí** |

Artefactos: `../reports/comparison_validation.csv`, `../reports/comparison_test.csv`, `../models/metadata.json` → `selection_criteria`.

## Docker

```bash
docker compose up --build
```

→ http://localhost:8501

## Regenerar métricas

```bash
python scripts/train_and_export.py
```

## Informe Word (solo addendum)

```bash
python scripts/patch_informe_apa7_addendum.py
```

Regenerar informe completo (opcional, reescribe el .docx):

```bash
python scripts/generate_informe_apa7.py
```

## Pendiente

- Presentación final (PDF / PPT) en esta carpeta cuando esté lista.