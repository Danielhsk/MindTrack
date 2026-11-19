# Documentación · MindTrack

| Archivo | Contenido |
|---------|-----------|
| [CONTEXT_MASTER_PROJECT.md](CONTEXT_MASTER_PROJECT.md) | Diseño maestro (alcance, RF/RNF, arquitectura) |
| [CONTEXTO_CHAT_Y_PRESENTACION.md](CONTEXTO_CHAT_Y_PRESENTACION.md) | Métricas validation/test, defensa oral, FAQ |
| [DOCKER.md](DOCKER.md) | Ejecución con Docker / Compose |
| [pipeline_xgboost_explicacion.md](pipeline_xgboost_explicacion.md) | Flujo de inferencia del motor en producción (XGBoost) |

## Resultados del experimento (referencia rápida)

- Validación: LR lidera F1 (0,819) y menos FP (31).
- Test (τ fijo): **XGBoost** lidera F1 (0,824) y PR-AUC (0,933) → `production_model_key` en `models/metadata.json`.
- Tablas: `../reports/comparison_validation.csv`, `../reports/comparison_test.csv`.

## Pendiente de agregar por el equipo

- Informe final para el profesor (PDF) — fuente: `python scripts/generate_informe_apa7.py`
- Presentación final (PDF / PPT)

Colocarlos en esta carpeta cuando estén listos.
