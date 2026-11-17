"""Helpers: formulario PRD en español con valores internos en inglés."""

from __future__ import annotations

import streamlit as st

from src.config import (
    FORM_BURNOUT_ES,
    FORM_CATEGORICAL,
    FORM_EDUCATION_ES,
    FORM_GENDER_ES,
)


def _select_es(
    label: str,
    options_en: list[str],
    labels_es: dict[str, str],
    default_en: str,
) -> str:
    display = [labels_es[o] for o in options_en]
    reverse = {labels_es[o]: o for o in options_en}
    idx = options_en.index(default_en)
    chosen = st.selectbox(label, display, index=idx)
    return reverse[chosen]


def categorical_gender(default_en: str) -> str:
    return _select_es(
        "Género",
        FORM_CATEGORICAL["Gender"],
        FORM_GENDER_ES,
        default_en,
    )


def categorical_education(default_en: str) -> str:
    return _select_es(
        "Nivel educativo",
        FORM_CATEGORICAL["Education_Level"],
        FORM_EDUCATION_ES,
        default_en,
    )


def categorical_burnout(default_en: str) -> str:
    return _select_es(
        "Nivel de burnout",
        FORM_CATEGORICAL["Burnout_Level"],
        FORM_BURNOUT_ES,
        default_en,
    )