"""Shared Streamlit CSS — MindTrack navy / white theme."""

from src.config import COLORS


def inject_css() -> str:
    return f"""
<style>
    .stApp {{
        background: linear-gradient(180deg, {COLORS["bg"]} 0%, #FFFFFF 40%);
    }}
    section[data-testid="stSidebar"] {{
        background: {COLORS["navy"]};
        color: white;
    }}
    section[data-testid="stSidebar"] * {{
        color: #F8FAFC !important;
    }}
    section[data-testid="stSidebar"] .stRadio label {{
        color: #F8FAFC !important;
    }}
    .mt-hero {{
        background: {COLORS["white"]};
        border: 1px solid {COLORS["border"]};
        border-radius: 16px;
        padding: 1.25rem 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06);
    }}
    .mt-hero h1 {{
        color: {COLORS["navy"]};
        margin: 0 0 0.35rem 0;
        font-size: 1.75rem;
        letter-spacing: -0.02em;
    }}
    .mt-hero p {{
        color: {COLORS["slate"]};
        margin: 0;
        font-size: 0.95rem;
    }}
    .mt-card {{
        background: {COLORS["white"]};
        border: 1px solid {COLORS["border"]};
        border-radius: 14px;
        padding: 1rem 1.1rem;
        margin-bottom: 0.75rem;
    }}
    .mt-badge {{
        display: inline-block;
        padding: 0.2rem 0.65rem;
        border-radius: 999px;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.04em;
        background: #E2E8F0;
        color: {COLORS["navy"]};
    }}
    .mt-badge-risk {{
        background: #FEF3C7;
        color: {COLORS["accent"]};
    }}
    .mt-badge-ok {{
        background: #DCFCE7;
        color: {COLORS["ok"]};
    }}
    .mt-disclaimer {{
        font-size: 0.82rem;
        color: {COLORS["slate"]};
        border-left: 3px solid {COLORS["navy"]};
        padding-left: 0.75rem;
        margin-top: 1rem;
    }}
    div[data-testid="stMetric"] {{
        background: {COLORS["white"]};
        border: 1px solid {COLORS["border"]};
        border-radius: 12px;
        padding: 0.75rem 0.9rem;
    }}
    .block-container {{
        padding-top: 1.5rem;
        max-width: 1100px;
    }}
</style>
"""
