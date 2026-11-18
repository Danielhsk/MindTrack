# Guión de presentación — MindTrack (10 diapositivas)

**Fuente:** `MindTrack.pdf` (defensa 2026)  
**Autores:** Geraldin Pérez · Daniel Hernández · Prof. Andrés Felipe Duque (Sistemas Inteligentes)

> Cada slide incluye **Qué decir** (hablado) y **Si preguntan** (términos). Tiempo total orientativo: **12–15 min** + demo **3–5 min**.

---

## Diapositiva 1 — Portada  
*MindTrack · Del dato al prototipo web defendible*

**Qué decir (≈40 s)**  
“Presentamos **MindTrack**, sistema inteligente de bienestar y **riesgo académico** para la asignatura Sistemas Inteligentes. Somos Geraldin Pérez y Daniel Hernández. El proyecto va **del dato al prototivo web**: modelo entrenado, aplicación en **Streamlit** y repositorio público en GitHub. La demo está en **mindtrack-si.streamlit.app**. Hoy mostramos el problema, los datos, la metodología, resultados, arquitectura y cierre ético.”

**Si preguntan**  
- **Prototipo web defendible:** producto demostrable con código, métricas y despliegue, no solo notebooks.

---

## Diapositiva 2 — Planteamiento del problema  
*Problema y propuesta de valor*

**Qué decir (≈1 min 20 s)**  
“El **contexto** es real: más redes, más IA, menos sueño y más **burnout**. Hoy muchas intervenciones llegan **tarde**, cuando ya hay notas reprobatorias.  
**MindTrack** propone algo **preventivo**: estimar **probabilidad de riesgo** con hábitos y bienestar, **sin usar calificaciones previas** en el modelo de producción —evitamos que el sistema ‘copie’ la nota.  
El **valor**: alerta temprana, gráfico **SHAP** de factores y **recomendaciones** por reglas.  
Dejamos claro el **marco ético**: no es diagnóstico clínico, no reemplaza psicología ni tutoría formal; no hay login ni integración con sistemas de la universidad.”

**Si preguntan**  
- **SHAP:** explica qué variables empujan esta predicción (ver slide 8).  
- **Preventivo vs reactivo:** sin `Academic_Performance_Score` en producción = escenario antes del fracaso visible en notas.

---

## Diapositiva 3 — Formulación del dataset  
*Una alerta temprana, no exactitud global*

**Qué decir (≈1 min 20 s)**  
“Tenemos **15.000 perfiles**, sin nulos ni duplicados. Solo **~6 %** está en riesgo: la clase positiva es minoritaria. Por eso insistimos: **no basta la exactitud global** —si el modelo siempre dijera ‘sin riesgo’ tendría ~**94 % accuracy** y **no detectaría** a nadie vulnerable.  
Usamos **11 variables** de hábitos y bienestar en el formulario; en el dataset hay 14 columnas, pero excluimos **Student_ID** y **Academic_Performance_Score** por identificador y **data leakage**.  
Retenemos edad, género, educación, redes, IA, sueño, actividad física, salud mental y física, aislamiento y burnout.”

**Si preguntan**  
- **Data leakage:** la nota estaría demasiado ligada al objetivo; inflaría métricas y no sería realista para alerta temprana.  
- **Academic_Failure_Risk:** target binario 0/1 del dataset.

---

## Diapositiva 4 — Ciclo de vida del proyecto  
*Del diseño al producto desplegado*

**Qué decir (≈1 min)**  
“Seguimos **cinco fases**:  
1) **Diseño** — objetivo de **recall ≥ 0,85**, sin fuga de información;  
2) **Preparación** — EDA, partición **70/15/15**, baseline logística;  
3) **Modelado** — LR, Random Forest, XGBoost y **sintonización de umbral**;  
4) **Software** — módulos, **SHAP**, motor de **reglas**;  
5) **Producto** — **Streamlit Cloud**, vistas **PRD** y **LAB**.  
El pipeline académico es: datos → EDA → preprocesamiento → entrenamiento → evaluación → predicción → explicación → visualización.”

**Si preguntan**  
- **Baseline:** regresión logística como referencia lineal simple antes de árboles.  
- **PRD/LAB:** consulta en vivo vs laboratorio de evidencia del experimento.

---

## Diapositiva 5 — Metodología experimental  
*Protocolo para validar y probar*

**Qué decir (≈1 min 20 s)**  
“Partimos **estratificadamente** con `random_state=42`:  
- **Train 70 %** — 10.500, ajuste de modelos;  
- **Validation 15 %** — 2.250, **comparación** y **elección de umbral**;  
- **Test 15 %** — 2.250, evaluación final **sin retocar** umbrales.  
**Burnout** va con **codificación ordinal** Low=0 … Severe=3 porque el orden importa. **Género** y **educación** con **one-hot** porque son categorías sin orden fijo.  
Solo los modelos **lineales** llevan **escalado estándar**; los árboles trabajan con las features ya transformadas.”

**Si preguntan**  
- **Ordinal:** un número que respeta severidad creciente.  
- **One-hot:** columnas 0/1 por categoría (con categoría referencia omitida).  
- **Umbral:** no usamos 0,5 fijo; se calibra en validación.

---

## Diapositiva 6 — Espacio de hipótesis  
*De una línea a conjuntos de árboles*

**Qué decir (≈1 min 30 s)**  
“Probamos **tres familias**:  
**Regresión logística** — línea base rápida; frontera lineal; umbral alto ~0,90; FN 20, FP 31.  
**Random Forest** — **300 árboles en paralelo**, más **recall**, menos FN (17), pero más **falsas alarmas** (FP 47); umbral ~0,42.  
**XGBoost** — **300 árboles en serie** que corrigen errores (**boosting**), learning rate bajo; FN 19, FP 43; umbral ~0,73.  
**Criterio rector:** **recall clase 1 ≥ 0,85** para no omitir estudiantes en riesgo; también miramos precisión, **F1** y **PR-AUC**.”

**Si preguntan**  
- **FN / FP:** falso negativo = no detectamos riesgo; falso positivo = alerta innecesaria.  
- **PR-AUC:** qué tan bien **ordena** de más a menos riesgo entre umbrales; **no** elige el corte.  
- **F1:** desempeño en el **umbral ya elegido** (equilibrio precisión–recall).  
- **Boosting vs bosque:** RF promedia árboles independientes; XGBoost suma correcciones secuenciales.

---

## Diapositiva 7 — Resultados empíricos  
*Validación vs test · decisión con datos*

**Qué decir (≈1 min 30 s)**  
“En **validación** (2.250 casos), los tres cumplen recall ≥ 0,85. **Logistic Regression** gana **F1 (0,819)** y tiene **menos alertas falsas (FP 31)**; RF el menor FN pero más ruido; XGBoost queda en el medio.  
En **test** evaluamos **los tres** con el mismo umbral de validación, sin re-ajuste: LR F1 0,801; RF recall 0,911 pero FP 46; **XGBoost F1 0,824 y PR-AUC 0,933** (recall 0,881, FN 16, FP 35).  
Criterio de producción: recall ≥ 0,85 en test, luego F1 → PR-AUC → precisión → menos FP → menos FN. Por eso el motor oficial es **XGBoost**, aunque LR gane solo en validación.”

**Si preguntan**  
- ¿Por qué no LR si menos FP en validación? Porque la elección oficial usa **test** (generalización).  
- ¿Por qué no RF si FN=12 en test? Más FP (46); pierde en F1 frente a XGB.  
- **Test inédito** para calibrar τ; solo para comparar modelos.

---

## Diapositiva 8 — Arquitectura del sistema  
*Predicción y explicación*

**Qué decir (≈1 min 30 s)**  
“**PRD:** el usuario llena el formulario → **preprocesamiento** → **pipeline joblib** XGBoost → probabilidad comparada con **umbral ~0,73** en `metadata.json` → decisión y bandas de riesgo.  
**Segunda opinión:** LR, RF y XGB informativos, sin cambiar la decisión oficial.  
**SHAP TreeExplainer:** barras ‘**Factores que empujan el estado**’ en **esta** consulta.  
**Reglas:** sueño, redes, actividad, salud mental, aislamiento, burnout → tarjetas de recomendación y disclaimer.  
**LAB:** EDA, trazabilidad del entrenamiento, tablas y **matrices de confusión** —solo lectura, sin reentrenar en servidor.”

**Si preguntan**  
- **joblib:** archivo del modelo entrenado listo para `predict_proba`.  
- **Explicabilidad local:** SHAP por estudiante, no causalidad.  
- **Reglas deterministas:** no es ChatGPT; son umbrales fijos del proyecto.

**Demo sugerida (3 min)**  
Perfil alerta → ejecutar consulta → mostrar estado, segunda opinión, SHAP, recomendación → cambiar a LAB → Arena de modelos.

---

## Diapositiva 9 — Despliegue y reproducibilidad

**Qué decir (≈1 min)**  
“Desplegamos con **Docker** (`docker compose up`) o **Streamlit Cloud**. Artefactos versionados: pipelines, `metadata.json`, `comparison_test.csv`; **no reentrenamos** al abrir la app.  
Reproducibilidad: `pip install -r requirements.txt`, `python scripts/train_and_export.py`, `streamlit run app/streamlit_app.py` — o solo Docker con la imagen del repo.”

**Si preguntan**  
- **Reproducibilidad:** mismo `random_state=42` y script único de exportación.  
- **Keep-alive:** GitHub Actions visita la URL pública con automatización.

---

## Diapositiva 10 — Síntesis y consideraciones éticas

**Qué decir (≈1 min)**  
“**Logros:** MVP de alerta temprana sin nota previa; XGBoost con recall **0,881** en test; **SHAP** y reglas; doble vista PRD para orientación y LAB para auditoría.  
**Ética:** datos observacionales —**correlación no es causa**; sin credenciales ni registro institucional; herramienta de **orientación preventiva**, no reemplazo de profesionales.  
Gracias; abrimos preguntas. Repo **Danielhsk/MindTrack** y app **mindtrack-si.streamlit.app**.”

---

## Reparto sugerido (2 personas)

| Slides | Contenido | Quién |
|--------|-----------|--------|
| 1–2 | Portada y problema | Geraldin |
| 3–5 | Datos, ciclo, metodología | Daniel |
| 6–7 | Modelos y resultados | Geraldin |
| 8–9 | Arquitectura, demo, deploy | Daniel |
| 10 | Cierre ético | Ambos / Geraldin |

---

## Cheat sheet — respuestas de 10 segundos

| Pregunta | Respuesta |
|----------|-----------|
| ¿PR-AUC elige el 0,85 de recall? | **No.** El umbral se elige en validación con recall ≥ 0,85 y max F1. |
| ¿Qué es PR-AUC? | Qué tan bien **ordena** el riesgo entre modelos. |
| ¿Qué es F1? | Rendimiento en **un** umbral ya calibrado. |
| ¿Por qué sin nota? | Preventivo + evitar leakage. |
| ¿Dónde se ve SHAP? | PRD, gráfico de barras bajo ‘Factores que empujan el estado’. |
| ¿La app entrena sola? | **No**; modelos en `models/`. |

---

*Alineado a `MindTrack.pdf` (10 páginas). Actualizar cifras si se reentrena el proyecto.*