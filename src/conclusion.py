"""Dynamic conclusion templates for the Production dashboard."""

from __future__ import annotations


def build_conclusion(
    prediction: dict,
    recommendations: list[dict],
    top_factors: list[str] | None = None,
) -> str:
    band = prediction["risk_band"]
    proba = prediction["probability"]
    model = prediction["model_label"]
    cls = "en riesgo (clase 1)" if prediction["predicted_class"] == 1 else "sin riesgo (clase 0)"

    factors = ", ".join(top_factors[:4]) if top_factors else "hábitos digitales y bienestar"
    recs = "; ".join(r["title"] for r in recommendations[:3])

    return (
        f"El análisis con **{model}** estima un nivel de riesgo académico **{band}** "
        f"(probabilidad de clase positiva ≈ {proba:.1%}). "
        f"La decisión binaria con el umbral de Validation ({prediction['threshold']:.3f}) "
        f"clasifica al estudiante como **{cls}**.\n\n"
        f"Los factores más relevantes en la explicación se relacionan con: **{factors}**.\n\n"
        f"Se sugiere prestar atención a: **{recs}**.\n\n"
        "Este resultado es **orientativo**: refleja patrones aprendidos sobre el dataset "
        "disponible. **No constituye un diagnóstico médico, psicológico ni una decisión "
        "institucional definitiva**. Correlación/predicción ≠ causalidad."
    )
