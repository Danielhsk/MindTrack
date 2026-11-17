"""Rule-based recommendation engine (no LLM)."""

from __future__ import annotations

from src.config import RULE_THRESHOLDS


def generate_recommendations(form: dict, max_items: int = 5) -> list[dict]:
    """Return prioritized recommendations from raw form values."""
    tips: list[dict] = []

    sleep = float(form.get("Sleep_Hours", 7))
    if sleep < RULE_THRESHOLDS["Sleep_Hours"]["max_ok"]:
        tips.append(
            {
                "priority": 1,
                "factor": "Sleep_Hours",
                "title": "Revisar hábitos de sueño",
                "detail": (
                    f"Reportas {sleep:.1f} h/día (umbral orientativo < "
                    f"{RULE_THRESHOLDS['Sleep_Hours']['max_ok']:.0f} h). "
                    "Prioriza horarios regulares y descanso suficiente."
                ),
            }
        )

    social = float(form.get("Daily_Social_Media_Hours", 0))
    if social > RULE_THRESHOLDS["Daily_Social_Media_Hours"]["min_ok"]:
        tips.append(
            {
                "priority": 2,
                "factor": "Daily_Social_Media_Hours",
                "title": "Moderar tiempo en redes sociales",
                "detail": (
                    f"Uso diario reportado: {social:.1f} h (umbral orientativo > "
                    f"{RULE_THRESHOLDS['Daily_Social_Media_Hours']['min_ok']:.1f} h). "
                    "Define bloques sin pantallas en periodos de estudio."
                ),
            }
        )

    activity = float(form.get("Physical_Activity_Hours", 1))
    if activity < RULE_THRESHOLDS["Physical_Activity_Hours"]["max_ok"]:
        tips.append(
            {
                "priority": 3,
                "factor": "Physical_Activity_Hours",
                "title": "Incorporar actividad física",
                "detail": (
                    f"Actividad reportada: {activity:.2f} h/día. "
                    "Sesiones cortas y constantes suelen ayudar al bienestar general."
                ),
            }
        )

    mental = float(form.get("Mental_Health_Score", 70))
    if mental < RULE_THRESHOLDS["Mental_Health_Score"]["max_ok"]:
        tips.append(
            {
                "priority": 4,
                "factor": "Mental_Health_Score",
                "title": "Atención al bienestar mental",
                "detail": (
                    f"Mental_Health_Score = {mental:.1f} (umbral orientativo < "
                    f"{RULE_THRESHOLDS['Mental_Health_Score']['max_ok']:.0f}). "
                    "Considera apoyo institucional o hábitos de autocuidado."
                ),
            }
        )

    isolation = float(form.get("Social_Isolation_Score", 4))
    if isolation > RULE_THRESHOLDS["Social_Isolation_Score"]["min_ok"]:
        tips.append(
            {
                "priority": 5,
                "factor": "Social_Isolation_Score",
                "title": "Reducir aislamiento social",
                "detail": (
                    f"Social_Isolation_Score = {isolation:.1f}. "
                    "Participar en grupos académicos o redes de apoyo puede ayudar."
                ),
            }
        )

    burnout = str(form.get("Burnout_Level", "Low"))
    if burnout in RULE_THRESHOLDS["Burnout_Level"]["severe_codes"]:
        tips.append(
            {
                "priority": 0,
                "factor": "Burnout_Level",
                "title": "Monitorear Burnout_Level",
                "detail": (
                    f"Nivel reportado: {burnout}. En el dataset, el riesgo académico "
                    "se concentra en High / Severe. Busca estrategias de carga y descanso."
                ),
            }
        )

    tips.sort(key=lambda x: x["priority"])
    if not tips:
        tips.append(
            {
                "priority": 99,
                "factor": "General",
                "title": "Mantener hábitos saludables",
                "detail": (
                    "El perfil no activa reglas de alerta. Conserva sueño, actividad "
                    "y equilibrio digital para sostener el desempeño académico."
                ),
            }
        )
    return tips[:max_items]
