"""Interactive Plotly visualizations for MindTrack Insight (read-only)."""

from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from src.config import BURNOUT_ORDER, COLORS, DATA_PATH, TARGET

MT_SEQ = [COLORS["navy"], COLORS["slate"], COLORS["accent"]]

SCATTER_METRIC_OPTIONS: list[tuple[str, str]] = [
    ("Sleep_Hours", "Horas de sueño"),
    ("Daily_Social_Media_Hours", "Horas en redes sociales"),
    ("Mental_Health_Score", "Bienestar mental"),
    ("Social_Isolation_Score", "Aislamiento social"),
]

METRIC_LABELS_ES = dict(SCATTER_METRIC_OPTIONS)


def load_dataset() -> pd.DataFrame:
    return pd.read_csv(DATA_PATH)


def fig_metric_vs_risk_jitter(
    df: pd.DataFrame,
    metric_col: str,
    *,
    sample_n: int = 2500,
    seed: int = 42,
) -> go.Figure:
    """Scatter con jitter vertical para riesgo binario (solo visualización)."""
    sample = df[[metric_col, TARGET]].sample(min(sample_n, len(df)), random_state=seed).copy()
    rng = np.random.default_rng(seed)
    sample["_y_plot"] = sample[TARGET].astype(float) + rng.uniform(-0.14, 0.14, len(sample))
    x_label = METRIC_LABELS_ES.get(metric_col, metric_col)
    fig = px.scatter(
        sample,
        x=metric_col,
        y="_y_plot",
        color=TARGET,
        opacity=0.4,
        color_discrete_map={0: COLORS["ok"], 1: COLORS["accent"]},
        labels={
            metric_col: x_label,
            "_y_plot": "Riesgo académico",
            TARGET: "Riesgo",
        },
        title=f"{x_label} frente a riesgo académico (muestra aleatoria)",
    )
    fig.update_yaxes(
        tickvals=[0, 1],
        ticktext=["Sin riesgo (0)", "En riesgo (1)"],
        range=[-0.28, 1.28],
        title="Riesgo académico",
    )
    fig.update_layout(
        height=400,
        margin=dict(t=50, b=40, l=10, r=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend_title_text="Resultado",
    )
    return fig


def fig_class_balance(df: pd.DataFrame) -> go.Figure:
    counts = df[TARGET].value_counts().sort_index()
    labels = ["Sin riesgo (0)", "En riesgo (1)"]
    fig = px.bar(
        x=labels,
        y=counts.values,
        color=labels,
        color_discrete_map={
            labels[0]: COLORS["ok"],
            labels[1]: COLORS["accent"],
        },
        text=[f"{v:,}" for v in counts.values],
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(
        title="Distribución de Academic_Failure_Risk",
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=340,
        margin=dict(t=50, b=40),
    )
    return fig


def fig_burnout_risk(df: pd.DataFrame) -> go.Figure:
    pct = (
        df.groupby("Burnout_Level")[TARGET]
        .value_counts(normalize=True)
        .unstack(fill_value=0)
        .reindex(BURNOUT_ORDER)
        * 100
    )
    fig = go.Figure()
    fig.add_bar(name="Sin riesgo (0)", x=pct.index, y=pct[0], marker_color=COLORS["ok"])
    fig.add_bar(name="En riesgo (1)", x=pct.index, y=pct[1], marker_color=COLORS["accent"])
    fig.update_layout(
        barmode="stack",
        title="Riesgo académico por Burnout_Level (%)",
        yaxis_title="%",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=360,
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
    )
    return fig


def fig_correlation_target(df: pd.DataFrame, top_n: int = 10) -> go.Figure:
    num = df.copy()
    num["Burnout_Level"] = num["Burnout_Level"].map(
        {k: v for k, v in zip(BURNOUT_ORDER, range(4))}
    )
    corr = num.select_dtypes(include="number").corr()[TARGET].drop(TARGET)
    corr = corr.reindex(corr.abs().sort_values(ascending=False).head(top_n).index)
    colors = [COLORS["accent"] if v > 0 else COLORS["navy"] for v in corr.values]
    fig = go.Figure(go.Bar(x=corr.values, y=corr.index, orientation="h", marker_color=colors))
    fig.update_layout(
        title="Correlación de Pearson con el riesgo",
        xaxis_title="r",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=380,
    )
    return fig


def fig_model_metrics(comparison: pd.DataFrame, metric: str) -> go.Figure:
    df = comparison.set_index("Modelo") if "Modelo" in comparison.columns else comparison
    fig = px.bar(
        df.reset_index(),
        x="Modelo",
        y=metric,
        color="Modelo",
        color_discrete_sequence=MT_SEQ,
        text=df[metric].map(lambda x: f"{x:.3f}"),
    )
    fig.update_traces(textposition="outside")
    ymin, ymax = 0, min(1.05, df[metric].max() * 1.15)
    if metric == "Recall (C1)":
        fig.add_hline(y=0.85, line_dash="dot", line_color=COLORS["accent"])
    fig.update_layout(
        showlegend=False,
        yaxis_range=[ymin, ymax],
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=320,
        margin=dict(t=40),
    )
    return fig


def fig_metrics_radar(comparison: pd.DataFrame) -> go.Figure:
    df = comparison.set_index("Modelo") if "Modelo" in comparison.columns else comparison
    metrics = ["Recall (C1)", "F1-Score (C1)", "PR-AUC", "ROC-AUC", "Precision (C1)"]
    fig = go.Figure()
    for i, model in enumerate(df.index):
        values = [df.loc[model, m] for m in metrics]
        fig.add_trace(
            go.Scatterpolar(
                r=values + [values[0]],
                theta=metrics + [metrics[0]],
                fill="toself",
                name=model,
                line_color=MT_SEQ[i % len(MT_SEQ)],
                opacity=0.65,
            )
        )
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
        title="Perfil de métricas · Validation",
        paper_bgcolor="rgba(0,0,0,0)",
        height=420,
        legend=dict(orientation="h", y=-0.15),
    )
    return fig


def fig_fn_fp(comparison: pd.DataFrame) -> go.Figure:
    df = comparison.set_index("Modelo") if "Modelo" in comparison.columns else comparison
    fig = go.Figure()
    fig.add_trace(go.Bar(name="FN", x=df.index, y=df["FN"], marker_color=COLORS["accent"]))
    fig.add_trace(go.Bar(name="FP", x=df.index, y=df["FP"], marker_color=COLORS["slate"]))
    fig.update_layout(
        barmode="group",
        title="Errores FN / FP · Validation",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=340,
    )
    return fig