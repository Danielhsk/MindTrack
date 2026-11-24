"""MindTrack Streamlit — PRD (inferencia producción) + LAB (Insight, solo lectura)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.conclusion import build_conclusion
from src.config import (
    COLORS,
    FIGURES_DIR,
    FORM_FIELD_LABELS_ES,
    MODELS_DIR,
    REPORTS_DIR,
    TARGET,
)
from src.form_ui import categorical_burnout, categorical_education, categorical_gender
from src.explainability import top_contributions
import importlib

import src.lab_viz as lab_viz

importlib.reload(lab_viz)

fig_burnout_risk = lab_viz.fig_burnout_risk
fig_class_balance = lab_viz.fig_class_balance
fig_confusion_matrix_row = lab_viz.fig_confusion_matrix_row
fig_correlation_target = lab_viz.fig_correlation_target
fig_fn_fp = lab_viz.fig_fn_fp
fig_metrics_radar = lab_viz.fig_metrics_radar
fig_metric_vs_risk_jitter = lab_viz.fig_metric_vs_risk_jitter
fig_model_metrics = lab_viz.fig_model_metrics
load_dataset = lab_viz.load_dataset
SCATTER_METRIC_OPTIONS = lab_viz.SCATTER_METRIC_OPTIONS
from src.predict import load_metadata, panel_opinions, predict_student
from src.recommendations import generate_recommendations
from src.ui_components import (
    EXAMPLE_PROFILES,
    content_divider,
    hero,
    init_session_defaults,
    insight_note,
    kpi_grid,
    page_footer,
    panel_heading,
    profile_chips_header,
    render_app_header,
    render_insight_nav,
    render_panel_opinions,
    render_verdict_block,
    render_static_figure_gallery,
    section_heading,
    timeline_block,
)
from src.ui_theme import apply_theme

st.set_page_config(
    page_title="MindTrack",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

apply_theme()

LAB_SECTIONS = [
    "Panorama",
    "Huella de datos",
    "Trazabilidad ML",
    "Arena de modelos",
]


@st.cache_data(show_spinner=False)
def cached_dataset() -> pd.DataFrame:
    return load_dataset()


def preset_values() -> dict:
    init_session_defaults()
    preset_key = st.session_state.get("form_preset", "neutral")
    if preset_key not in EXAMPLE_PROFILES:
        preset_key = "neutral"
        st.session_state.form_preset = preset_key
    return EXAMPLE_PROFILES[preset_key]["values"]


def production_form() -> dict | None:
    pv = preset_values()
    profile_chips_header()
    st.markdown('<motion-div class="mt-chip-bar" aria-hidden="true"></div>'.replace("motion-div", "div"), unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button(
            EXAMPLE_PROFILES["neutral"]["label"],
            use_container_width=True,
            key="btn_neutral",
            type="secondary",
        ):
            st.session_state.form_preset = "neutral"
    with c2:
        if st.button(
            EXAMPLE_PROFILES["alert"]["label"],
            use_container_width=True,
            key="btn_alert",
            type="secondary",
        ):
            st.session_state.form_preset = "alert"

    field_labels = FORM_FIELD_LABELS_ES
    with st.form("student_form", clear_on_submit=False):
        c1, c2, c3 = st.columns(3)
        with c1:
            panel_heading("Perfil", "Demografía y contexto")
            age = st.number_input(field_labels["Age"], 14, 40, pv["age"], 1)
            gender = categorical_gender(pv["gender"])
            education = categorical_education(pv["education"])
        with c2:
            panel_heading("Hábitos", "Digital · sueño · actividad")
            social = st.slider(field_labels["Daily_Social_Media_Hours"], 0.0, 14.0, float(pv["social"]), 0.1)
            ai_hours = st.slider(field_labels["Daily_AI_Tool_Usage_Hours"], 0.0, 10.0, float(pv["ai_hours"]), 0.1)
            sleep = st.slider(field_labels["Sleep_Hours"], 2.0, 12.0, float(pv["sleep"]), 0.1)
            activity = st.slider(field_labels["Physical_Activity_Hours"], 0.0, 6.0, float(pv["activity"]), 0.1)
        with c3:
            panel_heading("Bienestar", "Salud y burnout")
            mental = st.slider(field_labels["Mental_Health_Score"], 20.0, 100.0, float(pv["mental"]), 0.5)
            physical = st.slider(field_labels["Physical_Health_Score"], 20.0, 100.0, float(pv["physical"]), 0.5)
            isolation = st.slider(field_labels["Social_Isolation_Score"], 1.0, 9.0, float(pv["isolation"]), 0.1)
            burnout = categorical_burnout(pv["burnout"])
        submitted = st.form_submit_button(
            "Ejecutar consulta MindTrack",
            use_container_width=True,
            type="primary",
        )

    if not submitted:
        return None

    return {
        "Age": int(age),
        "Gender": gender,
        "Education_Level": education,
        "Daily_Social_Media_Hours": float(social),
        "Daily_AI_Tool_Usage_Hours": float(ai_hours),
        "Sleep_Hours": float(sleep),
        "Physical_Activity_Hours": float(activity),
        "Mental_Health_Score": float(mental),
        "Physical_Health_Score": float(physical),
        "Social_Isolation_Score": float(isolation),
        "Burnout_Level": burnout,
    }


def load_lab_artifacts() -> tuple[pd.DataFrame, dict] | None:
    csv_path = REPORTS_DIR / "comparison_validation.csv"
    meta_path = MODELS_DIR / "metadata.json"
    if not csv_path.exists() or not meta_path.exists():
        return None
    comparison = pd.read_csv(csv_path)
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    return comparison, meta


def _production_label() -> str:
    meta_path = MODELS_DIR / "metadata.json"
    if not meta_path.exists():
        return "XGBoost"
    raw = json.loads(meta_path.read_text(encoding="utf-8")).get("production_model_label", "XGBoost")
    return str(raw) if raw else "XGBoost"


def render_prd() -> None:
    meta_path = MODELS_DIR / "metadata.json"
    if not meta_path.exists():
        st.error("Ejecuta `python scripts/train_and_export.py` para generar artefactos.")
        return
    prod_label = _production_label()

    hero(
        "Consulta MindTrack",
        "Completa el perfil del estudiante y recibe una estimación de riesgo académico, "
        "los factores que más influyen y recomendaciones orientadas al bienestar. "
        f"La predicción oficial usa {prod_label} (elegido por métricas en test), "
        "sin incluir la nota directa en el modelo.",
        badge="PRD",
    )

    form = production_form()
    if form is None:
        st.markdown(
            "<div class='mt-card mt-tip' data-tip='No se ejecuta ML hasta enviar el formulario.'>"
            "Completa el perfil o carga un ejemplo, luego pulsa "
            "<strong>Ejecutar consulta MindTrack</strong>.</div>",
            unsafe_allow_html=True,
        )
        page_footer("PRD")
        return

    st.toast("Procesando consulta MindTrack…", icon="⏳")
    with st.status("Ejecutando consulta…", expanded=True) as run_status:
        st.write("Validando y transformando los datos del perfil…")
        result = predict_student(form)
        st.write(f"Calculando probabilidad con {prod_label} (motor oficial)…")
        opinions = panel_opinions(form)
        st.write("Preparando explicación, segunda opinión y recomendaciones…")
        contrib = top_contributions(form, k=8)
        recs = generate_recommendations(form)
        conclusion = build_conclusion(
            result, recs, top_factors=contrib["feature"].tolist()
        )
        run_status.update(label="Consulta completada", state="complete", expanded=False)
    st.success("Listo: puedes revisar el estado del perfil y el detalle a continuación.")

    content_divider()
    render_verdict_block(
        result["predicted_class"] == 1,
        result["probability"],
        result["threshold"],
        result["risk_band"],
    )

    m1, m2, m3, m4 = st.columns(4)
    m1.metric(
        "Banda",
        result["risk_band"],
        help=(
            "Qué tan alto parece el riesgo según la probabilidad del modelo: "
            "BAJO (lejos del corte), MODERADO (cerca) o ALTO (por encima). "
            "Es una guía analítica, no un dictamen oficial."
        ),
    )
    m2.metric(
        "Umbral",
        f"{result['threshold']:.3f}",
        help=(
            "Probabilidad mínima a partir de la cual el sistema marca alerta. "
            "Se calibró en validación para detectar bien los casos en riesgo "
            "(prioriza no pasar por alto alertas reales)."
        ),
    )
    m3.metric(
        "Clase",
        "1 · At risk" if result["predicted_class"] else "0 · No risk",
        help=(
            "Etiqueta simplificada del modelo: «At risk» si la probabilidad "
            "supera el umbral; «No risk» si queda por debajo."
        ),
    )
    m4.metric(
        "Modelo",
        result["model_label"],
        help=(
            f"Algoritmo de producción ({prod_label}), elegido tras comparar LR, RF y XGBoost en test."
        ),
    )

    content_divider()
    section_heading(
        "Segunda opinión del comité",
        "Tres modelos del experimento con su umbral de validación; "
        f"no modifica la decisión oficial de {prod_label}.",
    )
    render_panel_opinions(opinions)

    left, right = st.columns((1.1, 1))
    with left:
        section_heading(
            "Factores que empujan el estado",
            "Muestra qué variables del perfil empujan el resultado hacia alerta o calma; "
            "barras más largas = mayor influencia en esta consulta.",
        )
        fig = px.bar(
            contrib.sort_values("contribution"),
            x="contribution",
            y="feature",
            orientation="h",
            color="contribution",
            color_continuous_scale=[COLORS["navy"], COLORS["slate"], COLORS["accent"]],
        )
        fig.update_layout(
            height=380,
            margin=dict(l=10, r=10, t=20, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            coloraxis_showscale=False,
        )
        st.plotly_chart(fig, use_container_width=True)
        st.caption(f"Explicación: {contrib['method'].iloc[0]}")

    with right:
        section_heading(
            "Recomendaciones",
            "Sugerencias prácticas según el perfil (sueño, redes, bienestar); "
            "son reglas del proyecto, no texto generado por IA.",
        )
        for tip in recs:
            st.markdown(
                f"<div class='mt-card'><strong>{tip['title']}</strong>"
                f"<br/><span style='color:{COLORS['slate']};font-size:0.9rem'>"
                f"{tip['detail']}</span></div>",
                unsafe_allow_html=True,
            )

    content_divider()
    section_heading(
        "Conclusión",
        "Resumen en lenguaje natural que combina probabilidad, banda de riesgo "
        "y las recomendaciones mostradas arriba.",
    )
    st.markdown(conclusion)
    st.markdown(
        "<div class='mt-disclaimer'>Prototipo académico — no sustituye acompañamiento institucional.</div>",
        unsafe_allow_html=True,
    )
    page_footer("PRD")


def lab_panorama(meta: dict) -> None:
    test = meta.get("test_metrics_production", {})
    test_all = meta.get("test_metrics_all", [])
    val = meta.get("validation_metrics", [])
    sel = meta.get("selection_criteria", {})
    prod_label = meta.get("production_model_label", "XGBoost")
    prod_val = next((m for m in val if m["Modelo"] == prod_label), {})
    val_leader = sel.get("validation_winner_label", "—")
    risk_pct = cached_dataset()[TARGET].mean() * 100
    kpi_grid(
        [
            (
                "15,000",
                "Registros",
                "Cantidad de perfiles de estudiantes simulados en el dataset "
                "con el que se entrenó y evaluó MindTrack.",
            ),
            (
                f"{risk_pct:.1f}%",
                "Con riesgo en datos",
                "Porcentaje de filas marcadas con riesgo académico alto en el dataset; "
                "la mayoría de casos son «sin riesgo», como en la vida real.",
            ),
            (
                f"{prod_val.get('Recall (C1)', 0):.3f}",
                f"Recall · val. ({prod_label})",
                "Umbral calibrado solo en validación (recall ≥ 0,85). "
                f"Líder F1 en validación: {val_leader}.",
            ),
            (
                f"{test.get('Recall (C1)', 0):.3f}",
                f"Recall · test ({prod_label})",
                "Prueba final con τ fijado en validación (sin re-ajuste).",
            ),
            (
                f"{test.get('F1-Score (C1)', 0):.3f}",
                "F1 · test (producción)",
                "Criterio principal para elegir el motor entre modelos que cumplen recall en test.",
            ),
            (
                f"{test.get('PR-AUC', 0):.3f}",
                "PR-AUC · test",
                "Capacidad de ranking del riesgo en la partición de prueba.",
            ),
        ]
    )
    insight_note(
        f"Split 70/15/15 · seed {meta['random_state']} · recall ≥ {meta['recall_target']} · "
        f"producción = {prod_label} (test) · Docker: docs/DOCKER.md",
        "Validación calibra umbrales; test compara LR, RF y XGB con el mismo protocolo.",
    )
    if test_all:
        section_heading(
            "Resumen · test (tres modelos)",
            "Métricas en `reports/comparison_test.csv` · FN/FP con umbrales de validación.",
        )
        show_cols = [
            "Modelo",
            "Recall (C1)",
            "F1-Score (C1)",
            "PR-AUC",
            "FN",
            "FP",
            "Cumple Recall",
        ]
        df_test = pd.DataFrame(test_all)
        df_test = df_test[[c for c in show_cols if c in df_test.columns]]
        st.dataframe(df_test, use_container_width=True, hide_index=True)


def lab_huella() -> None:
    df = cached_dataset()
    section_heading(
        "Huella de datos",
        "Explora visualmente el dataset: balance de clases, burnout y correlaciones "
        "con el riesgo, con los mismos datos del análisis exploratorio del curso.",
    )
    st.caption(f"Dataset: `data/academic_risk_dataset.csv` · {len(df):,} filas.")
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(fig_class_balance(df), use_container_width=True)
    with c2:
        st.plotly_chart(fig_burnout_risk(df), use_container_width=True)
    metric_keys = [k for k, _ in SCATTER_METRIC_OPTIONS]
    metric_labels = {k: v for k, v in SCATTER_METRIC_OPTIONS}
    metric = st.selectbox(
        "Variable a comparar con el riesgo",
        metric_keys,
        format_func=lambda k: metric_labels[k],
    )
    st.caption(
        "Cada punto es un estudiante del dataset. La separación vertical es solo visual "
        "(jitter) para que no se amontonen en las líneas 0 y 1."
    )
    st.plotly_chart(fig_metric_vs_risk_jitter(df, metric), use_container_width=True)
    st.plotly_chart(fig_correlation_target(df), use_container_width=True)

    content_divider()
    from src.colab_assets import ASSETS_COLAB_DIR, COLAB_EDA_GALLERY

    render_static_figure_gallery(
        COLAB_EDA_GALLERY,
        ASSETS_COLAB_DIR,
        heading="Figuras del EDA (Colab)",
        lead=(
            "Mismas gráficas del notebook de análisis exploratorio; útiles como "
            "evidencia del informe y para comparar con los gráficos interactivos de arriba."
        ),
    )


def lab_trazabilidad() -> None:
    section_heading(
        "Trazabilidad ML",
        "Cronología del proyecto de punta a punta; pasa el cursor sobre cada paso "
        "para una explicación más detallada.",
    )
    st.markdown(
        "Cadena de decisiones del proyecto MindTrack (Entregables 2 y 3). "
        "Sin reentrenamiento en esta interfaz."
    )
    timeline_block()


def lab_arena(comparison: pd.DataFrame, meta: dict) -> None:
    section_heading(
        "Arena de modelos",
        "Compara métricas de los tres modelos candidatos y elige visualmente "
        "métricas en validación y la evaluación final en test (mismos umbrales de validación).",
    )
    st.markdown("#### Validación (calibración de umbral)")
    st.dataframe(comparison, use_container_width=True, hide_index=True)

    cm_cols = {"Modelo", "TN", "FP", "FN", "TP"}
    if cm_cols.issubset(comparison.columns):
        section_heading(
            "Matrices de confusión (validación)",
            "Vista por modelo: cuántas predicciones acertaron y qué tipo de error cometió "
            "con su umbral calibrado.",
        )
        st.caption(
            "FN = estudiante en riesgo no detectado · FP = alerta innecesaria · "
            "Útil junto al gráfico de barras de métricas."
        )
        cols = st.columns(3)
        for col, (_, row) in zip(cols, comparison.iterrows()):
            with col:
                st.plotly_chart(
                    fig_confusion_matrix_row(row),
                    use_container_width=True,
                    key=f"cm_{row['Modelo']}",
                )
        content_divider()

    metric_choice = st.selectbox(
        "Métrica interactiva",
        ["Recall (C1)", "F1-Score (C1)", "PR-AUC", "Precision (C1)", "ROC-AUC"],
    )
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(fig_model_metrics(comparison, metric_choice), use_container_width=True)
    with c2:
        st.plotly_chart(fig_fn_fp(comparison), use_container_width=True)
    st.plotly_chart(fig_metrics_radar(comparison), use_container_width=True)

    test_all_path = REPORTS_DIR / "comparison_test.csv"
    if test_all_path.exists():
        test_df = pd.read_csv(test_all_path)
        prod_label = meta.get("production_model_label", "XGBoost")
        sel = meta.get("selection_criteria", {})
        content_divider()
        section_heading(
            "Test · los tres modelos",
            "Evaluación en datos nunca usados para entrenar ni para elegir umbral. "
            "Cada fila usa el τ aprendido en validación (sin re-ajuste).",
        )
        st.dataframe(test_df, use_container_width=True, hide_index=True)
        if sel.get("test_selection_steps"):
            st.markdown(
                f"**Modelo de producción ({prod_label})** — criterio: "
                + " ".join(sel["test_selection_steps"])
            )
        if {"Modelo", "FN", "FP"}.issubset(test_df.columns):
            st.plotly_chart(
                fig_fn_fp(test_df.set_index("Modelo")),
                use_container_width=True,
                key="fn_fp_test",
            )

    content_divider()
    from src.colab_assets import ML_EXPORT_GALLERY

    render_static_figure_gallery(
        ML_EXPORT_GALLERY,
        FIGURES_DIR,
        heading="Figuras del experimento (Colab / export)",
        lead=(
            "PNG generadas al entrenar y comparar modelos (mismo contenido que el "
            "notebook de comparación en Colab y `scripts/train_and_export.py`)."
        ),
    )


def render_lab() -> None:
    init_session_defaults()
    hero(
        "MindTrack Insight",
        "Recorre los datos del estudio, cómo se construyó el modelo y cómo se compararon "
        "los algoritmos. Es una vista de consulta: no cambia ni vuelve a entrenar "
        "el motor que usa la pestaña de producción.",
        badge="LAB",
    )
    data = load_lab_artifacts()
    if data is None:
        st.error("Faltan `reports/comparison_validation.csv` o `models/metadata.json`.")
        return
    comparison, meta = data
    section = render_insight_nav(LAB_SECTIONS)

    if section == "Panorama":
        lab_panorama(meta)
    elif section == "Huella de datos":
        lab_huella()
    elif section == "Trazabilidad ML":
        lab_trazabilidad()
    elif section == "Arena de modelos":
        lab_arena(comparison, meta)

    page_footer("LAB")


def main() -> None:
    init_session_defaults()
    prod_label = _production_label()
    render_app_header(prod_label)
    env = st.session_state.get("mindtrack_env", "PRD")
    if env not in ("PRD", "LAB"):
        env = "PRD"
        st.session_state.mindtrack_env = env
    if env == "PRD":
        render_prd()
    else:
        render_lab()


if __name__ == "__main__":
    main()