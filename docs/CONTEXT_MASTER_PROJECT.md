# CONTEXT MASTER PROJECT — StudentAI
## Sistema Inteligente de Análisis de Bienestar y Riesgo Académico

> **Asignatura:** Sistemas Inteligentes  
> **Tipo:** Machine Learning supervisado + dashboard  
> **Alcance:** MVP universitario, deliberadamente acotado para garantizar su finalización.

---

# 1. Resumen ejecutivo

**StudentAI** será un sistema inteligente en el que un estudiante diligencia un formulario con información sobre hábitos digitales, sueño, actividad física, bienestar, aislamiento social, burnout y desempeño académico.

El sistema procesará estas variables mediante un modelo de **Machine Learning** y entregará:

1. Predicción del riesgo académico.
2. Dashboard con los parámetros analizados.
3. Factores más relevantes para el resultado.
4. Recomendaciones generales sobre aspectos que podrían mejorarse.
5. Una conclusión escrita en lenguaje natural.

El sistema será un **prototipo académico**. No realizará diagnósticos médicos o psicológicos ni tomará decisiones definitivas sobre estudiantes.

---

# 2. Alcance

## Incluido

- Formulario web.
- Validación de datos.
- Preprocesamiento.
- Modelo de clasificación.
- Predicción de `Academic_Failure_Risk`.
- Dashboard.
- Visualización de parámetros.
- Explainable AI básica mediante SHAP.
- Motor sencillo de recomendaciones basado en reglas.
- Conclusión textual mediante plantilla dinámica.
- Evaluación y comparación de modelos.

## Fuera de alcance

- Aplicación móvil.
- Login/multiusuario.
- Integraciones institucionales.
- Base de datos empresarial.
- Chatbot complejo.
- RAG.
- Fine-tuning de LLM.
- Microservicios/Kubernetes.
- Diagnóstico médico o psicológico.
- Seguimiento longitudinal.

**Objetivo:** construir un MVP funcional y defendible en una asignatura universitaria.

---

# 3. Definición del problema

Los estudiantes están expuestos a factores que pueden relacionarse con su experiencia académica: uso de redes sociales, uso de herramientas de IA, sueño, actividad física, aislamiento social, burnout y desempeño académico.

El dataset suministrado reúne información que permite estudiar estas variables y su relación con `Academic_Failure_Risk`.

**Dataset:** `AI_SocialMedia_Student_Health_Dataset_clean.csv`

El archivo contiene **15,000 registros y 14 variables**.

## Situación actual

Un estudiante puede conocer sus calificaciones, pero no necesariamente dispone de una herramienta que integre diferentes factores y los presente en una interpretación sencilla.

## Necesidad

Crear un sistema que reciba información del estudiante, la analice automáticamente, estime su riesgo académico y explique el resultado mediante un dashboard y recomendaciones.

## Pregunta problema

> **¿Es posible desarrollar un sistema inteligente basado en Machine Learning que, a partir de información sobre hábitos digitales, sueño, actividad física, bienestar y desempeño académico, estime el riesgo académico de un estudiante y genere una conclusión con recomendaciones personalizadas?**

---

# 4. Justificación

El rendimiento académico puede estar relacionado con múltiples variables y no necesariamente con un único indicador. El dataset permite analizar simultáneamente diferentes características de los estudiantes.

Machine Learning es pertinente porque permite aprender patrones a partir de registros históricos y utilizar dichos patrones para realizar predicciones sobre nuevos registros.

La solución aportará:

- Análisis automatizado.
- Integración de múltiples variables.
- Predicción basada en datos.
- Identificación de factores relevantes.
- Visualización de resultados.
- Recomendaciones generales.

Académicamente, el proyecto permite aplicar un ciclo completo de Sistemas Inteligentes:

**Datos → Exploración → Preprocesamiento → Entrenamiento → Evaluación → Predicción → Explicación → Visualización**

---

# 5. Objetivos

## 5.1 Objetivo general

> **Desarrollar un sistema inteligente basado en Machine Learning que permita estimar el riesgo académico de un estudiante a partir de variables relacionadas con sus hábitos digitales, bienestar, actividad física, sueño y desempeño académico, generando una interpretación visual y textual de los resultados.**

## 5.2 Objetivos específicos

1. Analizar las características y calidad de los datos disponibles.
2. Preparar los datos necesarios para entrenar modelos de Machine Learning.
3. Implementar y comparar diferentes algoritmos de clasificación.
4. Evaluar los modelos mediante métricas apropiadas.
5. Implementar un prototipo web que presente predicciones, factores relevantes y recomendaciones.

---

# 6. Antecedentes y estado del arte

El grupo deberá consultar mínimo **5 artículos científicos**, preferiblemente publicados durante los últimos cinco años, sobre:

- Predicción de rendimiento académico.
- Predicción de riesgo estudiantil.
- Educational Data Mining.
- Machine Learning aplicado a educación.
- Bienestar estudiantil.
- Explainable AI.

Fuentes recomendadas:

- IEEE Xplore.
- ScienceDirect.
- Springer.
- ACM Digital Library.
- Scopus.
- Google Scholar como apoyo de búsqueda.

## Matriz

| Artículo | Problema | Datos | Modelo | Métricas | Resultado | Limitaciones |
|---|---|---|---|---|---|---|
| Paper 1 | | | | | | |
| Paper 2 | | | | | | |
| Paper 3 | | | | | | |
| Paper 4 | | | | | | |
| Paper 5 | | | | | | |

Los artículos específicos deberán ser seleccionados y citados por el grupo; no se inventarán referencias.

---

# 7. Datos

## 7.1 Dataset

**Archivo:** `AI_SocialMedia_Student_Health_Dataset_clean.csv`

**Registros:** 15,000  
**Variables:** 14

El encabezado contiene:

```text
Student_ID
Age
Gender
Education_Level
Daily_Social_Media_Hours
Daily_AI_Tool_Usage_Hours
Sleep_Hours
Physical_Activity_Hours
Mental_Health_Score
Physical_Health_Score
Social_Isolation_Score
Burnout_Level
Academic_Performance_Score
Academic_Failure_Risk
```

El dataset contiene variables numéricas y categóricas, además de un identificador y una variable objetivo binaria. fileciteturn1file0L12-L20

## 7.2 Variable objetivo

```text
Academic_Failure_Risk
```

```text
0 = No presenta riesgo según el dataset
1 = Presenta riesgo según el dataset
```

## 7.3 Variables de entrada

| Variable | Tipo | Uso |
|---|---|---|
| `Student_ID` | ID | No se utilizará como feature |
| `Age` | Numérica | Entrada |
| `Gender` | Categórica | Entrada |
| `Education_Level` | Categórica | Entrada |
| `Daily_Social_Media_Hours` | Numérica | Entrada |
| `Daily_AI_Tool_Usage_Hours` | Numérica | Entrada |
| `Sleep_Hours` | Numérica | Entrada |
| `Physical_Activity_Hours` | Numérica | Entrada |
| `Mental_Health_Score` | Numérica | Entrada |
| `Physical_Health_Score` | Numérica | Entrada |
| `Social_Isolation_Score` | Numérica | Entrada |
| `Burnout_Level` | Categórica | Entrada |
| `Academic_Performance_Score` | Numérica | Entrada potencial |

Ejemplos reales muestran niveles educativos `High School`, `College` y `University`, diferentes niveles de burnout y el objetivo binario. fileciteturn1file0L13-L20 fileciteturn1file0L77-L86

## 7.4 Calidad inicial

El análisis del archivo indica:

- **Valores faltantes:** 0
- **Duplicados:** 0

La distribución de clases deberá documentarse en el notebook de EDA y utilizarse para decidir las estrategias de balanceo/evaluación.

## 7.5 Data Leakage

Antes del entrenamiento será obligatorio verificar cómo fue generada `Academic_Failure_Risk`.

Existe una posibilidad importante: que el objetivo haya sido construido utilizando directamente `Academic_Performance_Score` u otra variable disponible.

Por ejemplo:

```text
Academic_Performance_Score < X
              ↓
Academic_Failure_Risk = 1
```

Si esto ocurre, utilizar esa variable para entrenar puede producir **data leakage** y métricas artificialmente altas.

Por ello se realizarán dos experimentos:

### Experimento A
Todas las variables disponibles.

### Experimento B
Variables de hábitos/bienestar **sin `Academic_Performance_Score`**.

Se compararán ambos resultados antes de seleccionar el modelo definitivo.

---

# 8. Enfoque de Machine Learning

El problema será tratado inicialmente como:

> **Clasificación binaria supervisada.**

```text
Datos del estudiante
        ↓
Modelo ML
        ↓
Academic_Failure_Risk
        ↓
0 / 1 + probabilidad
```

---

# 9. Algoritmos

Se compararán como mínimo tres modelos.

## 9.1 Logistic Regression

Baseline para establecer una referencia.

Ventajas:

- Simple.
- Rápida.
- Interpretable.
- Adecuada para clasificación binaria.

## 9.2 Random Forest

Modelo basado en múltiples árboles.

Ventajas:

- Captura relaciones no lineales.
- Funciona bien con datos tabulares.
- Permite analizar importancia de variables.

## 9.3 XGBoost

Candidato principal para datos tabulares.

Ventajas:

- Buen desempeño en clasificación.
- Captura relaciones no lineales e interacciones.
- Permite trabajar con problemas de clases desbalanceadas.

### Estrategia

```text
Logistic Regression
        ↓
Random Forest
        ↓
XGBoost
        ↓
Comparación
        ↓
Modelo ganador
```

No se utilizará Deep Learning en el MVP porque el dataset es tabular y la complejidad adicional no está justificada para el alcance universitario.

---

# 10. Metodología

```text
Problema
   ↓
Dataset
   ↓
Análisis exploratorio
   ↓
Limpieza
   ↓
Preprocesamiento
   ↓
División de datos
   ↓
Entrenamiento
   ↓
Evaluación
   ↓
Comparación
   ↓
Selección
   ↓
SHAP
   ↓
Aplicación
   ↓
Dashboard
```

## Etapa 1 — Recolección

Utilizar el dataset suministrado.

## Etapa 2 — Análisis exploratorio

Analizar:

- Estadística descriptiva.
- Distribuciones.
- Variables categóricas.
- Valores faltantes.
- Duplicados.
- Outliers.
- Distribución de clases.
- Correlaciones.
- Relación entre variables y objetivo.

## Etapa 3 — Preprocesamiento

- Eliminar `Student_ID` de las features.
- Tratar valores faltantes.
- Codificar variables categóricas.
- Escalar variables cuando sea necesario.
- Revisar outliers.
- Revisar data leakage.

## Etapa 4 — División

Propuesta:

```text
70 % → Entrenamiento
15 % → Validación
15 % → Prueba
```

La división será estratificada respecto a `Academic_Failure_Risk`.

## Etapa 5 — Entrenamiento

Entrenar:

```text
Logistic Regression
Random Forest
XGBoost
```

Se utilizarán pipelines reproducibles.

## Etapa 6 — Evaluación

Para clasificación:

- Accuracy.
- Precision.
- Recall.
- F1-score.
- ROC-AUC.
- PR-AUC.
- Matriz de confusión.

Debido al posible desbalance, **Accuracy no será la única métrica de decisión**.

## Etapa 7 — Comparación

| Modelo | Accuracy | Precision | Recall | F1 | ROC-AUC | PR-AUC |
|---|---:|---:|---:|---:|---:|---:|
| Logistic Regression | — | — | — | — | — | — |
| Random Forest | — | — | — | — | — | — |
| XGBoost | — | — | — | — | — | — |

## Etapa 8 — Selección

Se priorizarán:

1. F1-score.
2. Recall de la clase positiva.
3. Precision.
4. PR-AUC / ROC-AUC.
5. Interpretabilidad.
6. Complejidad.

---

# 11. Explainable AI

Se utilizará **SHAP (SHapley Additive exPlanations)** para interpretar las predicciones.

El sistema deberá poder responder:

> **¿Qué variables fueron más relevantes para este resultado?**

Ejemplo:

```text
Riesgo estimado: ALTO

Factores relevantes:

Academic Performance    ██████████
Sleep Hours             ████████
Burnout Level           ███████
Social Media            █████
Social Isolation        ████
```

SHAP se utilizará para:

- Importancia global.
- Explicación individual.
- Visualización de factores relevantes.

---

# 12. Motor de recomendaciones

Para mantener el proyecto pequeño, las recomendaciones se generarán mediante **reglas**, no mediante un LLM.

Ejemplo conceptual:

```text
SI Sleep_Hours < umbral
→ Recomendar revisar hábitos de sueño.

SI Daily_Social_Media_Hours > umbral
→ Recomendar revisar el tiempo destinado a redes sociales.

SI Physical_Activity_Hours < umbral
→ Recomendar incorporar actividad física.

SI Academic_Performance_Score < umbral
→ Recomendar priorizar planificación y seguimiento académico.
```

Los umbrales deberán definirse y justificarse en el proyecto.

Las recomendaciones serán generales y no constituirán diagnósticos.

---

# 13. Conclusión textual

La aplicación generará una conclusión a partir de:

- Predicción.
- Probabilidad.
- Parámetros.
- Factores relevantes.
- Reglas de recomendación.

Se recomienda inicialmente utilizar **plantillas dinámicas**, por ejemplo:

```text
El análisis identifica un nivel de riesgo académico
[BAJO/MODERADO/ALTO]. Los factores con mayor relevancia
en el resultado están relacionados con [FACTORES].

Se recomienda prestar especial atención a:
[RECOMENDACIONES].

Este resultado es orientativo y corresponde al comportamiento
aprendido por el modelo sobre el dataset utilizado.
```

No se incorporará un LLM en el MVP.

---

# 14. Dashboard

El dashboard tendrá cuatro bloques.

## 14.1 Resultado principal

```text
ACADEMIC FAILURE RISK

72 %

ALTO
```

## 14.2 Parámetros

Mostrar:

- Redes sociales.
- Uso de IA.
- Sueño.
- Actividad física.
- Mental Health Score.
- Physical Health Score.
- Social Isolation Score.
- Burnout.
- Academic Performance.

## 14.3 Factores relevantes

Gráfico de barras con las variables más influyentes.

## 14.4 Recomendaciones

Mostrar entre 3 y 5 recomendaciones priorizadas.

## 14.5 Conclusión

Mostrar el texto generado dinámicamente.

---

# 15. Formulario

El usuario ingresará:

### Información básica

- Edad.
- Género.
- Nivel educativo.

### Hábitos digitales

- Horas diarias de redes sociales.
- Horas diarias de herramientas de IA.

### Hábitos y bienestar

- Horas de sueño.
- Horas de actividad física.
- Mental Health Score.
- Physical Health Score.
- Social Isolation Score.
- Burnout Level.

### Información académica

- Academic Performance Score.

**Importante:** `Academic_Failure_Risk` no se solicita al usuario porque es la variable objetivo.

---

# 16. Arquitectura

```text
┌─────────────────────────────┐
│          STREAMLIT          │
│         FORMULARIO          │
└──────────────┬──────────────┘
               ↓
┌─────────────────────────────┐
│       PREPROCESAMIENTO      │
│        Scikit-learn         │
└──────────────┬──────────────┘
               ↓
┌─────────────────────────────┐
│       MODELO ENTRENADO      │
│     XGBoost / ganador       │
└──────────────┬──────────────┘
               ↓
       ┌───────┴────────┐
       ↓                ↓
   ┌────────┐     ┌──────────────┐
   │  SHAP  │     │ RULE ENGINE  │
   └────┬───┘     └──────┬───────┘
        └────────┬────────┘
                 ↓
        ┌──────────────────┐
        │    DASHBOARD     │
        │                  │
        │ Predicción       │
        │ Parámetros       │
        │ Factores         │
        │ Recomendaciones  │
        │ Conclusión       │
        └──────────────────┘
```

---

# 17. Tecnologías

| Necesidad | Tecnología |
|---|---|
| Lenguaje | Python 3.11+ |
| Datos | Pandas |
| Cálculo | NumPy |
| ML | Scikit-learn |
| Gradient Boosting | XGBoost |
| Explainability | SHAP |
| Gráficos | Plotly |
| Dashboard | Streamlit |
| Persistencia | Joblib |
| Notebook | Jupyter |
| IDE | VS Code |
| Control de versiones | Git/GitHub |

## ¿Por qué Streamlit?

Es la opción recomendada porque permite crear el formulario y dashboard directamente en Python, reduciendo considerablemente el tiempo de desarrollo.

Por el alcance del proyecto **no se recomienda inicialmente React + FastAPI**.

---

# 18. Estructura del proyecto

```text
student-ai/
│
├── data/
│   └── AI_SocialMedia_Student_Health_Dataset_clean.csv
│
├── notebooks/
│   ├── 01_eda.ipynb
│   ├── 02_preprocessing.ipynb
│   ├── 03_model_training.ipynb
│   └── 04_model_evaluation.ipynb
│
├── src/
│   ├── preprocessing.py
│   ├── train.py
│   ├── predict.py
│   ├── explainability.py
│   └── recommendations.py
│
├── models/
│   └── best_model.pkl
│
├── app/
│   └── app.py
│
├── reports/
│   ├── figures/
│   └── results/
│
├── requirements.txt
├── README.md
└── CONTEXT_MASTER_PROJECT.md
```

---

# 19. Requisitos funcionales

| ID | Requisito |
|---|---|
| RF-01 | Mostrar formulario |
| RF-02 | Validar datos |
| RF-03 | Preprocesar información |
| RF-04 | Ejecutar modelo |
| RF-05 | Calcular riesgo académico |
| RF-06 | Mostrar probabilidad |
| RF-07 | Mostrar parámetros |
| RF-08 | Mostrar factores relevantes |
| RF-09 | Generar recomendaciones |
| RF-10 | Generar conclusión |

---

# 20. Requisitos no funcionales

| ID | Requisito |
|---|---|
| RNF-01 | Interfaz sencilla |
| RNF-02 | Predicción en pocos segundos |
| RNF-03 | Código reproducible |
| RNF-04 | Modelo separado de interfaz |
| RNF-05 | Resultados interpretables |
| RNF-06 | No presentar resultados como diagnóstico |
| RNF-07 | Ejecución local |

---

# 21. Entregable 1 – Proyecto de Sistemas Inteligentes

## 21.1 Definición del problema

El proyecto aborda el desarrollo de un sistema inteligente capaz de estimar el riesgo académico de un estudiante utilizando información relacionada con hábitos digitales, sueño, actividad física, bienestar, aislamiento social, burnout y desempeño académico.

La técnica principal será **Machine Learning supervisado para clasificación binaria**.

### Pregunta problema

> ¿Es posible desarrollar un sistema inteligente basado en Machine Learning que, a partir de información sobre hábitos digitales, sueño, actividad física, bienestar y desempeño académico, estime el riesgo académico de un estudiante y genere una conclusión con recomendaciones personalizadas?

## 21.2 Justificación

La solución integra diferentes variables en un único análisis y permite aplicar Machine Learning para identificar patrones presentes en datos históricos.

Los principales aportes serán:

- Análisis automatizado.
- Predicción.
- Explicabilidad.
- Dashboard.
- Recomendaciones.
- Conclusión comprensible.

## 21.3 Objetivos

### General

> Desarrollar un sistema inteligente basado en Machine Learning que permita estimar el riesgo académico de un estudiante a partir de variables relacionadas con sus hábitos digitales, bienestar, actividad física, sueño y desempeño académico, generando una interpretación visual y textual de los resultados.

### Específicos

1. Analizar las características y calidad de los datos disponibles.
2. Preparar los datos necesarios para entrenar modelos.
3. Implementar y comparar algoritmos de clasificación.
4. Evaluar los modelos mediante métricas apropiadas.
5. Implementar el prototipo web con predicción, explicación y recomendaciones.

## 21.4 Datos

Se utilizará el dataset suministrado con 15,000 registros y 14 variables.

Se deberá documentar:

- Fuente.
- Registros.
- Variables.
- Tipos.
- Faltantes.
- Duplicados.
- Outliers.
- Distribución de clases.
- Calidad.
- Data leakage.

## 21.5 Metodología

**Problema → Recolección → Exploración → Limpieza → Preprocesamiento → División → Entrenamiento → Evaluación → Comparación → Selección → Implementación**

Se compararán:

- Logistic Regression.
- Random Forest.
- XGBoost.

---

# 22. ¿Por qué no utilizar LLM?

Aunque la asignatura permite Machine Learning, Deep Learning, NLP o LLM, no es necesario utilizar todas estas tecnologías.

El problema principal es una **clasificación sobre datos tabulares**, por lo que Machine Learning tradicional es más apropiado.

El uso de un LLM únicamente para redactar la conclusión aumentaría la complejidad y no mejoraría necesariamente el modelo predictivo.

Por ello, el MVP utilizará:

> **Machine Learning + SHAP + reglas + plantillas dinámicas.**

Un LLM podría ser una extensión futura.

---

# 23. Criterios de éxito

El proyecto será exitoso si:

- El dataset se procesa correctamente.
- Se documenta el EDA.
- Se revisa data leakage.
- Se comparan al menos tres modelos.
- Se utilizan métricas adecuadas.
- Se selecciona un modelo.
- Se realizan predicciones sobre nuevos registros.
- Existe un formulario funcional.
- Existe un dashboard.
- Se muestran factores relevantes.
- Se generan recomendaciones.
- Se genera una conclusión.
- El grupo puede explicar técnicamente el funcionamiento.

---

# 24. Cronograma sugerido

## Fase 1 — Datos

- EDA.
- Calidad.
- Distribución.
- Data leakage.

## Fase 2 — ML

- Preprocesamiento.
- División.
- Entrenamiento.
- Evaluación.

## Fase 3 — Explicabilidad

- SHAP.
- Importancia global.
- Explicación individual.

## Fase 4 — Aplicación

- Formulario.
- Predicción.
- Dashboard.
- Recomendaciones.
- Conclusión.

## Fase 5 — Entrega

- Estado del arte.
- Resultados.
- Conclusiones.
- Presentación.

---

# 25. Resultado final esperado

El estudiante ingresará sus datos:

```text
FORMULARIO
    ↓
ANÁLISIS ML
    ↓
RIESGO ACADÉMICO
    ↓
PROBABILIDAD
    ↓
FACTORES RELEVANTES
    ↓
RECOMENDACIONES
    ↓
CONCLUSIÓN
```

El sistema final debe sentirse como una herramienta sencilla:

> **"Ingresa tus datos → Analiza tu perfil → Comprende los factores → Recibe recomendaciones."**

---

# 26. Nota metodológica final

El proyecto deberá diferenciar claramente entre **correlación/predicción** y **causalidad**.

Si el modelo identifica que una variable es importante, esto no significa que dicha variable sea necesariamente la causa del riesgo académico.

El sistema debe presentarse como un modelo predictivo experimental entrenado con el dataset disponible.

---

**Fin del Context Master Project**
