# MindTrack

**Sistema inteligente de estimación de riesgo académico estudiantil**  
Asignatura: Sistemas Inteligentes · Prototipo universitario (Machine Learning + Streamlit)

MindTrack permite ingresar el perfil de un estudiante (hábitos digitales, sueño, actividad física, bienestar y burnout) y obtener:

1. Predicción de `Academic_Failure_Risk` con el modelo de **producción** (actualmente **XGBoost**, según test)
2. Probabilidad y banda de riesgo (BAJO / MODERADO / ALTO)
3. Factores relevantes de la predicción
4. Recomendaciones basadas en reglas
5. Una conclusión en lenguaje claro

> **Disclaimer:** MindTrack es un prototipo académico. **No** es un diagnóstico médico ni psicológico, ni una decisión institucional definitiva. Predicción ≠ causalidad.

---

## Resumen ejecutivo

| Aspecto | Detalle |
|---------|---------|
| **Problema** | ¿Es posible estimar el riesgo de fracaso académico a partir de hábitos y bienestar? |
| **Datos** | 15.000 registros · 14 variables · ~6 % clase en riesgo |
| **Target** | `Academic_Failure_Risk` (0 / 1) |
| **Excluido del ML** | `Academic_Performance_Score` (data leakage / escenario preventivo) |
| **Modelos** | Logistic Regression · Random Forest · **XGBoost (producción)** |
| **Split** | 70 % train / 15 % validation / 15 % test · `random_state=42` |
| **Criterio** | Recall (clase 1) ≥ 0.85; umbral en Validation; **producción elegida por métricas en Test** (F1 → PR-AUC → precisión → menos FP → menos FN) |
| **App** | Streamlit · **Producción** + **Laboratorio** · Docker opcional (`docker compose up`) |
| **Despliegue** | Local, [Docker](docs/DOCKER.md) o Streamlit Cloud |

### Validation (umbral ajustado por modelo)

| Modelo | Recall | F1 | PR-AUC | FN | FP | Ganador solo val. |
|--------|-------:|---:|-------:|---:|---:|:-------------------|
| **Logistic Regression** | 0.852 | **0.819** | **0.917** | 20 | **31** | **Sí (F1)** |
| Random Forest | 0.874 | 0.787 | 0.899 | 17 | 47 | — |
| XGBoost | 0.859 | 0.789 | 0.915 | 19 | 43 | — |

### Test (τ fijado en Validation, sin re-ajuste · `reports/comparison_test.csv`)

| Modelo | Recall | F1 | PR-AUC | FN | FP | Producción |
|--------|-------:|---:|-------:|---:|---:|:----------:|
| Logistic Regression | 0.852 | 0.801 | 0.918 | 20 | 37 | — |
| Random Forest | 0.911 | 0.809 | 0.926 | 12 | 46 | — |
| **XGBoost** | **0.881** | **0.824** | **0.933** | **16** | **35** | **Sí** |

En validación gana LR en F1 y menos alertas falsas; en **test** los tres cumplen recall ≥ 0,85 y **XGBoost** queda primero por F1 y PR-AUC (menos FN que LR, menos FP que RF). Esa elección está en `models/metadata.json` → `selection_criteria`.

---

## Estructura del repositorio

```text
MindTrack/
├── app/streamlit_app.py          # Aplicación Streamlit (Prod + Lab)
├── Dockerfile / docker-compose.yml
├── src/                          # Preprocess, predict, reglas, explicación, UI
├── models/                       # Pipelines joblib + metadata.json
├── data/academic_risk_dataset.csv
├── notebooks/                    # Entregable 2 (EDA) y Entregable 3 (comparación)
├── reports/                      # comparison_validation/test.csv + figures PNG
├── scripts/train_and_export.py   # Regenera modelos y reportes
├── docs/                         # CONTEXTO, DOCKER, guion, informe
├── requirements.txt
└── README.md
```

---

## Cómo ejecutar

### Opción A · Docker (recomendado para demo / entrega)

Requiere [Docker Desktop](https://www.docker.com/products/docker-desktop/).

```bash
docker compose up --build
```

Navegador: **http://localhost:8501** · Guía detallada: [docs/DOCKER.md](docs/DOCKER.md)

### Opción B · Python local

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
pip install -r requirements.txt

# (Opcional) Regenerar modelos y gráficas
python scripts/train_and_export.py

streamlit run app/streamlit_app.py
```

- **Producción:** formulario → preprocess → modelo en `metadata.json` → umbral → recomendaciones.  
- **Laboratorio:** `comparison_validation.csv`, `comparison_test.csv` y PNG; **no reentrena**.

---

## Notebooks (Colab)

| Entregable | Notebook | Rol |
|:----------:|----------|-----|
| 2 | `notebooks/MindTrack_EDA_Preprocesamiento.ipynb` | Calidad, EDA, preprocesamiento, split, baseline LR |
| 3 | `notebooks/MindTrack_03_Comparacion_Modelos.ipynb` | Comparación LR / RF / XGBoost |

Abrir en Colab (tras push a GitHub):

- Repo: https://github.com/Danielhsk/MindTrack  
- [Entregable 2 en Colab](https://colab.research.google.com/github/Danielhsk/MindTrack/blob/main/notebooks/MindTrack_EDA_Preprocesamiento.ipynb)  
- [Entregable 3 en Colab](https://colab.research.google.com/github/Danielhsk/MindTrack/blob/main/notebooks/MindTrack_03_Comparacion_Modelos.ipynb)

---

## Datos

- Archivo: `data/academic_risk_dataset.csv`
- Origen: dataset académico de hábitos digitales / salud estudiantil (Kaggle / curso)
- Variable objetivo: `Academic_Failure_Risk`
- Ver `data/README.md`

---

## Decisiones de diseño (producto)

1. Formulario de producción **sin** `Academic_Performance_Score`.
2. Comparación **LR · RF · XGB** en validation y **test**; producción = ganador en **test** (`selection_criteria` en metadata).
3. Actualmente **XGBoost** (F1 y PR-AUC en test; recall 0,881 · FN 16 · FP 35).
4. Laboratorio = visor de artefactos; Docker empaqueta la misma app sin reentrenar.
5. UI en español; columnas y nombres de modelos en inglés.

### Documentación clave

| Archivo | Contenido |
|---------|-----------|
| [docs/CONTEXTO_CHAT_Y_PRESENTACION.md](docs/CONTEXTO_CHAT_Y_PRESENTACION.md) | Métricas, defensa oral, arquitectura |
| [docs/DOCKER.md](docs/DOCKER.md) | Contenedor y troubleshooting |
| [reports/README.md](reports/README.md) | CSV y figuras del experimento |
| [docs/CONTEXT_MASTER_PROJECT.md](docs/CONTEXT_MASTER_PROJECT.md) | Diseño maestro del curso |

---

## Autores

Geraldin Perez · Daniel Hernandez

---

## Licencia de uso académico

Prototipo desarrollado con fines educativos. Uso del dataset sujeto a los términos de su fuente original.
