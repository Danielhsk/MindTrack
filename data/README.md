# Datos · MindTrack

## Archivo

- `academic_risk_dataset.csv` — 15.000 filas × 14 columnas.

## Variable objetivo

- `Academic_Failure_Risk` — binaria (0 = sin riesgo, 1 = en riesgo).
- Prevalencia aproximada de la clase positiva: **6 %** (900 / 15.000).

## Variables de entrada usadas en el modelo

Hábitos digitales, sueño, actividad física, scores de salud/aislamiento, `Burnout_Level`, `Age`, `Gender`, `Education_Level`.

## Exclusiones

| Columna | Motivo |
|---------|--------|
| `Student_ID` | Identificador, sin valor predictivo |
| `Academic_Performance_Score` | Riesgo de **data leakage**; escenario preventivo (no disponible como “nota previa” en producción) |

## Calidad (Entregable 2)

- 0 % valores faltantes
- 0 % duplicados
- Outliers conservados de forma deliberada (perfiles extremos reales)
