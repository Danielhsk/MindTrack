"""Reusable MindTrack UI blocks (HTML + Streamlit helpers)."""

from __future__ import annotations

import html
from pathlib import Path
from typing import Iterable

import streamlit as st

from src.config import COLORS


def _esc(text: str) -> str:
    return html.escape(text, quote=True)


def eyebrow(text: str) -> None:
    st.markdown(
        f"<p class='mt-eyebrow'>{text}</p>",
        unsafe_allow_html=True,
    )


def hero(title: str, subtitle: str, badge: str | None = None) -> None:
    badge_mod = ""
    if badge:
        badge_mod = f" mt-hero--{badge.lower()}"
        badge_html = f"<span class='mt-badge mt-badge-hero'>{_esc(badge)}</span>"
    else:
        badge_html = ""
    st.markdown(
        f"""
        <div class="mt-hero{badge_mod}">
            <motion-div class="mt-hero-glow" aria-hidden="true"></div>
            {badge_html}
            <h1>{_esc(title)}</h1>
            <p>{_esc(subtitle)}</p>
        </div>
        """.replace("motion-div", "div"),
        unsafe_allow_html=True,
    )


def _resolve_env(choice: str | None) -> str:
    """PRD/LAB from widget; segmented_control can briefly return None on switch."""
    current = st.session_state.get("mindtrack_env", "PRD")
    if choice in ("PRD", "LAB"):
        return choice
    return current if current in ("PRD", "LAB") else "PRD"


def _render_env_widget() -> str:
    """PRD/LAB control (main area)."""
    default = _resolve_env(None)
    if hasattr(st, "segmented_control"):
        choice = st.segmented_control(
            "env_switch",
            options=["PRD", "LAB"],
            default=default,
            label_visibility="collapsed",
        )
    else:
        choice = st.radio(
            "env_switch",
            options=["PRD", "LAB"],
            index=0 if default == "PRD" else 1,
            horizontal=True,
            label_visibility="collapsed",
        )
    env = _resolve_env(choice)
    st.session_state.mindtrack_env = env
    return env


def render_app_header() -> str:
    """Barra superior: marca + switch PRD/LAB (sin sidebar)."""
    with st.container(border=True):
        st.markdown('<span class="mt-appbar-marker" aria-hidden="true"></span>', unsafe_allow_html=True)
        c_brand, c_switch, c_meta = st.columns([1.45, 0.48, 1.05], gap="small")
        with c_brand:
            st.markdown(
                """
                <div class="mt-appbar-brand">
                    <div class="mt-appbar-mark" aria-hidden="true">
                        <svg viewBox="0 0 32 32" fill="none" aria-hidden="true">
                            <circle cx="16" cy="16" r="14" stroke="#94A3B8" stroke-width="1.5"/>
                            <path d="M10 19c1.2-4 3.5-6 6-6s4.8 2 6 6" stroke="#64748B" stroke-width="1.6" stroke-linecap="round"/>
                            <circle cx="16" cy="20" r="2" fill="#6366F1"/>
                        </svg>
                    </div>
                    <div>
                        <div class="mt-appbar-title">MindTrack</div>
                        <div class="mt-appbar-sub">Riesgo académico · hábitos y bienestar</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with c_switch:
            st.markdown('<p class="mt-env-switch-label">Vista</p>', unsafe_allow_html=True)
            env = _render_env_widget()
        with c_meta:
            if env == "PRD":
                st.markdown(
                    "<p class='mt-appbar-meta'><strong>Producción</strong> · "
                    "XGBoost en vivo<br/><span>Preventivo · sin nota en el modelo</span></p>",
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    "<p class='mt-appbar-meta'><strong>Insight</strong> · laboratorio<br/>"
                    "<span>Evidencia Colab · solo lectura</span></p>",
                    unsafe_allow_html=True,
                )
    return env


def render_sidebar_brand() -> None:
    st.sidebar.markdown(
        """
        <motion-div class="mt-brand mt-side-panel mt-side-panel--hero">
            <motion-div class="mt-brand-glow" aria-hidden="true"></div>
            <motion-div class="mt-brand-mark" aria-hidden="true">
                <svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <defs>
                        <linearGradient id="mtRing" x1="8" y1="8" x2="40" y2="40">
                            <stop stop-color="#5EEAD4"/>
                            <stop offset="1" stop-color="#A7F3D0"/>
                        </linearGradient>
                    </defs>
                    <circle cx="24" cy="24" r="22" stroke="url(#mtRing)" stroke-width="2"/>
                    <path d="M14 28c2-8 6-12 10-12s8 4 10 12" stroke="#99F6E4" stroke-width="2.2" stroke-linecap="round"/>
                    <path d="M18 22c1.5-3 4-5 6-5s4.5 2 6 5" stroke="#D1FAE5" stroke-width="2" stroke-linecap="round"/>
                    <circle cx="24" cy="30" r="3.2" fill="#6EE7B7"/>
                </svg>
            </motion-div>
            <motion-div class="mt-brand-copy">
                <motion-div class="mt-brand-title">MindTrack</motion-div>
                <motion-div class="mt-brand-sub">Riesgo académico · hábitos y bienestar</motion-div>
                <motion-div class="mt-brand-tags">
                    <span class="mt-tag-course">Sistemas Inteligentes</span>
                    <span class="mt-ui-ver">Calm · v2.3</span>
                </motion-div>
            </motion-div>
        </motion-div>
        """.replace("motion-div", "div"),
        unsafe_allow_html=True,
    )


def render_sidebar_status() -> None:
    with st.sidebar.container(border=True):
        st.markdown('<p class="mt-side-label">Motor en producción</p>', unsafe_allow_html=True)
        st.markdown(
            """
            <motion-div class="mt-side-status">
                <motion-div class="mt-side-status-head">
                    <span class="mt-side-pill">PRD</span>
                    <strong>XGBoost</strong>
                </motion-div>
                <p class="mt-side-note">
                    Consulta preventiva sin usar la nota académica dentro del modelo.
                </p>
                <motion-div class="mt-side-chips">
                    <span>Detección ≥ 85%</span>
                    <span>13 variables</span>
                    <span>Sin filtración</span>
                </motion-div>
            </motion-div>
            """.replace("motion-div", "div"),
            unsafe_allow_html=True,
        )


def panel_heading(title: str, subtitle: str = "") -> None:
    sub = f"<small>{_esc(subtitle)}</small>" if subtitle else ""
    st.markdown(
        f'<motion-div class="mt-panel-head"><span>{_esc(title)}</span>{sub}</motion-div>'.replace(
            "motion-div", "div"
        ),
        unsafe_allow_html=True,
    )


def profile_chips_header() -> None:
    st.markdown(
        '<p class="mt-chip-label">Perfiles de ejemplo</p>',
        unsafe_allow_html=True,
    )


def render_verdict_block(
    at_risk: bool,
    probability: float,
    threshold: float,
    risk_band: str = "",
) -> None:
    """Tarjeta señal MindTrack (sin estilo sello / veredicto tipo spam)."""
    mode = "alert" if at_risk else "stable"
    headline = "Señal de alerta académica" if at_risk else "Señal estable"
    clase = "Clase 1 · riesgo detectado" if at_risk else "Clase 0 · por debajo del umbral"
    band = risk_band or "—"
    tip = (
        "La probabilidad supera el umbral Validation del pipeline XGBoost."
        if at_risk
        else "Probabilidad menor al umbral; el modelo predice clase 0 en este perfil."
    )
    pct = max(0.0, min(100.0, probability * 100))
    thr_pct = max(0.0, min(100.0, threshold * 100))
    st.markdown(
        f"""
        <motion-div class="mt-signal-card mt-signal--{mode} mt-tip" data-tip="{_esc(tip)}">
            <motion-div class="mt-signal-rail" aria-hidden="true"></div>
            <motion-div class="mt-signal-ring-wrap">
                <motion-div class="mt-signal-ring" style="--pct: {pct:.2f}; --thr: {thr_pct:.2f};">
                    <motion-div class="mt-signal-ring-inner">
                        <b>{probability:.1%}</b>
                        <small>clase 1</small>
                    </motion-div>
                </motion-div>
            </div>
            <motion-div class="mt-signal-body">
                <span class="mt-signal-kicker">Lectura MindTrack</span>
                <h2>{_esc(headline)}</h2>
                <p>{_esc(clase)} · Banda <strong>{_esc(band)}</strong></p>
                <motion-div class="mt-signal-meta">
                    <span>Umbral PRD: <b>{threshold:.3f}</b></span>
                    <span>Δ vs umbral: <b>{(probability - threshold):+.1%}</b></span>
                </motion-div>
            </motion-div>
        </motion-div>
        """.replace("motion-div", "div"),
        unsafe_allow_html=True,
    )


def page_footer(env: str) -> None:
    st.markdown(
        f"""
        <footer class="mt-footer">
            <span>MindTrack · Sistemas Inteligentes</span>
            <span class="mt-footer-dot">·</span>
            <span>Modo {_esc(env)}</span>
            <span class="mt-footer-dot">·</span>
            <span>Prototipo universitario</span>
        </footer>
        """,
        unsafe_allow_html=True,
    )


def content_divider() -> None:
    st.markdown('<hr class="mt-divider" />', unsafe_allow_html=True)


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


def kpi_grid(cards: Iterable[tuple[str, str, str]]) -> None:
    """KPI cards with hover vignettes (value, label, tip)."""
    blocks = []
    accents = ("c0", "c1", "c2", "c3")
    for i, (value, label, tip) in enumerate(cards):
        ac = accents[i % len(accents)]
        blocks.append(
            f'<div class="mt-kpi mt-kpi-{ac} mt-tip" data-tip="{_esc(tip)}">'
            f"<b>{_esc(value)}</b><span>{_esc(label)}</span></div>"
        )
    st.markdown(
        f'<div class="mt-kpi-grid">{"".join(blocks)}</div>',
        unsafe_allow_html=True,
    )
    st.caption("Pasa el cursor sobre cada tarjeta para ver de dónde sale el dato.")


def insight_note(text: str, tip: str) -> None:
    st.markdown(
        f'<div class="mt-insight-note mt-tip" data-tip="{_esc(tip)}">{_esc(text)}</div>',
        unsafe_allow_html=True,
    )


def render_static_figure_gallery(
    entries: list[tuple[str, str, str]],
    base_dir: Path,
    *,
    heading: str = "Figuras del Colab (referencia estática)",
    lead: str = (
        "Capturas exportadas desde los notebooks de Google Colab; "
        "complementan las visualizaciones interactivas de esta sección."
    ),
    columns: int = 2,
) -> None:
    """Grid of static images (JPEG/PNG) with title and short caption."""
    if not entries:
        return
    st.markdown(f"#### {_esc(heading)}")
    st.caption(lead)
    cols = st.columns(columns)
    for i, (filename, title, description) in enumerate(entries):
        path = base_dir / filename
        with cols[i % columns]:
            st.markdown(
                f"<p class='mt-fig-title'>{_esc(title)}</p>",
                unsafe_allow_html=True,
            )
            if path.is_file():
                st.image(str(path), use_container_width=True)
                st.caption(description)
            else:
                st.warning(f"No se encontró `{filename}` en el repositorio.")


def section_heading(title: str, tip: str) -> None:
    st.markdown(
        f"""
        <div class="mt-section-head">
            <h3>{_esc(title)}</h3>
            <span class="mt-tip mt-info-dot" data-tip="{_esc(tip)}">i</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


LAB_NAV: list[tuple[str, str]] = [
    (
        "Panorama",
        "Números clave del estudio: cuántos estudiantes hay en los datos, "
        "qué tan frecuente es el riesgo y qué tan bien detecta el modelo los casos en alerta.",
    ),
    (
        "Huella de datos",
        "Gráficos interactivos del dataset más las figuras estáticas exportadas "
        "desde el EDA en Colab (balance, histogramas, correlación, etc.).",
    ),
    (
        "Trazabilidad ML",
        "Recorrido paso a paso de cómo se preparan los datos y se entrena el modelo, "
        "sin volver a entrenar desde esta pantalla.",
    ),
    (
        "Arena de modelos",
        "Comparación de tres métodos de aprendizaje automático y por qué MindTrack "
        "usa XGBoost en la consulta en vivo.",
    ),
]


def render_insight_nav(sections: list[str] | None = None) -> str:
    """Horizontal Insight navigation (main area, not sidebar)."""
    sections = sections or [s[0] for s in LAB_NAV]
    current = st.session_state.lab_section
    if current not in sections:
        st.session_state.lab_section = sections[0]
        current = sections[0]

    with st.container(border=True):
        st.markdown('<p class="mt-insight-nav-label">Explorar Insight</p>', unsafe_allow_html=True)
        cols = st.columns(len(sections))
        for col, name in zip(cols, sections):
            subtitle = next((h for n, h in LAB_NAV if n == name), "")
            with col:
                active = name == current
                btn_type = "primary" if active else "secondary"
                if st.button(
                    name,
                    key=f"insight_nav_{name}",
                    use_container_width=True,
                    type=btn_type,
                    help=subtitle,
                ):
                    st.session_state.lab_section = name
                    st.rerun()
    return st.session_state.lab_section


def render_env_switch() -> str:
    """Legacy sidebar switch (reservado; usar render_app_header)."""
    return render_app_header()


def timeline_block() -> None:
    steps = [
        ("01 · Integridad", "Validación de tipos, rangos y ausencia de faltantes."),
        ("02 · Anti-leakage", "Se excluye Academic_Performance_Score del modelado preventivo."),
        ("03 · Codificación", "Burnout ordinal · One-Hot en Gender y Education_Level."),
        ("04 · Partición", "70 % Train · 15 % Validation · 15 % Test (estratificado, seed 42)."),
        ("05 · Modelos", "Logistic Regression · Random Forest · XGBoost (oficial PRD)."),
        ("06 · Umbral", "Recall (C1) ≥ 0.85 en Validation; Test reservado para informe."),
    ]
    step_tips = {
        "01 · Integridad": (
            "Revisamos que cada fila del dataset tenga valores coherentes "
            "(edades válidas, escalas en rango, sin datos vacíos críticos)."
        ),
        "02 · Anti-leakage": (
            "No usamos la nota o desempeño académico directo en el modelo, "
            "para simular un escenario preventivo real."
        ),
        "03 · Codificación": (
            "Convertimos categorías (género, nivel educativo, burnout) a formato "
            "numérico que el algoritmo pueda aprender."
        ),
        "04 · Partición": (
            "Dividimos los datos en entrenamiento, validación y prueba "
            "para medir el modelo sin hacer trampa."
        ),
        "05 · Modelos": (
            "Entrenamos tres alternativas y guardamos la ganadora "
            "como motor de la consulta en producción."
        ),
        "06 · Umbral": (
            "Ajustamos el punto de corte para priorizar detectar estudiantes "
            "en verdadero riesgo (pocos falsos negativos)."
        ),
    }
    for title, text in steps:
        tip = step_tips.get(title, "")
        st.markdown(
            f"<div class='mt-step mt-tip' data-tip='{_esc(tip)}'><b>{title}</b><br/>"
            f"<span style='color:{COLORS['slate']}'>{text}</span></div>",
            unsafe_allow_html=True,
        )