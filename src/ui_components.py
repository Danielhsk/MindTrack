"""Reusable MindTrack UI blocks (HTML + Streamlit helpers)."""

from __future__ import annotations

import streamlit as st

from src.config import COLORS


def eyebrow(text: str) -> None:
    st.markdown(
        f"<p class='mt-eyebrow'>{text}</p>",
        unsafe_allow_html=True,
    )


def hero(title: str, subtitle: str, badge: str | None = None) -> None:
    badge_html = f"<span class='mt-badge'>{badge}</span>" if badge else ""
    st.markdown(
        f"""
        <div class="mt-hero">
            {badge_html}
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def verdict_stamp(at_risk: bool, probability: float) -> None:
    cls = "stamp-risk" if at_risk else "stamp-safe"
    label = "AT RISK" if at_risk else "NO RISK"
    st.markdown(
        f"""
        <div class="mt-verdict">
            <div class="mt-stamp {cls}">{label}</div>
            <div class="mt-prob">
                <b>{probability:.1%}</b>
                <small>Academic_Failure_Risk · clase 1</small>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def threshold_gauge(probability: float, threshold: float) -> None:
    pct = max(0.0, min(100.0, probability * 100))
    thr = max(0.0, min(100.0, threshold * 100))
    st.markdown(
        f"""
        <div class="mt-gauge-wrap">
            <div class="mt-gauge">
                <i style="width:{pct:.1f}%"></i>
                <u style="left:{thr:.1f}%"></u>
            </div>
            <div class="mt-gauge-labels">
                <span>0%</span><span>Umbral {threshold:.3f}</span><span>100%</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def init_session_defaults() -> None:
    if "mindtrack_env" not in st.session_state:
        st.session_state.mindtrack_env = "PRD"
    if "lab_section" not in st.session_state:
        st.session_state.lab_section = "Panorama"
    if "form_preset" not in st.session_state:
        st.session_state.form_preset = "neutral"


EXAMPLE_PROFILES = {
    "neutral": {
        "label": "Perfil equilibrado",
        "values": dict(
            age=20,
            gender="Female",
            education="College",
            social=4.5,
            ai_hours=2.0,
            sleep=6.8,
            activity=1.5,
            mental=74.0,
            physical=82.0,
            isolation=4.0,
            burnout="Low",
        ),
    },
    "alert": {
        "label": "Perfil de alerta",
        "values": dict(
            age=21,
            gender="Female",
            education="University",
            social=9.0,
            ai_hours=3.5,
            sleep=4.8,
            activity=0.1,
            mental=52.0,
            physical=58.0,
            isolation=7.0,
            burnout="Severe",
        ),
    },
}


def render_env_switch() -> str:
    """PRD / LAB pill-style switch (Streamlit segmented control + CSS)."""
    st.sidebar.markdown("### Ambiente")
    if hasattr(st.sidebar, "segmented_control"):
        env = st.sidebar.segmented_control(
            "env_switch",
            options=["PRD", "LAB"],
            default=st.session_state.mindtrack_env,
            label_visibility="collapsed",
        )
    else:
        env = st.sidebar.radio(
            "env_switch",
            options=["PRD", "LAB"],
            index=0 if st.session_state.mindtrack_env == "PRD" else 1,
            horizontal=True,
            label_visibility="collapsed",
        )
    if env:
        st.session_state.mindtrack_env = env

    st.sidebar.markdown(
        f"<div class='mt-env-hint'>"
        f"{'Consulta en vivo con XGBoost' if env == 'PRD' else 'Insight · evidencia del experimento'}"
        f"</div>",
        unsafe_allow_html=True,
    )
    return env


def timeline_block() -> None:
    steps = [
        ("01 · Integridad", "Validación de tipos, rangos y ausencia de faltantes."),
        ("02 · Anti-leakage", "Se excluye Academic_Performance_Score del modelado preventivo."),
        ("03 · Codificación", "Burnout ordinal · One-Hot en Gender y Education_Level."),
        ("04 · Partición", "70 % Train · 15 % Validation · 15 % Test (estratificado, seed 42)."),
        ("05 · Modelos", "Logistic Regression · Random Forest · XGBoost (oficial PRD)."),
        ("06 · Umbral", "Recall (C1) ≥ 0.85 en Validation; Test reservado para informe."),
    ]
    for title, text in steps:
        st.markdown(
            f"<div class='mt-step'><b>{title}</b><br/>"
            f"<span style='color:{COLORS['slate']}'>{text}</span></div>",
            unsafe_allow_html=True,
        )