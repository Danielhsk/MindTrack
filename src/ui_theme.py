"""Shared Streamlit CSS — MindTrack navy / white theme."""

from src.config import COLORS


def inject_css() -> str:
    green_on = "#22C55E"
    track_off = "#E8ECF1"
    return f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;600;700&display=swap');
    html, body, [class*="css"] {{
        font-family: 'DM Sans', system-ui, sans-serif;
    }}
    .stApp {{
        background: linear-gradient(165deg, {COLORS["bg"]} 0%, #FFFFFF 45%, #F1F5F9 100%);
    }}
    section[data-testid="stSidebar"] {{
        background: linear-gradient(180deg, #0B1F3A 0%, {COLORS["navy"]} 55%, #1E3A5F 100%);
        color: white;
        border-right: 1px solid rgba(255,255,255,0.06);
    }}
    section[data-testid="stSidebar"] * {{
        color: #F8FAFC !important;
    }}
    section[data-testid="stSidebar"] .stMarkdown small {{
        color: #CBD5E1 !important;
    }}
    .mt-eyebrow {{
        text-transform: uppercase;
        letter-spacing: 0.14em;
        font-size: 0.72rem;
        font-weight: 700;
        color: {COLORS["slate"]};
        margin: 0 0 0.25rem 0;
    }}
    .mt-hero {{
        background: {COLORS["white"]};
        border: 1px solid {COLORS["border"]};
        border-radius: 18px;
        padding: 1.35rem 1.6rem;
        margin-bottom: 1.1rem;
        box-shadow: 0 12px 32px rgba(15, 23, 42, 0.07);
    }}
    .mt-hero h1 {{
        color: {COLORS["navy"]};
        margin: 0.25rem 0 0.4rem 0;
        font-size: 1.85rem;
        letter-spacing: -0.03em;
        font-weight: 700;
    }}
    .mt-hero p {{
        color: {COLORS["slate"]};
        margin: 0;
        font-size: 0.98rem;
        line-height: 1.45;
    }}
    .mt-card {{
        background: {COLORS["white"]};
        border: 1px solid {COLORS["border"]};
        border-radius: 14px;
        padding: 1rem 1.1rem;
        margin-bottom: 0.75rem;
        box-shadow: 0 4px 14px rgba(15,23,42,0.04);
    }}
    .mt-badge {{
        display: inline-block;
        padding: 0.22rem 0.7rem;
        border-radius: 999px;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.06em;
        text-transform: uppercase;
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
        box-shadow: 0 2px 8px rgba(15,23,42,0.04);
    }}
    .block-container {{
        padding-top: 1.25rem;
        max-width: 1180px;
    }}
    .mt-env-hint {{
        font-size: 0.78rem;
        color: #CBD5E1 !important;
        margin-top: -0.35rem;
        margin-bottom: 0.75rem;
        line-height: 1.35;
    }}
  /* PRD / LAB neumorphic segmented control */
    div[data-testid="stSidebar"] div[data-baseweb="segmented-control"] {{
        background: #0F172A !important;
        border-radius: 999px !important;
        padding: 5px !important;
        box-shadow: inset 0 2px 6px rgba(0,0,0,0.35);
        border: 1px solid rgba(255,255,255,0.08) !important;
        min-height: 46px;
    }}
    div[data-testid="stSidebar"] div[data-baseweb="segmented-control"] button {{
        border-radius: 999px !important;
        font-weight: 700 !important;
        letter-spacing: 0.08em !important;
        font-size: 0.82rem !important;
        border: none !important;
        background: transparent !important;
        color: #94A3B8 !important;
        box-shadow: none !important;
        transition: all 0.25s ease;
    }}
    div[data-testid="stSidebar"] div[data-baseweb="segmented-control"] button[aria-selected="true"] {{
        background: {green_on} !important;
        color: #052E16 !important;
        box-shadow: 0 4px 14px rgba(34,197,94,0.45),
            inset 0 -2px 0 rgba(0,0,0,0.08) !important;
    }}
    div[data-testid="stSidebar"] div[data-baseweb="segmented-control"] button[aria-selected="true"],
    div[data-testid="stSidebar"] div[data-baseweb="segmented-control"] button[aria-selected="true"] div,
    div[data-testid="stSidebar"] div[data-baseweb="segmented-control"] button[aria-selected="true"] p {{
        color: #052E16 !important;
        -webkit-text-fill-color: #052E16 !important;
    }}
    div[data-testid="stSidebar"] div[data-baseweb="segmented-control"] button[aria-selected="false"],
    div[data-testid="stSidebar"] div[data-baseweb="segmented-control"] button[aria-selected="false"] > div {{
        background: transparent !important;
        color: #E2E8F0 !important;
        box-shadow: none !important;
    }}
    div[data-testid="stSidebar"] div[data-baseweb="segmented-control"] button[aria-selected="false"] p {{
        color: #E2E8F0 !important;
        -webkit-text-fill-color: #E2E8F0 !important;
    }}
    div[data-testid="stSidebar"] div[data-baseweb="segmented-control"] button[aria-selected="false"]:hover {{
        color: #F8FAFC !important;
        background: rgba(255,255,255,0.06) !important;
    }}
    /* Horizontal radio fallback */
    div[data-testid="stSidebar"] .stRadio > div {{
        flex-direction: row !important;
        background: #0F172A;
        border-radius: 999px;
        padding: 4px;
        box-shadow: inset 0 2px 6px rgba(0,0,0,0.35);
    }}
    div[data-testid="stSidebar"] .stRadio label {{
        border-radius: 999px !important;
        padding: 0.45rem 1.1rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.08em;
    }}
    .mt-verdict {{
        display: flex;
        align-items: center;
        gap: 1.25rem;
        margin: 0.75rem 0 1rem;
        flex-wrap: wrap;
    }}
    .mt-stamp {{
        font-size: 1.35rem;
        font-weight: 800;
        letter-spacing: 0.12em;
        padding: 0.65rem 1.1rem;
        border-radius: 12px;
        border: 3px solid;
        transform: rotate(-4deg);
        box-shadow: 0 6px 0 rgba(0,0,0,0.08);
    }}
    .stamp-risk {{
        color: {COLORS["accent"]};
        border-color: {COLORS["accent"]};
        background: #FFFBEB;
    }}
    .stamp-safe {{
        color: {COLORS["ok"]};
        border-color: {COLORS["ok"]};
        background: #F0FDF4;
    }}
    .mt-prob b {{
        font-size: 1.75rem;
        color: {COLORS["navy"]};
        display: block;
    }}
    .mt-prob small {{
        color: {COLORS["slate"]};
        font-size: 0.78rem;
    }}
    .mt-gauge-wrap {{
        margin: 0.5rem 0 1.25rem;
    }}
    .mt-gauge {{
        position: relative;
        height: 14px;
        border-radius: 999px;
        background: {track_off};
        box-shadow: inset 0 2px 5px rgba(0,0,0,0.08);
        overflow: visible;
    }}
    .mt-gauge i {{
        display: block;
        height: 100%;
        border-radius: 999px;
        background: linear-gradient(90deg, {COLORS["navy"]}, {COLORS["accent"]});
        box-shadow: 0 2px 8px rgba(180,83,9,0.35);
    }}
    .mt-gauge u {{
        position: absolute;
        top: -5px;
        width: 3px;
        height: 24px;
        background: {COLORS["navy"]};
        border-radius: 2px;
        text-decoration: none;
        box-shadow: 0 0 0 2px white;
    }}
    .mt-gauge-labels {{
        display: flex;
        justify-content: space-between;
        font-size: 0.72rem;
        color: {COLORS["slate"]};
        margin-top: 0.35rem;
    }}
    .mt-step {{
        background: {COLORS["white"]};
        border: 1px solid {COLORS["border"]};
        border-left: 4px solid {COLORS["navy"]};
        border-radius: 0 12px 12px 0;
        padding: 0.75rem 1rem;
        margin-bottom: 0.55rem;
        font-size: 0.9rem;
    }}
    .mt-kpi-grid {{
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 0.65rem;
        margin-bottom: 1rem;
    }}
    @media (max-width: 900px) {{
        .mt-kpi-grid {{ grid-template-columns: repeat(2, 1fr); }}
    }}
    .mt-kpi {{
        background: white;
        border: 1px solid {COLORS["border"]};
        border-radius: 12px;
        padding: 0.85rem;
        text-align: center;
    }}
    .mt-kpi b {{
        display: block;
        font-size: 1.25rem;
        color: {COLORS["navy"]};
    }}
    .mt-kpi span {{
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: {COLORS["slate"]};
    }}
    .mt-tip {{
        position: relative;
        cursor: help;
    }}
    .mt-tip::after {{
        content: attr(data-tip);
        position: absolute;
        left: 50%;
        bottom: calc(100% + 8px);
        transform: translateX(-50%);
        width: max-content;
        max-width: 260px;
        padding: 0.45rem 0.65rem;
        font-size: 0.74rem;
        line-height: 1.35;
        font-weight: 500;
        color: #F8FAFC;
        background: #0F172A;
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 10px;
        box-shadow: 0 8px 20px rgba(15, 23, 42, 0.22);
        opacity: 0;
        visibility: hidden;
        pointer-events: none;
        transition: opacity 0.15s ease, visibility 0.15s ease;
        z-index: 50;
        text-transform: none;
        letter-spacing: normal;
        text-align: left;
    }}
    .mt-tip:hover::after {{
        opacity: 1;
        visibility: visible;
    }}
    .mt-kpi.mt-tip::after {{
        white-space: normal;
    }}
    .mt-insight-note {{
        background: #E0F2FE;
        border: 1px solid #BAE6FD;
        color: #0C4A6E;
        border-radius: 12px;
        padding: 0.85rem 1rem;
        font-size: 0.92rem;
        margin: 0.5rem 0 1rem;
    }}
    .mt-insight-nav-label {{
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: {COLORS["slate"]};
        margin: 0 0 0.35rem 0;
    }}
    .mt-section-head {{
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin: 0.5rem 0 0.25rem;
    }}
    .mt-section-head h3 {{
        margin: 0;
        font-size: 1.05rem;
        color: {COLORS["navy"]};
    }}
    .mt-info-dot {{
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 1.15rem;
        height: 1.15rem;
        border-radius: 50%;
        font-size: 0.7rem;
        font-weight: 800;
        background: {COLORS["navy"]};
        color: white;
        flex-shrink: 0;
    }}
    .mt-info-dot::after {{
        bottom: calc(100% + 6px);
        left: 0;
        transform: none;
    }}
</style>
"""