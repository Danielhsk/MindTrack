# MindTrack

**Sistema inteligente de estimación de riesgo académico estudiantil**  
Asignatura: Sistemas Inteligentes · Prototipo universitario (Machine Learning + Streamlit)

MindTrack permite ingresar el perfil de un estudiante (hábitos digitales, sueño, actividad física, bienestar y burnout) y obtener:

1. Predicción de `Academic_Failure_Risk` con **XGBoost**
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
| **Criterio** | Recall (clase 1) ≥ 0.85 en Validation (umbral ajustado) |
| **App** | Streamlit · módulo **Producción** (inferencia) + **Laboratorio** (resultados del experimento, solo lectura) |

### Métricas recientes (Validation, umbral ajustado)

| Modelo | Recall (C1) | F1 (C1) | PR-AUC | Cumple Recall |
|--------|------------:|--------:|-------:|:-------------:|
| Logistic Regression | 0.852 | 0.819 | 0.917 | Sí |
| Random Forest | 0.874 | 0.787 | 0.899 | Sí |
| **XGBoost** | **0.859** | **0.789** | **0.915** | **Sí** |

**Producción (XGBoost) en Test:** Recall ≈ **0.881** · F1 ≈ **0.824** · PR-AUC ≈ **0.933**.

XGBoost se fija como modelo oficial de despliegue (candidato principal del diseño del proyecto, cumple el Recall objetivo y generaliza bien en Test). La comparación completa vive en el módulo Laboratorio y en los notebooks.

---

## Estructura del repositorio

```text
MindTrack/
├── app/streamlit_app.py          # Aplicación Streamlit (Prod + Lab)
├── src/                          # Preprocess, predict, reglas, explicación, UI
├── models/                       # Pipelines joblib + metadata.json
├── data/academic_risk_dataset.csv
├── notebooks/                    # Entregable 2 (EDA) y Entregable 3 (comparación)
├── reports/                      # Tablas CSV + figures PNG del experimento
├── scripts/train_and_export.py   # Regenera modelos y reportes
├── docs/                         # Context master; informe/presentación (añadir luego)
├── requirements.txt
└── README.md
```

---

## Cómo ejecutar (local)

```bash
# 1. Crear entorno e instalar
python -m venv .venv
# Windows:
.venv\Scripts\activate
pip install -r requirements.txt

# 2. (Opcional) Regenerar modelos y gráficas del laboratorio
python scripts/train_and_export.py

# 3. Abrir la app
streamlit run app/streamlit_app.py
```

- **Producción:** formulario → preprocess → XGBoost → umbral → recomendaciones.  
- **Laboratorio:** tablas y PNG ya exportados (misma lógica que Colab Entregable 3); **no reentrena**.

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
2. Modelo oficial: **XGBoost** + umbral calibrado en Validation.
3. Laboratorio = **visor** de artefactos del experimento (performante en Streamlit Cloud).
4. UI en español; nombres técnicos / columnas / modelos en inglés.
5. Streamlit Cloud se publicará **después** de validar localmente.

---

## Autores

Geraldin Perez · Daniel Hernandez

---

## Licencia de uso académico

Prototipo desarrollado con fines educativos. Uso del dataset sujeto a los términos de su fuente original.
