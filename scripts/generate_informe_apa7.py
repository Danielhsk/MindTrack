"""Genera informe Word APA 7 para MindTrack."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml.ns import qn
from docx.shared import Inches, Pt

ROOT = Path(__file__).resolve().parents[1]
LOGO = ROOT / "docs" / "assets" / "ecci-logo.jpg"
OUT = ROOT / "docs" / "Informe_MindTrack_APA7.docx"
ENTREGABLE2_CANDIDATES = [
    Path(
        r"C:\Users\dsher\Downloads\MindTrack - Entregable 2_ Validación, "
        r"Análisis Exploratorio, Preparación de Datos y Métricas (1).docx"
    ),
    ROOT / "docs" / "source" / "MindTrack_Entregable2.docx",
]
def resolve_entregable2_path() -> Path | None:
    for path in ENTREGABLE2_CANDIDATES:
        if path.exists():
            return path
    return None
FIGURES_DIR = ROOT / "reports" / "figures"
IMAGES_DIR = ROOT / "Imagenes"
E2_ASSETS = ROOT / "docs" / "assets" / "entregable2"
COMPARISON_CSV = ROOT / "reports" / "comparison_validation.csv"
TEST_CSV = ROOT / "reports" / "comparison_test.csv"
TEST_PROD_CSV = ROOT / "reports" / "evaluation_test_production.csv"
TEST_PROD_CSV_LEGACY = ROOT / "reports" / "evaluation_test_xgboost.csv"

_table_counter = 0
_figure_counter = 0
_seen_image_hashes: set[str] = set()


def set_document_defaults(doc: Document) -> None:
    for section in doc.sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)
    style = doc.styles["Normal"]
    font = style.font
    font.name = "Times New Roman"
    font.size = Pt(12)
    pf = style.paragraph_format
    pf.line_spacing_rule = WD_LINE_SPACING.DOUBLE
    pf.space_after = Pt(0)
    pf.space_before = Pt(0)


def _run_font(run, bold=False, italic=False, size=12):
    run.font.name = "Times New Roman"
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run._element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")


def center_paragraph(doc: Document, text: str, *, bold=False, size=12) -> None:
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(text)
    _run_font(run, bold=bold, size=size)


def body(doc: Document, text: str) -> None:
    p = doc.add_paragraph(text)
    p.paragraph_format.first_line_indent = Inches(0.5)


def heading1(doc: Document, text: str) -> None:
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(text)
    _run_font(run, bold=True)


def heading2(doc: Document, text: str) -> None:
    p = doc.add_paragraph()
    run = p.add_run(text)
    _run_font(run, bold=True)


def heading3(doc: Document, text: str) -> None:
    p = doc.add_paragraph()
    run = p.add_run(text)
    _run_font(run, bold=True, italic=True)


def page_break(doc: Document) -> None:
    doc.add_page_break()


def load_table_from_doc(doc_path: Path, table_index: int) -> list[list[str]]:
    source = Document(str(doc_path))
    table = source.tables[table_index]
    return [[cell.text.strip().replace("\n", " ") for cell in row.cells] for row in table.rows]


def add_apa_table(doc: Document, title: str, rows: list[list[str]], *, font_size: int = 10) -> None:
    global _table_counter
    _table_counter += 1
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
    run = p.add_run(f"Tabla {_table_counter}\n{title}")
    _run_font(run, bold=True, size=12)

    cols = max(len(r) for r in rows) if rows else 1
    table = doc.add_table(rows=len(rows), cols=cols)
    table.style = "Table Grid"
    for i, row in enumerate(rows):
        for j in range(cols):
            val = row[j] if j < len(row) else ""
            cell = table.rows[i].cells[j]
            cell.text = val
            for paragraph in cell.paragraphs:
                paragraph.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
                for r in paragraph.runs:
                    _run_font(r, size=font_size)
    note = doc.add_paragraph()
    note.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
    note.paragraph_format.space_after = Pt(12)
    doc.add_paragraph()


def add_apa_figure(
    doc: Document,
    image_path: Path,
    caption: str,
    *,
    width: float = 5.8,
) -> None:
    global _figure_counter
    if not image_path.exists():
        return
    digest = __import__("hashlib").md5(image_path.read_bytes()).hexdigest()
    if digest in _seen_image_hashes:
        return
    _seen_image_hashes.add(digest)
    _figure_counter += 1
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
    run = p.add_run()
    run.add_picture(str(image_path), width=Inches(width))
    cap = doc.add_paragraph()
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
    cap.paragraph_format.space_after = Pt(12)
    cr = cap.add_run(f"Figura {_figure_counter}. {caption}")
    _run_font(cr, italic=True, size=12)
    doc.add_paragraph()


def insert_entregable2_tables(doc: Document) -> None:
    e2_path = resolve_entregable2_path()
    if e2_path is None:
        body(
            doc,
            "Las tablas detalladas del análisis exploratorio se encuentran en el notebook "
            "MindTrack_EDA_Preprocesamiento y en reports/ del repositorio del proyecto.",
        )
        return

    specs = [
        (0, "Marco del proyecto MindTrack"),
        (1, "Diccionario de datos: variables, tipos y descripción"),
        (2, "Análisis de valores atípicos y decisión metodológica"),
        (3, "Estadísticos descriptivos de variables numéricas"),
        (4, "Frecuencias de variables categóricas y burnout"),
        (5, "Correlación de Pearson con Academic_Failure_Risk"),
        (6, "Riesgo académico según nivel de burnout"),
        (7, "Balance de la variable objetivo"),
        (8, "Partición estratificada del dataset (train / validation / test)"),
        (9, "Jerarquía de métricas de evaluación"),
    ]
    for idx, title in specs:
        rows = load_table_from_doc(e2_path, idx)
        fs = 8 if max(len(r) for r in rows) > 5 else 9
        add_apa_table(doc, title, rows, font_size=fs)


def insert_eda_figures(doc: Document) -> None:
    heading2(doc, "Figuras del análisis exploratorio")
    body(
        doc,
        "Las figuras siguientes sintetizan el análisis exploratorio: balance de la variable objetivo, "
        "distribuciones, correlaciones, relación con el riesgo y diagramas por categorías.",
    )
    colab = ROOT / "assets" / "colab"
    eda_figs = [
        (
            colab / "eda-target-balance.jpeg",
            IMAGES_DIR / "diagrama variable objetivo.jpeg",
            "Distribución de la variable objetivo (Academic_Failure_Risk).",
        ),
        (
            colab / "eda-histogram.jpeg",
            IMAGES_DIR / "Histograma.jpeg",
            "Histogramas de variables numéricas del dataset.",
        ),
        (
            colab / "eda-distribution.jpeg",
            IMAGES_DIR / "Grafica distribucion.jpeg",
            "Distribución de características numéricas.",
        ),
        (
            colab / "eda-correlation-matrix.jpeg",
            IMAGES_DIR / "Matriz correlacion.jpeg",
            "Matriz de correlación de Pearson entre variables.",
        ),
        (
            colab / "eda-academic-risk.jpeg",
            IMAGES_DIR / "Riesgo academico.jpeg",
            "Asociación de variables con el riesgo académico.",
        ),
        (
            colab / "eda-boxplot.jpeg",
            IMAGES_DIR / "Boxplot.jpeg",
            "Diagramas de caja por categorías (burnout, educación, género).",
        ),
        (
            colab / "eda-boxplot-alt.jpeg",
            IMAGES_DIR / "Boxplot2.jpeg",
            "Diagramas de caja complementarios del EDA.",
        ),
    ]
    for primary, fallback, caption in eda_figs:
        path = primary if primary.exists() else fallback
        add_apa_figure(doc, path, caption)


def insert_model_tables_and_figures(doc: Document) -> None:
    heading2(doc, "Resultados del experimento de modelos")
    body(
        doc,
        "Las tablas y figuras siguientes sintetizan la comparación Logistic Regression, Random Forest "
        "y XGBoost en validación, con umbrales calibrados para recall ≥ 0,85, y la evaluación "
        "comparativa de los tres en el conjunto de prueba (mismos umbrales, sin re-ajuste).",
    )
    if COMPARISON_CSV.exists():
        df = pd.read_csv(COMPARISON_CSV)
        cols_show = [
            "Modelo",
            "Umbral",
            "Recall (C1)",
            "Precision (C1)",
            "F1-Score (C1)",
            "PR-AUC",
            "ROC-AUC",
            "FN",
            "FP",
            "TP",
            "TN",
        ]
        df = df[cols_show]
        for col in df.select_dtypes(include="float").columns:
            if col != "Umbral":
                df[col] = df[col].map(lambda x: f"{x:.3f}")
            else:
                df[col] = df[col].map(lambda x: f"{x:.3f}")
        rows = [cols_show] + df.astype(str).values.tolist()
        add_apa_table(doc, "Comparación de modelos en validación (umbrales calibrados)", rows, font_size=8)

    if TEST_CSV.exists():
        df = pd.read_csv(TEST_CSV)
        cols_show = [
            "Modelo",
            "Recall (C1)",
            "Precision (C1)",
            "F1-Score (C1)",
            "PR-AUC",
            "FN",
            "FP",
            "TP",
            "TN",
            "Cumple Recall",
        ]
        df = df[[c for c in cols_show if c in df.columns]]
        for col in df.select_dtypes(include="float").columns:
            df[col] = df[col].map(lambda x: f"{x:.3f}")
        rows = [df.columns.tolist()] + df.astype(str).values.tolist()
        add_apa_table(doc, "Comparación de modelos en prueba (umbrales de validación)", rows, font_size=8)

    prod_path = (
        TEST_PROD_CSV
        if TEST_PROD_CSV.exists()
        else (TEST_PROD_CSV_LEGACY if TEST_PROD_CSV_LEGACY.exists() else None)
    )
    if prod_path is not None:
        df = pd.read_csv(prod_path)
        label = str(df.iloc[0].get("Modelo", "Producción"))
        rows = [df.columns.tolist()] + [
            [
                f"{v:.3f}" if isinstance(v, float) and c != "Modelo" else str(v)
                for c, v in zip(df.columns, df.iloc[0])
            ]
        ]
        add_apa_table(doc, f"Modelo de producción en prueba — {label}", rows, font_size=9)

    model_figs = [
        (FIGURES_DIR / "metrics_validation.png", "Métricas de validación por modelo."),
        (FIGURES_DIR / "confusion_validation.png", "Matrices de confusión en validación."),
        (FIGURES_DIR / "pr_curves_validation.png", "Curvas precision–recall (validación)."),
        (FIGURES_DIR / "fn_fp_validation.png", "Falsos negativos versus falsos positivos."),
        (FIGURES_DIR / "heatmap_validation.png", "Mapa de calor de métricas en validación."),
        (FIGURES_DIR / "metrics_test.png", "Métricas en prueba por modelo."),
        (FIGURES_DIR / "fn_fp_test.png", "Falsos negativos y positivos en prueba."),
        (FIGURES_DIR / "heatmap_test.png", "Mapa de calor de métricas en prueba."),
    ]
    for path, cap in model_figs:
        add_apa_figure(doc, path, cap, width=6.2)


def title_page(doc: Document) -> None:
    if LOGO.exists():
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run()
        run.add_picture(str(LOGO), width=Inches(2.8))
        doc.add_paragraph()

    center_paragraph(
        doc,
        "MindTrack: Sistema Inteligente de Estimación de Riesgo Académico Estudiantil",
        bold=True,
        size=12,
    )
    doc.add_paragraph()
    center_paragraph(doc, "Daniel Hernández")
    center_paragraph(doc, "Geraldin Pérez")
    doc.add_paragraph()
    center_paragraph(doc, "Universidad ECCI")
    doc.add_paragraph()
    center_paragraph(doc, "Sistemas Inteligentes")
    doc.add_paragraph()
    center_paragraph(doc, "Profesor: Andrés Felipe Duque")
    doc.add_paragraph()
    center_paragraph(doc, "17 de noviembre de 2026")


def build_content(doc: Document) -> None:
    page_break(doc)
    heading1(doc, "Resumen")
    body(
        doc,
        "MindTrack es un prototipo académico que estima la probabilidad de riesgo académico "
        "(variable Academic_Failure_Risk) a partir de hábitos digitales, sueño, actividad física, "
        "indicadores de bienestar, aislamiento social y burnout, en un escenario preventivo que "
        "excluye la nota académica directa para evitar fuga de información (data leakage). "
        "Se trabajó con 15.000 registros y 14 variables; la clase en riesgo representa aproximadamente "
        "el 6 % del conjunto. El pipeline incluye exploración de datos, preprocesamiento, partición "
        "estratificada 70/15/15, entrenamiento comparativo de regresión logística, Random Forest y "
        "XGBoost, y calibración de umbrales en validación con objetivo de recall ≥ 0,85 en la clase "
        "positiva. XGBoost se adoptó como modelo de producción por cumplir el criterio y generalizar "
        "en prueba (recall ≈ 0,88; PR-AUC ≈ 0,93). La solución se desplegó en Streamlit con dos modos: "
        "consulta en vivo (XGBoost, explicación SHAP, reglas de recomendación) y laboratorio de "
        "trazabilidad del experimento. El sistema es orientativo y no sustituye acompañamiento "
        "institucional ni diagnóstico clínico.",
    )
    kw = doc.add_paragraph()
    kw.paragraph_format.first_line_indent = Inches(0.5)
    r1 = kw.add_run("Palabras clave: ")
    _run_font(r1, bold=True, italic=True)
    r2 = kw.add_run(
        "riesgo académico, aprendizaje supervisado, XGBoost, Random Forest, "
        "explicabilidad, Streamlit"
    )
    _run_font(r2, italic=True)

    page_break(doc)
    heading1(doc, "Introducción")
    body(
        doc,
        "El rendimiento académico de los estudiantes puede relacionarse con múltiples dimensiones "
        "del bienestar y del uso de tecnologías digitales, más allá de indicadores puntuales de "
        "desempeño. En la asignatura Sistemas Inteligentes se plantea el desarrollo de un sistema "
        "capaz de integrar variables de hábitos y salud estudiantil y entregar una estimación "
        "probabilística de riesgo académico, acompañada de visualización e interpretación en "
        "lenguaje accesible. El producto resultante se denominó MindTrack (documentación interna "
        "StudentAI).",
    )
    body(
        doc,
        "La pregunta problema que orienta el proyecto es: ¿es posible desarrollar un sistema "
        "inteligente basado en machine learning que, a partir de información sobre hábitos digitales, "
        "sueño, actividad física y bienestar, estime el riesgo académico de un estudiante y genere "
        "recomendaciones personalizadas de orientación? El objetivo general consiste en implementar "
        "ese ciclo completo —datos, modelado, evaluación, predicción, explicación y despliegue— en un "
        "prototipo web defendible en contexto universitario.",
    )
    e2_path = resolve_entregable2_path()
    if e2_path is not None:
        marco = load_table_from_doc(e2_path, 0)
        prob = next((r[1] for r in marco if r[0] == "Problema Seleccionado"), None)
        if prob:
            body(doc, prob)
    body(
        doc,
        "El informe documenta de forma coherente las fases de diseño, análisis exploratorio, "
        "preprocesamiento, entrenamiento y comparación de modelos (con énfasis en la construcción "
        "de árboles de decisión y ensembles), selección del modelo de producción, desarrollo de la "
        "aplicación Streamlit y despliegue. Se enfatizan las decisiones metodológicas (exclusión de "
        "Academic_Performance_Score, métrica de recall) y las consideraciones éticas del uso "
        "orientativo del sistema.",
    )

    heading1(doc, "Marco Conceptual y Alcance")
    heading2(doc, "Clasificación supervisada y alerta temprana")
    body(
        doc,
        "El problema se formuló como clasificación binaria supervisada: dado un vector de "
        "características x, estimar P(y=1|x), donde y=1 indica presencia de riesgo académico según "
        "el criterio del dataset. En escenarios con clase minoritaria en riesgo, la exactitud global "
        "es engañosa; por ello se priorizó el recall de la clase positiva (capacidad de detectar "
        "estudiantes en riesgo) y métricas como F1, precision y PR-AUC.",
    )
    heading2(doc, "Alcance del MVP")
    body(
        doc,
        "El alcance incluye formulario web, validación de entradas, pipelines de ML exportados, "
        "dashboard con modo producción y modo laboratorio, explicabilidad local mediante SHAP, "
        "motor de recomendaciones basado en reglas y conclusión textual. Quedaron fuera de alcance "
        "login multiusuario, integraciones institucionales, bases de datos empresariales, modelos "
        "generativos de lenguaje y diagnóstico clínico.",
    )

    heading1(doc, "Metodología")
    heading2(doc, "Diseño de la investigación")
    body(
        doc,
        "Se siguió un diseño de desarrollo experimental replicable: (1) auditoría y EDA del dataset; "
        "(2) preprocesamiento documentado en código y notebooks; (3) entrenamiento offline de tres "
        "modelos con el mismo split; (4) selección de umbrales en validación; (5) evaluación final en "
        "prueba solo para el modelo de producción; (6) empaquetado en aplicación Streamlit; (7) "
        "despliegue en Streamlit Community Cloud con automatización de mantenimiento de disponibilidad.",
    )
    heading2(doc, "Dataset y variables")
    body(
        doc,
        "El archivo data/academic_risk_dataset.csv contiene 15.000 filas y 14 columnas. La variable "
        "objetivo es Academic_Failure_Risk (0 sin riesgo, 1 en riesgo), con prevalencia aproximada "
        "del 6 %. Las variables de entrada incluyen edad, género, nivel educativo, horas diarias en "
        "redes sociales y en herramientas de IA, horas de sueño, actividad física, puntajes de salud "
        "mental y física, aislamiento social y nivel de burnout. Se excluyeron Student_ID (identificador) "
        "y Academic_Performance_Score (riesgo de data leakage en escenario preventivo).",
    )
    heading2(doc, "Calidad de datos y análisis exploratorio")
    body(
        doc,
        "El análisis exploratorio (notebook MindTrack_EDA_Preprocesamiento) reportó 0 % de valores "
        "faltantes y 0 % de duplicados. Se generaron histogramas, boxplots, análisis del balance del "
        "target, tablas de correlación y gráficos por nivel de burnout. El desbalance motivó pesos de "
        "clase y la elección de PR-AUC. Los valores atípicos se conservaron de forma deliberada, dado "
        "que los modelos basados en árboles pueden modelar regiones extremas sin requerir transformaciones "
        "agresivas. A continuación se presentan las tablas y figuras del análisis exploratorio.",
    )
    insert_entregable2_tables(doc)
    insert_eda_figures(doc)
    heading2(doc, "Preprocesamiento")
    body(
        doc,
        "El preprocesamiento (src/preprocessing.py) replica el flujo del notebook: eliminación de "
        "columnas excluidas, codificación ordinal de Burnout_Level (Low=0 a Severe=3), one-hot encoding "
        "de Gender y Education_Level con drop_first=True, y alineación de columnas en inferencia. El "
        "vector final comprende 13 características utilizadas en metadata.json.",
    )
    heading2(doc, "Partición de datos")
    body(
        doc,
        "Se aplicó división estratificada con random_state=42: 70 % entrenamiento (≈10.500), 15 % "
        "validación (≈2.250) y 15 % prueba (≈2.250). El conjunto de entrenamiento ajusta parámetros; "
        "validación calibra umbrales y compara modelos; prueba evalúa generalización del XGBoost sin "
        "reajuste de umbral.",
    )
    heading2(doc, "Fases del proyecto")
    body(
        doc,
        "Fase 1: diseño según CONTEXT_MASTER (alcance, ética, criterio de recall). Fase 2: EDA y "
        "preprocesamiento en Colab. Fase 3: comparación de modelos y exportación de métricas. Fase 4: "
        "implementación del repositorio MindTrack y pipelines joblib. Fase 5: productización UX, matrices "
        "de confusión en laboratorio, despliegue cloud y automatización keep-alive. Cada fase dejó "
        "artefactos verificables (notebooks, CSV, PNG, metadata.json, aplicación web).",
    )
    heading2(doc, "Algoritmos y construcción de árboles")
    heading3(doc, "Árbol de decisión (base teórica)")
    body(
        doc,
        "Un árbol de decisión particiona recursivamente el espacio de características mediante reglas "
        "del tipo “si feature ≤ umbral”. En cada nodo se evalúan candidatos de división y se selecciona "
        "el corte que maximiza la reducción de impureza (criterio Gini en implementaciones CART). El "
        "proceso continúa en nodos hijo hasta alcanzar criterios de parada (profundidad máxima, tamaño "
        "mínimo de hoja). Cada hoja entrega una probabilidad de clase positiva. Un solo árbol es "
        "interpretable pero inestable; por ello se emplearon ensembles.",
    )
    heading3(doc, "Random Forest")
    body(
        doc,
        "Random Forest construye B=300 árboles independientes. Cada árbol se entrena con una muestra "
        "bootstrap de las filas de entrenamiento y, en cada división, considera un subconjunto aleatorio "
        "de características. Se configuró min_samples_leaf=2 y class_weight=balanced_subsample para "
        "atender el desbalance. La predicción final es el promedio de probabilidades de los árboles, "
        "lo que reduce varianza y captura interacciones no lineales entre variables.",
    )
    heading3(doc, "XGBoost (modelo de producción)")
    body(
        doc,
        "XGBoost implementa gradient boosting: los árboles se entrenan en secuencia, cada uno corrigiendo "
        "errores residuales del conjunto anterior bajo una función de pérdida logística. Hiperparámetros: "
        "n_estimators=300, max_depth=5, learning_rate=0.05, subsample=0.9, colsample_bytree=0.9, "
        "scale_pos_weight proporcional a n_neg/n_pos en entrenamiento. La predicción agrega "
        "contribuciones de todos los árboles con tasa de aprendizaje moderada para mitigar sobreajuste.",
    )
    heading3(doc, "Regresión logística")
    body(
        doc,
        "Como línea base, se entrenó regresión logística con estandarización previa y class_weight=balanced. "
        "Modela una frontera lineal en el espacio escalado y sirve para contraste en el módulo de segunda "
        "opinión de la aplicación.",
    )
    heading2(doc, "Calibración del umbral")
    body(
        doc,
        "No se utilizó el corte 0,5 por defecto. En validación, para cada modelo, se recorrió la curva "
        "precision–recall y se eligió el umbral más alto que cumple recall≥0,85 maximizando F1 entre los "
        "candidatos válidos. Umbrales obtenidos: Logistic Regression ≈0,904; Random Forest ≈0,418; "
        "XGBoost ≈0,728. El umbral del XGBoost se fijó para inferencia en producción y prueba.",
    )
    heading2(doc, "Métricas de evaluación")
    body(
        doc,
        "Se reportaron recall, precisión, F1 de la clase positiva, PR-AUC, ROC-AUC y conteos TN, FP, FN, "
        "TP. FN representa estudiantes en riesgo no detectados (costo prioritario en alerta temprana); FP "
        "representa alertas innecesarias.",
    )

    heading1(doc, "Desarrollo del Sistema MindTrack")
    heading2(doc, "Arquitectura de software")
    body(
        doc,
        "El repositorio GitHub (Danielhsk/MindTrack) organiza app/streamlit_app.py (interfaz), módulos "
        "src/ (preprocesamiento, predicción, explicación, recomendaciones, visualización), models/ "
        "(pipelines joblib y metadata.json), reports/ (CSVs y figuras) y scripts/train_and_export.py "
        "para reproducir el experimento. El entrypoint streamlit_app.py en raíz habilita despliegue en "
        "Streamlit Cloud.",
    )
    heading2(doc, "Modo Producción (PRD)")
    body(
        doc,
        "El usuario completa un formulario en español (sin nota académica). La aplicación ejecuta "
        "preprocesamiento, inferencia XGBoost, cálculo de banda de riesgo (BAJO/MODERADO/ALTO), panel "
        "de segunda opinión con tres modelos (informativo), contribuciones SHAP (TreeExplainer), "
        "recomendaciones por reglas (sueño, redes, actividad, salud mental, aislamiento, burnout) y "
        "conclusión con disclaimer ético.",
    )
    heading2(doc, "Modo Laboratorio (LAB)")
    body(
        doc,
        "El laboratorio es de solo lectura: panorama con KPIs, huella de datos (EDA interactivo y galería "
        "Colab), trazabilidad del protocolo experimental y arena de modelos con tabla comparativa, "
        "matrices de confusión, gráficos de métricas y falsos negativos versus falsos positivos. No "
        "reentrena modelos en la nube para mantener tiempos de respuesta estables.",
    )
    heading2(doc, "Despliegue y operación")
    body(
        doc,
        "La aplicación pública está en https://mindtrack-si.streamlit.app/. Se configuró un workflow "
        "GitHub Actions (Keep Streamlit app awake) que visita la URL cada 5 horas (UTC) mediante "
        "automatización con Puppeteer para mitigar el estado de inactividad de Streamlit Community Cloud.",
    )

    heading1(doc, "Resultados")
    heading2(doc, "Tabla de variables del formulario de producción")
    body(
        doc,
        "El formulario de producción solicita: edad; género; nivel educativo; horas diarias en redes "
        "sociales; horas diarias de uso de herramientas de IA; horas de sueño; horas de actividad "
        "física; puntuación de bienestar mental; puntuación de bienestar físico; puntuación de "
        "aislamiento social; y nivel de burnout (ordinal). No solicita Student_ID ni "
        "Academic_Performance_Score.",
    )
    insert_model_tables_and_figures(doc)
    heading2(doc, "Síntesis narrativa de resultados")
    body(
        doc,
        "En validación (n≈2.250), con umbrales calibrados: Logistic Regression alcanzó recall 0,852, "
        "precisión 0,788, F1 0,819 y PR-AUC 0,917 (FN=20, FP=31, TP=115, TN=2084). Random Forest "
        "alcanzó recall 0,874, precisión 0,715, F1 0,787 y PR-AUC 0,899 (FN=17, FP=47, TP=118, "
        "TN=2068). XGBoost alcanzó recall 0,859, precisión 0,730, F1 0,789 y PR-AUC 0,915 "
        "(FN=19, FP=43, TP=116, TN=2072). Los tres modelos cumplieron el recall objetivo ≥0,85.",
    )
    body(
        doc,
        "En prueba (n≈2.250), con el umbral aprendido en validación y sin re-ajuste: Logistic Regression "
        "obtuvo recall 0,852, F1 0,801 y PR-AUC 0,918 (FN=20, FP=37). Random Forest obtuvo recall "
        "0,911, F1 0,809 y PR-AUC 0,926 (FN=12, FP=46). XGBoost obtuvo recall 0,881, F1 0,824 y "
        "PR-AUC 0,933 (FN=16, FP=35). Los tres cumplieron recall ≥0,85 en prueba.",
    )
    heading2(doc, "Selección del modelo de producción")
    body(
        doc,
        "En validación, Logistic Regression lideró F1 y registró menos falsas alarmas (FP). La decisión "
        "de despliegue se basó en prueba: entre modelos que cumplen recall, se ordenó por F1, PR-AUC, "
        "precisión, menor FP y menor FN. XGBoost quedó primero en esa jerarquía (mayor F1 y PR-AUC en "
        "prueba), con menos FN que LR y menos FP que Random Forest. Por ello se adoptó como motor "
        "oficial de la consulta en vivo.",
    )

    heading1(doc, "Discusión")
    body(
        doc,
        "Los resultados apoyan la viabilidad de estimar riesgo académico a partir de variables de "
        "bienestar y hábitos digitales en un escenario sin nota previa. La comparación de tres familias "
        "de algoritmos (lineal, bagging de árboles, boosting de árboles) aporta trazabilidad académica "
        "y transparencia mediante segunda opinión en la interfaz. La explicabilidad local (SHAP) y las "
        "recomendaciones basadas en reglas complementan la probabilidad con mensajes accionables, sin "
        "sustituir acompañamiento humano.",
    )
    body(
        doc,
        "Las limitaciones incluyen dependencia de un dataset académico/sintético, ausencia de validación "
        "con población institucional real, posible desalineación temporal de hábitos digitales, y riesgo "
        "de sobreconfianza interpretativa. Predicción no implica causalidad.",
    )

    heading1(doc, "Conclusiones")
    body(
        doc,
        "MindTrack materializa un ciclo completo de sistemas inteligentes: análisis de datos, "
        "preprocesamiento, entrenamiento comparativo, selección con criterio de recall, despliegue web "
        "y explicación. El prototipo cumple los objetivos del curso en formato MVP defendible, con "
        "documentación, notebooks, artefactos versionados y aplicación pública. Futuras mejoras "
        "podrían incluir calibración probabilística, monitoreo de drift y estudios de usabilidad con "
        "docentes y estudiantes.",
    )

    heading1(doc, "Consideraciones Éticas")
    body(
        doc,
        "MindTrack es orientativo. No constituye diagnóstico médico ni psicológico ni decisión "
        "institucional. Se comunicó explícitamente en interfaz y conclusiones. El tratamiento de datos "
        "en el MVP no almacena historiales personales en servidor propio más allá de la sesión Streamlit; "
        "en despliegue cloud aplican políticas del proveedor.",
    )

    page_break(doc)
    heading1(doc, "Referencias")
    refs = [
        "American Psychological Association. (2020). Publication manual of the American Psychological "
        "Association (7th ed.). https://doi.org/10.1037/0000165-000",
        "Bishop, C. M. (2006). Pattern recognition and machine learning. Springer.",
        "Breiman, L. (2001). Random forests. Machine Learning, 45(1), 5–32. "
        "https://doi.org/10.1023/A:1010933404324",
        "Chen, T., & Guestrin, C. (2016). XGBoost: A scalable tree boosting system. Proceedings of the "
        "22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, 785–794. "
        "https://doi.org/10.1145/2939672.2939785",
        "Lundberg, S. M., & Lee, S.-I. (2017). A unified approach to interpreting model predictions. "
        "Advances in Neural Information Processing Systems, 30. "
        "https://doi.org/10.48550/arXiv.1705.07874",
        "Pedregosa, F., et al. (2011). Scikit-learn: Machine learning in Python. Journal of Machine "
        "Learning Research, 12, 2825–2830.",
        "Streamlit Inc. (s. f.). Streamlit documentation. https://docs.streamlit.io",
    ]
    for ref in refs:
        p = doc.add_paragraph(ref)
        p.paragraph_format.first_line_indent = Inches(-0.5)
        p.paragraph_format.left_indent = Inches(0.5)

    page_break(doc)
    heading1(doc, "Apéndices")
    heading2(doc, "Apéndice A: Repositorio y entregables")
    body(
        doc,
        "Repositorio: https://github.com/Danielhsk/MindTrack. Notebooks: MindTrack_EDA_Preprocesamiento "
        "y MindTrack_03_Comparacion_Modelos. Aplicación: mindtrack-si.streamlit.app.",
    )
    heading2(doc, "Apéndice B: Comandos de reproducibilidad")
    body(
        doc,
        "pip install -r requirements.txt; python scripts/train_and_export.py; "
        "streamlit run app/streamlit_app.py",
    )


def main() -> None:
    global _table_counter, _figure_counter, _seen_image_hashes
    _table_counter = 0
    _figure_counter = 0
    _seen_image_hashes = set()
    doc = Document()
    set_document_defaults(doc)
    title_page(doc)
    build_content(doc)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc.save(OUT)
    print(f"Informe generado: {OUT}")


if __name__ == "__main__":
    main()