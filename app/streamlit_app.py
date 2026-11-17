"""MindTrack Streamlit — PRD (consulta XGBoost) + LAB (Insight, solo lectura)."""

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
    FORM_CATEGORICAL,
    MODELS_DIR,
    REPORTS_DIR,
    TARGET,
)
from src.explainability import top_contributions
from src.lab_viz import (
    fig_burnout_risk,
    fig_class_balance,
    fig_correlation_target,
    fig_fn_fp,
    fig_metrics_radar,
    fig_model_metrics,
    load_dataset,
)
from src.predict import load_metadata, predict_student
from src.recommendations import generate_recommendations
from src.ui_components import (
    EXAMPLE_PROFILES,
    hero,
    init_session_defaults,
    render_env_switch,
    threshold_gauge,
    timeline_block,
    verdict_stamp,
)
from src.ui_theme import inject_css

st.set_page_config(
    page_title="MindTrack",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(inject_css(), unsafe_allow_html=True)
init_session_defaults()

LAB_SECTIONS = [
    "Panorama",
    "Huella de datos",
    "Trazabilidad ML",
    "Arena de modelos",
]


@st.cache_data(show_spinner=False)
def cached_dataset() -> pd.DataFrame:
    return load_dataset()


def sidebar_brand() -> None:
    st.sidebar.markdown("## MindTrack")
    st.sidebar.caption("Riesgo académico · hábitos digitales y bienestar")
    env = render_env_switch()
    st.sidebar.markdown("---")
    if env == "LAB":
        st.sidebar.markdown("**Navegación Insight**")
        st.session_state.lab_section = st.sidebar.radio(
            "Sección",
            LAB_SECTIONS,
            index=LAB_SECTIONS.index(st.session_state.lab_section),
            label_visibility="collapsed",
        )
    st.sidebar.markdown(
        "<span class='mt-badge'>Motor PRD: XGBoost</span>",
        unsafe_allow_html=True,
    )
    st.sidebar.caption(
        "Academic_Performance_Score fuera del ML (escenario preventivo)."
    )


def preset_values() -> dict:
    return EXAMPLE_PROFILES[st.session_state.form_preset]["values"]


def production_form() -> dict | None:
    pv = preset_values()
    st.markdown("**Perfiles de ejemplo**")
    c1, c2 = st.columns(2)
    with c1:
        if st.button(
            EXAMPLE_PROFILES["neutral"]["label"],
            use_container_width=True,
            key="btn_neutral",
        ):
            st.session_state.form_preset = "neutral"
    with c2:
        if st.button(
            EXAMPLE_PROFILES["alert"]["label"],
            use_container_width=True,
            key="btn_alert",
        ):
            st.session_state.form_preset = "alert"

    with st.form("student_form", clear_on_submit=False):
        c1, c2, c3 = st.columns(3)
        with c1:
            age = st.number_input("Age", 14, 40, pv["age"], 1)
            gender = st.selectbox("Gender", FORM_CATEGORICAL["Gender"], index=FORM_CATEGORICAL["Gender"].index(pv["gender"]))
            education = st.selectbox(
                "Education_Level",
                FORM_CATEGORICAL["Education_Level"],
                index=FORM_CATEGORICAL["Education_Level"].index(pv["education"]),
            )
        with c2:
            social = st.slider("Daily_Social_Media_Hours", 0.0, 14.0, float(pv["social"]), 0.1)
            ai_hours = st.slider("Daily_AI_Tool_Usage_Hours", 0.0, 10.0, float(pv["ai_hours"]), 0.1)
            sleep = st.slider("Sleep_Hours", 2.0, 12.0, float(pv["sleep"]), 0.1)
            activity = st.slider("Physical_Activity_Hours", 0.0, 6.0, float(pv["activity"]), 0.1)
        with c3:
            mental = st.slider("Mental_Health_Score", 20.0, 100.0, float(pv["mental"]), 0.5)
            physical = st.slider("Physical_Health_Score", 20.0, 100.0, float(pv["physical"]), 0.5)
            isolation = st.slider("Social_Isolation_Score", 1.0, 9.0, float(pv["isolation"]), 0.1)
            burnout = st.selectbox(
                "Burnout_Level",
                FORM_CATEGORICAL["Burnout_Level"],
                index=FORM_CATEGORICAL["Burnout_Level"].index(pv["burnout"]),
            )
        submitted = st.form_submit_button("Ejecutar consulta MindTrack", use_container_width=True)

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


def render_prd() -> None:
    hero(
        "Consulta MindTrack",
        "Inferencia en vivo con el pipeline de producción (preprocess + XGBoost). "
        "Probabilidad de Academic_Failure_Risk, explicación y recomendaciones.",
        badge="PRD",
    )

    meta_path = MODELS_DIR / "metadata.json"
    if not meta_path.exists():
        st.error("Ejecuta `python scripts/train_and_export.py` para generar artefactos.")
        return

    meta = load_metadata()
    tm = meta["thresholds"][meta["production_model_label"]]
    st.caption(
        f"Artefactos · {meta['generated_at_utc']} · umbral Validation={tm:.4f}"
    )

    form = production_form()
    if form is None:
        st.info("Completa el perfil o carga un ejemplo, luego **Ejecutar consulta MindTrack**.")
        return

    with st.spinner("Pipeline en ejecución..."):
        result = predict_student(form)
        contrib = top_contributions(form, k=8)
        recs = generate_recommendations(form)
        conclusion = build_conclusion(
            result, recs, top_factors=contrib["feature"].tolist()
        )

    verdict_stamp(result["predicted_class"] == 1, result["probability"])
    threshold_gauge(result["probability"], result["threshold"])

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Banda", result["risk_band"])
    m2.metric("Umbral", f"{result['threshold']:.3f}")
    m3.metric("Clase", "1 · At risk" if result["predicted_class"] else "0 · No risk")
    m4.metric("Modelo", result["model_label"])

    left, right = st.columns((1.1, 1))
    with left:
        st.subheader("Señales que empujan la predicción")
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
        st.subheader("Recomendaciones")
        for tip in recs:
            st.markdown(
                f"<div class='mt-card'><strong>{tip['title']}</strong>"
                f"<br/><span style='color:{COLORS['slate']};font-size:0.9rem'>"
                f"{tip['detail']}</span></div>",
                unsafe_allow_html=True,
            )

    st.subheader("Conclusión")
    st.markdown(conclusion)
    st.markdown(
        "<div class='mt-disclaimer'>Prototipo académico — no sustituye acompañamiento institucional.</div>",
        unsafe_allow_html=True,
    )


def lab_panorama(meta: dict) -> None:
    test = meta.get("test_metrics_production", {})
    val = meta.get("validation_metrics", [])
    xgb_val = next((m for m in val if m["Modelo"] == "XGBoost"), {})
    risk_pct = cached_dataset()[TARGET].mean() * 100
    st.markdown(
        f"""
        <div class="mt-kpi-grid">
            <motion-div class="mt-kpi"><b>15,000</b><span>Registros</span></div>
            <motion-div class="mt-kpi"><b>{risk_pct:.1f}%</b><span>Clase 1 en datos</span></div>
            <motion-div class="mt-kpi"><b>{xgb_val.get('Recall (C1)', 0):.3f}</b><span>Recall XGB · Val</span></div>
            <motion-div class="mt-kpi"><b>{test.get('Recall (C1)', 0):.3f}</b><span>Recall XGB · Test</span></motion-div>
        </div>
        """.replace("motion-div", "div"),
        unsafe_allow_html=True,
    )
    st.info(
        f"Experimento exportado · split 70/15/15 · seed {meta['random_state']} · "
        f"Recall objetivo {meta['recall_target']} · producción = **XGBoost**."
    )


def lab_huella() -> None:
    df = cached_dataset()
    st.caption(f"Dataset: `data/academic_risk_dataset.csv` · {len(df):,} filas.")
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(fig_class_balance(df), use_container_width=True)
    with c2:
        st.plotly_chart(fig_burnout_risk(df), use_container_width=True)
    metric = st.selectbox(
        "Variable numérica (scatter vs riesgo)",
        [
            "Sleep_Hours",
            "Daily_Social_Media_Hours",
            "Mental_Health_Score",
            "Social_Isolation_Score",
        ],
    )
    sample = df[[metric, TARGET]].sample(min(2500, len(df)), random_state=42)
    fig = px.scatter(
        sample,
        x=metric,
        y=TARGET,
        opacity=0.25,
        color=TARGET,
        color_discrete_map={0: COLORS["ok"], 1: COLORS["accent"]},
        labels={TARGET: "Academic_Failure_Risk"},
    )
    fig.update_layout(
        height=360,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig, use_container_width=True)
    st.plotly_chart(fig_correlation_target(df), use_container_width=True)


def lab_trazabilidad() -> None:
    st.markdown(
        "Cadena de decisiones del proyecto MindTrack (Entregables 2 y 3). "
        "Sin reentrenamiento en esta interfaz."
    )
    timeline_block()


def lab_arena(comparison: pd.DataFrame, meta: dict) -> None:
    st.dataframe(comparison, use_container_width=True, hide_index=True)

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

    test_path = REPORTS_DIR / "evaluation_test_xgboost.csv"
    if test_path.exists():
        st.subheader("Test · XGBoost (producción)")
        st.dataframe(pd.read_csv(test_path), use_container_width=True, hide_index=True)

    with st.expander("Figuras estáticas del notebook (zoom / referencia)"):
        figures = [
            ("metrics_validation.png", "Métricas Validation"),
            ("pr_curves_validation.png", "Curvas Precision-Recall"),
            ("confusion_validation.png", "Matrices de confusión"),
            ("heatmap_validation.png", "Heatmap métricas"),
        ]
        cols = st.columns(2)
        for i, (name, title) in enumerate(figures):
            path = FIGURES_DIR / name
            with cols[i % 2]:
                st.markdown(f"**{title}**")
                if path.exists():
                    st.image(str(path), use_container_width=True)
                else:
                    st.warning(f"Falta {name}")


def render_lab() -> None:
    hero(
        "MindTrack Insight",
        "Laboratorio de evidencia: datos, trazabilidad del pipeline y comparativa de modelos "
        "(artefactos del experimento, solo lectura).",
        badge="LAB",
    )
    data = load_lab_artifacts()
    if data is None:
        st.error("Faltan `reports/comparison_validation.csv` o `models/metadata.json`.")
        return
    comparison, meta = data
    section = st.session_state.lab_section

    if section == "Panorama":
        lab_panorama(meta)
    elif section == "Huella de datos":
        lab_huella()
    elif section == "Trazabilidad ML":
        lab_trazabilidad()
    elif section == "Arena de modelos":
        lab_arena(comparison, meta)


def main() -> None:
    sidebar_brand()
    env = st.session_state.mindtrack_env
    if env == "PRD":
        render_prd()
    else:
        render_lab()


if __name__ == "__main__":
    main()