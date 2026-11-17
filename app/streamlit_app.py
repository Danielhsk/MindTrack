"""MindTrack Streamlit application — Production (XGBoost) + Laboratory (read-only)."""

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
    FORM_CATEGORICAL,
    FORM_NUMERIC,
    FIGURES_DIR,
    MODELS_DIR,
    REPORTS_DIR,
)
from src.explainability import top_contributions
from src.predict import load_metadata, predict_student
from src.recommendations import generate_recommendations
from src.ui_theme import inject_css

st.set_page_config(
    page_title="MindTrack · Academic Risk",
    page_icon="📘",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(inject_css(), unsafe_allow_html=True)


def sidebar() -> str:
    st.sidebar.markdown("## MindTrack")
    st.sidebar.caption("Sistema inteligente de riesgo académico")
    mode = st.sidebar.radio(
        "Modulo",
        options=["Producción", "Laboratorio"],
        index=0,
        help="Producción: inferencia XGBoost. Laboratorio: resultados del Entregable 3 (solo lectura).",
    )
    st.sidebar.markdown("---")
    st.sidebar.markdown(
        f"<span class='mt-badge'>Modelo oficial: XGBoost</span>",
        unsafe_allow_html=True,
    )
    st.sidebar.caption(
        "Academic_Performance_Score excluido del ML (escenario preventivo / anti-leakage)."
    )
    return mode


def render_hero(title: str, subtitle: str) -> None:
    st.markdown(
        f"""
        <div class="mt-hero">
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def production_form() -> dict | None:
    with st.form("student_form", clear_on_submit=False):
        c1, c2, c3 = st.columns(3)
        with c1:
            age = st.number_input("Age", min_value=14, max_value=40, value=20, step=1)
            gender = st.selectbox("Gender", FORM_CATEGORICAL["Gender"])
            education = st.selectbox("Education_Level", FORM_CATEGORICAL["Education_Level"])
        with c2:
            social = st.slider("Daily_Social_Media_Hours", 0.0, 14.0, 4.5, 0.1)
            ai_hours = st.slider("Daily_AI_Tool_Usage_Hours", 0.0, 10.0, 2.5, 0.1)
            sleep = st.slider("Sleep_Hours", 2.0, 12.0, 6.5, 0.1)
            activity = st.slider("Physical_Activity_Hours", 0.0, 6.0, 1.2, 0.1)
        with c3:
            mental = st.slider("Mental_Health_Score", 20.0, 100.0, 72.0, 0.5)
            physical = st.slider("Physical_Health_Score", 20.0, 100.0, 80.0, 0.5)
            isolation = st.slider("Social_Isolation_Score", 1.0, 9.0, 4.2, 0.1)
            burnout = st.selectbox("Burnout_Level", FORM_CATEGORICAL["Burnout_Level"])

        submitted = st.form_submit_button("Analizar estudiante", use_container_width=True)

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


def render_production() -> None:
    render_hero(
        "Producción · Predicción de riesgo",
        "Ingresa el perfil del estudiante. MindTrack ejecuta el pipeline real de Machine Learning "
        "(XGBoost) y muestra probabilidad, factores relevantes y recomendaciones.",
    )

    meta_path = MODELS_DIR / "metadata.json"
    if not meta_path.exists():
        st.error(
            "No se encontró `models/metadata.json`. Ejecuta primero "
            "`python scripts/train_and_export.py`."
        )
        return

    meta = load_metadata()
    st.caption(
        f"Artefactos: {meta['generated_at_utc']} · random_state={meta['random_state']} · "
        f"umbral Validation={meta['thresholds'][meta['production_model_label']]:.4f}"
    )

    form = production_form()
    if form is None:
        st.info("Completa el formulario y pulsa **Analizar estudiante** para ejecutar el modelo.")
        return

    with st.spinner("Ejecutando preprocess + XGBoost..."):
        result = predict_student(form)
        contrib = top_contributions(form, k=8)
        recs = generate_recommendations(form)
        conclusion = build_conclusion(
            result, recs, top_factors=contrib["feature"].tolist()
        )

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Probabilidad (clase 1)", f"{result['probability']:.1%}")
    m2.metric("Umbral", f"{result['threshold']:.3f}")
    m3.metric("Clase predicha", "At risk (1)" if result["predicted_class"] else "No risk (0)")
    m4.metric("Banda", result["risk_band"])

    badge = "mt-badge-risk" if result["predicted_class"] == 1 else "mt-badge-ok"
    st.markdown(
        f"<span class='mt-badge {badge}'>Modelo: {result['model_label']}</span>",
        unsafe_allow_html=True,
    )

    left, right = st.columns((1.1, 1))
    with left:
        st.subheader("Factores relevantes")
        fig = px.bar(
            contrib.sort_values("contribution"),
            x="contribution",
            y="feature",
            orientation="h",
            color="contribution",
            color_continuous_scale=["#1F3A5F", "#94A3B8", "#B45309"],
            labels={"contribution": "Contribution", "feature": "Feature"},
        )
        fig.update_layout(
            height=360,
            margin=dict(l=10, r=10, t=20, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            coloraxis_showscale=False,
        )
        st.plotly_chart(fig, use_container_width=True)
        st.caption(f"Método de explicación: {contrib['method'].iloc[0]}")

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
        "<div class='mt-disclaimer'>MindTrack es un prototipo académico. "
        "Los resultados no reemplazan orientación profesional.</div>",
        unsafe_allow_html=True,
    )


def render_laboratory() -> None:
    render_hero(
        "Laboratorio · Comparación de modelos",
        "Visualización de los mismos resultados del Entregable 3 (Colab). "
        "Solo lectura: no se reentrena ni se procesa el dataset en esta pantalla.",
    )

    csv_path = REPORTS_DIR / "comparison_validation.csv"
    test_path = REPORTS_DIR / "evaluation_test_xgboost.csv"
    meta_path = MODELS_DIR / "metadata.json"

    if not csv_path.exists() or not meta_path.exists():
        st.error(
            "Faltan artefactos del laboratorio. Ejecuta "
            "`python scripts/train_and_export.py` y vuelve a cargar."
        )
        return

    comparison = pd.read_csv(csv_path)
    meta = json.loads(meta_path.read_text(encoding="utf-8"))

    st.info(
        f"Resultados exportados · {meta['generated_at_utc']} · "
        f"split 70/15/15 · random_state={meta['random_state']} · "
        f"Recall target={meta['recall_target']}"
    )

    st.subheader("Tabla comparativa · Validation")
    st.dataframe(comparison, use_container_width=True, hide_index=True)

    if test_path.exists():
        st.subheader("Evaluación final · Test (XGBoost producción)")
        st.dataframe(pd.read_csv(test_path), use_container_width=True, hide_index=True)

    st.subheader("Gráficas del experimento")
    figures = [
        ("metrics_validation.png", "Métricas Validation"),
        ("pr_curves_validation.png", "Curvas Precision-Recall"),
        ("fn_fp_validation.png", "FN vs FP"),
        ("confusion_validation.png", "Matrices de confusión"),
        ("heatmap_validation.png", "Heatmap de métricas"),
    ]
    cols = st.columns(2)
    for i, (name, title) in enumerate(figures):
        path = FIGURES_DIR / name
        with cols[i % 2]:
            st.markdown(f"**{title}**")
            if path.exists():
                st.image(str(path), use_container_width=True)
            else:
                st.warning(f"No encontrada: {name}")

    st.markdown(
        "<div class='mt-disclaimer'>Estas figuras y métricas se generan fuera de Streamlit "
        "(notebook / script) y se versionan en el repositorio. "
        "Para regenerarlas: <code>python scripts/train_and_export.py</code>.</div>",
        unsafe_allow_html=True,
    )


def main() -> None:
    mode = sidebar()
    if mode == "Producción":
        render_production()
    else:
        render_laboratory()


if __name__ == "__main__":
    main()
