"""Shared Streamlit CSS — MindTrack navy / white theme."""

from src.config import COLORS


def inject_css() -> str:
    green_on = "#22C55E"
    track_off = "#E8ECF1"
    return f"""
<!-- MindTrack UI build: contrast + depth -->
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;600;700&display=swap');
    html, body, [class*="css"] {{
        font-family: 'DM Sans', system-ui, sans-serif;
    }}
    .stApp {{
        background:
            radial-gradient(ellipse 80% 50% at 100% 0%, rgba(14,165,233,0.07), transparent 55%),
            radial-gradient(ellipse 70% 45% at 0% 100%, rgba(99,102,241,0.06), transparent 50%),
            linear-gradient(165deg, {COLORS["bg"]} 0%, #FFFFFF 45%, #F1F5F9 100%);
    }}
    section[data-testid="stSidebar"] {{
        background:
            radial-gradient(ellipse 120% 80% at -10% 0%, rgba(56,189,248,0.28), transparent 50%),
            radial-gradient(ellipse 90% 60% at 110% 85%, rgba(129,140,248,0.22), transparent 45%),
            radial-gradient(circle at 50% 40%, rgba(37,99,235,0.12), transparent 55%),
            linear-gradient(188deg, #020617 0%, #0B2544 32%, {COLORS["navy"]} 58%, #0C4A6E 100%);
        color: white;
        border-right: 1px solid rgba(125,211,252,0.15);
        box-shadow: inset -1px 0 0 rgba(255,255,255,0.04),
                    4px 0 24px rgba(2,6,23,0.15);
    }}
    section[data-testid="stSidebar"] [data-testid="stSidebarContent"] {{
        padding: 0.85rem 0.75rem 1.5rem;
    }}
    /* Sin color global en sidebar (evita texto blanco sobre fondos claros). */
    section[data-testid="stSidebar"] [data-testid="stMarkdown"] p,
    section[data-testid="stSidebar"] [data-testid="stMarkdown"] li {{
        color: #E2E8F0;
    }}
    section[data-testid="stSidebar"] h3 {{
        display: none;
    }}
    section[data-testid="stSidebar"] hr {{
        border: none;
        height: 1px;
        margin: 0.85rem 0;
        background: linear-gradient(
            90deg,
            transparent,
            rgba(125,211,252,0.35),
            rgba(129,140,248,0.25),
            transparent
        );
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
        position: relative;
        overflow: hidden;
        background: {COLORS["white"]};
        border: 1px solid {COLORS["border"]};
        border-radius: 20px;
        padding: 1.5rem 1.75rem 1.4rem;
        margin-bottom: 1.25rem;
        box-shadow: 0 16px 40px rgba(15, 23, 42, 0.08);
    }}
    .mt-hero::before {{
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, {COLORS["navy"]}, #38BDF8, {COLORS["accent"]});
    }}
    .mt-hero--prd {{
        background: linear-gradient(145deg, #FFFFFF 55%, #ECFDF5 100%);
    }}
    .mt-hero--prd::before {{
        background: linear-gradient(90deg, {COLORS["navy"]}, {COLORS["mint"]}, #22C55E);
    }}
    .mt-hero--lab {{
        background: linear-gradient(145deg, #FFFFFF 55%, #EFF6FF 100%);
    }}
    .mt-hero--lab::before {{
        background: linear-gradient(90deg, {COLORS["sky"]}, {COLORS["violet"]}, {COLORS["navy"]});
    }}
    .mt-hero-glow {{
        position: absolute;
        width: 220px;
        height: 220px;
        right: -80px;
        top: -120px;
        background: radial-gradient(circle, rgba(56,189,248,0.12) 0%, transparent 70%);
        pointer-events: none;
    }}
    .mt-badge-hero {{
        margin-bottom: 0.45rem;
        background: rgba(31,58,95,0.08);
        color: {COLORS["navy"]};
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
        background: linear-gradient(180deg, #FFFFFF 0%, #F8FAFC 100%);
        border: 1px solid {COLORS["border"]};
        border-left: 3px solid {COLORS["sky"]};
        border-radius: 12px;
        padding: 0.75rem 0.9rem;
        box-shadow: 0 2px 8px rgba(15,23,42,0.04);
    }}
    .block-container {{
        padding-top: 1.25rem;
        max-width: 1180px;
    }}
  /* PRD / LAB neumorphic segmented control */
    div[data-testid="stSidebar"] div[data-baseweb="segmented-control"] {{
        background: rgba(2,6,23,0.55) !important;
        border-radius: 999px !important;
        padding: 5px !important;
        box-shadow: inset 0 2px 8px rgba(0,0,0,0.45),
                    0 0 0 1px rgba(129,140,248,0.08) !important;
        border: 1px solid rgba(56,189,248,0.2) !important;
        min-height: 46px;
    }}
    div[data-testid="stSidebar"] div[data-baseweb="segmented-control"] button {{
        border-radius: 999px !important;
        font-weight: 800 !important;
        letter-spacing: 0.08em !important;
        font-size: 0.82rem !important;
        border: none !important;
        background: rgba(15,23,42,0.35) !important;
        color: #CBD5E1 !important;
        box-shadow: none !important;
        transition: all 0.25s ease;
    }}
    div[data-testid="stSidebar"] div[data-baseweb="segmented-control"] button p,
    div[data-testid="stSidebar"] div[data-baseweb="segmented-control"] button div {{
        color: inherit !important;
        -webkit-text-fill-color: currentColor !important;
        background: transparent !important;
    }}
    div[data-testid="stSidebar"] div[data-baseweb="segmented-control"] button[aria-selected="true"] {{
        background: linear-gradient(135deg, #4ADE80, #22C55E) !important;
        color: #052E16 !important;
        box-shadow: 0 4px 14px rgba(34,197,94,0.4),
            inset 0 -2px 0 rgba(0,0,0,0.08) !important;
    }}
    div[data-testid="stSidebar"] div[data-baseweb="segmented-control"] button[aria-selected="true"] p,
    div[data-testid="stSidebar"] div[data-baseweb="segmented-control"] button[aria-selected="true"] div {{
        color: #052E16 !important;
        -webkit-text-fill-color: #052E16 !important;
    }}
    div[data-testid="stSidebar"] div[data-baseweb="segmented-control"] button[aria-selected="false"] {{
        background: rgba(15,23,42,0.35) !important;
        color: #E2E8F0 !important;
        box-shadow: none !important;
    }}
    div[data-testid="stSidebar"] div[data-baseweb="segmented-control"] button[aria-selected="false"] p,
    div[data-testid="stSidebar"] div[data-baseweb="segmented-control"] button[aria-selected="false"] div {{
        color: #E2E8F0 !important;
        -webkit-text-fill-color: #E2E8F0 !important;
    }}
    div[data-testid="stSidebar"] div[data-baseweb="segmented-control"] button[aria-selected="false"]:hover {{
        background: rgba(56,189,248,0.15) !important;
        color: #F0F9FF !important;
    }}
    div[data-testid="stSidebar"] div[data-baseweb="segmented-control"] > div {{
        background: transparent !important;
        box-shadow: none !important;
    }}
    div[data-testid="stSidebar"] div[data-baseweb="segmented-control"] button {{
        -webkit-text-fill-color: unset !important;
    }}
    div[data-testid="stSidebar"] div[data-baseweb="segmented-control"] button[aria-selected="false"],
    div[data-testid="stSidebar"] div[data-baseweb="segmented-control"] button:not([aria-selected="true"]) {{
        background: rgba(15,23,42,0.72) !important;
        color: #F1F5F9 !important;
    }}
    div[data-testid="stSidebar"] div[data-baseweb="segmented-control"] button:not([aria-selected="true"]) p,
    div[data-testid="stSidebar"] div[data-baseweb="segmented-control"] button:not([aria-selected="true"]) div,
    div[data-testid="stSidebar"] div[data-baseweb="segmented-control"] button:not([aria-selected="true"]) span {{
        color: #F1F5F9 !important;
        -webkit-text-fill-color: #F1F5F9 !important;
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
    .mt-signal-card {{
        display: flex;
        align-items: center;
        gap: 1.35rem;
        flex-wrap: wrap;
        position: relative;
        padding: 1.1rem 1.25rem 1.1rem 1rem;
        margin: 0.35rem 0 1.1rem;
        border-radius: 20px;
        border: 1px solid {COLORS["border"]};
        background: {COLORS["white"]};
        box-shadow: 0 14px 36px rgba(15, 23, 42, 0.08);
        overflow: hidden;
    }}
    .mt-signal-rail {{
        position: absolute;
        left: 0;
        top: 0;
        bottom: 0;
        width: 6px;
    }}
    .mt-signal--alert .mt-signal-rail {{
        background: linear-gradient(180deg, {COLORS["amber"]}, {COLORS["accent"]});
    }}
    .mt-signal--stable .mt-signal-rail {{
        background: linear-gradient(180deg, {COLORS["mint"]}, {COLORS["ok"]});
    }}
    .mt-signal--alert {{
        background: linear-gradient(120deg, #FFFBEB 0%, #FFFFFF 45%, #FFF7ED 100%);
        border-color: #FCD34D;
    }}
    .mt-signal--stable {{
        background: linear-gradient(120deg, #ECFDF5 0%, #FFFFFF 50%, #F0FDFA 100%);
        border-color: #6EE7B7;
    }}
    .mt-signal-ring-wrap {{
        flex-shrink: 0;
        padding-left: 0.35rem;
    }}
    .mt-signal-ring {{
        width: 108px;
        height: 108px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
    }}
    .mt-signal--alert .mt-signal-ring {{
        background: conic-gradient(
            {COLORS["amber"]} 0%,
            {COLORS["accent"]} calc(var(--pct) * 1%),
            #FEE2E2 calc(var(--pct) * 1%),
            #FEE2E2 100%
        );
    }}
    .mt-signal--stable .mt-signal-ring {{
        background: conic-gradient(
            {COLORS["mint"]} 0%,
            {COLORS["ok"]} calc(var(--pct) * 1%),
            #D1FAE5 calc(var(--pct) * 1%),
            #D1FAE5 100%
        );
    }}
    .mt-signal-ring-inner {{
        width: 78px;
        height: 78px;
        border-radius: 50%;
        background: white;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        box-shadow: inset 0 0 0 1px rgba(15,23,42,0.06);
    }}
    .mt-signal-ring-inner b {{
        font-size: 1.15rem;
        color: {COLORS["navy"]};
        line-height: 1.1;
    }}
    .mt-signal-ring-inner small {{
        font-size: 0.62rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: {COLORS["mist"]};
    }}
    .mt-signal-body {{
        flex: 1;
        min-width: 200px;
    }}
    .mt-signal-kicker {{
        font-size: 0.68rem;
        font-weight: 800;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        color: {COLORS["violet"]};
    }}
    .mt-signal--alert .mt-signal-kicker {{ color: {COLORS["accent"]}; }}
    .mt-signal--stable .mt-signal-kicker {{ color: {COLORS["ok"]}; }}
    .mt-signal-body h2 {{
        margin: 0.2rem 0 0.35rem;
        font-size: 1.35rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        color: {COLORS["ink"]} !important;
    }}
    .mt-signal-body p {{
        margin: 0 0 0.55rem;
        font-size: 0.88rem;
        color: {COLORS["slate"]};
    }}
    .mt-signal-meta {{
        display: flex;
        flex-wrap: wrap;
        gap: 0.75rem 1.25rem;
        font-size: 0.78rem;
        color: {COLORS["slate"]};
    }}
    .mt-signal-meta b {{
        color: {COLORS["navy"]};
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
        border-top: 3px solid {COLORS["navy"]};
    }}
    .mt-kpi-c0 {{ border-top-color: {COLORS["sky"]}; background: linear-gradient(180deg, #F0F9FF 0%, #fff 55%); }}
    .mt-kpi-c1 {{ border-top-color: {COLORS["violet"]}; background: linear-gradient(180deg, #EEF2FF 0%, #fff 55%); }}
    .mt-kpi-c2 {{ border-top-color: {COLORS["mint"]}; background: linear-gradient(180deg, #F0FDFA 0%, #fff 55%); }}
    .mt-kpi-c3 {{ border-top-color: {COLORS["amber"]}; background: linear-gradient(180deg, #FFFBEB 0%, #fff 55%); }}
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
    /* Sidebar brand */
    .mt-brand {{
        position: relative;
        display: flex;
        align-items: center;
        gap: 0.8rem;
        margin-bottom: 0.85rem;
        padding: 0.9rem 0.85rem;
        border-radius: 16px;
        border: 1px solid rgba(125,211,252,0.22);
        background: linear-gradient(
            145deg,
            rgba(255,255,255,0.12) 0%,
            rgba(56,189,248,0.06) 45%,
            rgba(99,102,241,0.08) 100%
        );
        box-shadow: 0 12px 28px rgba(2,6,23,0.35),
            inset 0 1px 0 rgba(255,255,255,0.12);
        overflow: hidden;
    }}
    .mt-brand-glow {{
        position: absolute;
        right: -30px;
        top: -40px;
        width: 120px;
        height: 120px;
        background: radial-gradient(circle, rgba(56,189,248,0.35), transparent 70%);
        pointer-events: none;
    }}
    .mt-brand-mark {{
        width: 50px;
        height: 50px;
        flex-shrink: 0;
        filter: drop-shadow(0 4px 10px rgba(56,189,248,0.35));
    }}
    .mt-brand-mark svg {{
        width: 100%;
        height: 100%;
    }}
    .mt-brand-title {{
        font-size: 1.4rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        color: #F8FAFC !important;
        line-height: 1.05;
        text-shadow: 0 2px 12px rgba(56,189,248,0.25);
    }}
    .mt-brand-sub {{
        font-size: 0.74rem;
        color: #BAE6FD !important;
        margin-top: 0.2rem;
        line-height: 1.3;
    }}
    .mt-brand-tags span {{
        display: inline-block;
        margin-top: 0.45rem;
        margin-right: 0.25rem;
        font-size: 0.62rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: #7DD3FC !important;
        padding: 0.15rem 0.45rem;
        border-radius: 6px;
        background: rgba(14,165,233,0.15);
        border: 1px solid rgba(56,189,248,0.25);
    }}
    .mt-brand-tags .mt-ui-ver {{
        color: #052E16 !important;
        background: linear-gradient(135deg, #86EFAC, #4ADE80) !important;
        border-color: rgba(34,197,94,0.45) !important;
    }}
    .mt-side-glass {{
        border-radius: 14px;
        border: 1px solid rgba(125,211,252,0.18);
        background: rgba(15,23,42,0.45);
        backdrop-filter: blur(8px);
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.06),
                    0 8px 20px rgba(2,6,23,0.25);
        margin-bottom: 0.85rem;
        padding: 0.75rem 0.8rem;
    }}
    .mt-side-label {{
        margin: 0 0 0.5rem;
        font-size: 0.68rem;
        font-weight: 800;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        color: #7DD3FC !important;
    }}
    .mt-env-hint {{
        margin-top: 0.35rem;
        margin-bottom: 0 !important;
        padding: 0.45rem 0.55rem;
        border-radius: 10px;
        font-size: 0.76rem;
        line-height: 1.35;
        border: 1px solid rgba(255,255,255,0.06);
    }}
    .mt-env-hint--prd {{
        background: rgba(34,197,94,0.12);
        color: #BBF7D0 !important;
        border-color: rgba(34,197,94,0.22);
    }}
    .mt-env-hint--lab {{
        background: rgba(56,189,248,0.12);
        color: #BAE6FD !important;
        border-color: rgba(56,189,248,0.25);
    }}
    .mt-side-status-head {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 0.5rem;
        margin-bottom: 0.35rem;
    }}
    .mt-side-status-head strong {{
        font-size: 0.95rem;
        color: #E0F2FE !important;
        letter-spacing: 0.02em;
    }}
    .mt-side-pill {{
        font-size: 0.62rem;
        font-weight: 800;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        padding: 0.2rem 0.5rem;
        border-radius: 999px;
        color: #082F49 !important;
        background: linear-gradient(135deg, #7DD3FC, #38BDF8);
        box-shadow: 0 2px 8px rgba(56,189,248,0.35);
    }}
    .mt-side-note {{
        margin: 0 0 0.55rem;
        font-size: 0.72rem;
        line-height: 1.4;
        color: #94A3B8 !important;
    }}
    .mt-side-chips {{
        display: flex;
        flex-wrap: wrap;
        gap: 0.35rem;
    }}
    .mt-side-chips span {{
        font-size: 0.62rem;
        font-weight: 600;
        padding: 0.18rem 0.45rem;
        border-radius: 8px;
        color: #CBD5E1 !important;
        background: rgba(30,58,95,0.65);
        border: 1px solid rgba(148,163,184,0.2);
    }}
    div[data-testid="stSidebar"] .mt-badge {{
        background: rgba(255,255,255,0.12) !important;
        color: #E2E8F0 !important;
        border: 1px solid rgba(255,255,255,0.1);
    }}
    /* Form & panels */
    div[data-testid="stForm"] {{
        background: linear-gradient(165deg, #FFFFFF 0%, #F8FAFC 48%, #F1F5F9 100%);
        border: 1px solid #CBD5E1;
        border-top: 3px solid {COLORS["sky"]};
        border-radius: 18px;
        padding: 1.15rem 1.25rem 1.35rem;
        box-shadow: 0 16px 40px rgba(15,23,42,0.08),
                    inset 0 1px 0 rgba(255,255,255,0.85);
    }}
    div[data-testid="stForm"] [data-testid="column"] {{
        background: rgba(255,255,255,0.72);
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 0.55rem 0.65rem 0.15rem;
        box-shadow: 0 6px 18px rgba(31,58,95,0.06);
    }}
    div[data-testid="stForm"] [data-testid="stWidgetLabel"] p,
    div[data-testid="stForm"] label {{
        color: {COLORS["navy"]} !important;
        font-weight: 600 !important;
    }}
    .mt-chip-bar + div [data-testid="stHorizontalBlock"] .stButton > button,
    div.element-container:has(.mt-chip-label) + div.element-container .stButton > button {{
        border-radius: 12px !important;
        min-height: 2.75rem;
        font-weight: 700 !important;
        border: 1px solid #BFDBFE !important;
        background: linear-gradient(180deg, #FFFFFF, #EFF6FF) !important;
        color: {COLORS["navy"]} !important;
        box-shadow: 0 6px 0 #CBD5E1, 0 10px 20px rgba(37,99,235,0.12) !important;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }}
    .mt-chip-bar + div [data-testid="stHorizontalBlock"] .stButton > button:hover,
    div.element-container:has(.mt-chip-label) + div.element-container .stButton > button:hover {{
        transform: translateY(-1px);
        box-shadow: 0 7px 0 #93C5FD, 0 14px 24px rgba(37,99,235,0.16) !important;
    }}
    .mt-chip-bar + div [data-testid="stHorizontalBlock"] .stButton > button[kind="primary"],
    div.element-container:has(.mt-chip-label) + div.element-container .stButton > button[kind="primary"] {{
        border-color: #FCD34D !important;
        background: linear-gradient(180deg, #FEF3C7, #FDE68A) !important;
        color: #92400E !important;
        box-shadow: 0 6px 0 #D97706, 0 10px 20px rgba(180,83,9,0.2) !important;
    }}
    .mt-panel-head {{
        display: flex;
        flex-direction: column;
        gap: 0.15rem;
        margin: 0.15rem 0 0.5rem;
        padding-bottom: 0.35rem;
        border-bottom: 1px dashed {COLORS["border"]};
    }}
    .mt-panel-head span {{
        font-size: 0.78rem;
        font-weight: 800;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: {COLORS["navy"]};
    }}
    .mt-panel-head small {{
        font-size: 0.72rem;
        color: {COLORS["mist"]};
        font-weight: 500;
    }}
    .mt-chip-label {{
        font-size: 0.82rem;
        font-weight: 700;
        color: {COLORS["navy"]};
        margin: 0.25rem 0 0.35rem;
    }}
  .main div[data-testid="stVerticalBlock"] > div:has(.mt-chip-label) + div button {{
        border-radius: 12px !important;
        border: 1px solid {COLORS["border"]} !important;
        background: white !important;
        color: {COLORS["navy"]} !important;
        font-weight: 600 !important;
        transition: box-shadow 0.2s ease, transform 0.15s ease;
    }}
    .main div[data-testid="stVerticalBlock"] > div:has(.mt-chip-label) + div button:hover {{
        box-shadow: 0 6px 16px rgba(31,58,95,0.12);
        transform: translateY(-1px);
    }}
    .mt-divider {{
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, {COLORS["border"]}, transparent);
        margin: 1.25rem 0;
    }}
    [data-testid="stVerticalBlockBorderWrapper"]:has(.mt-insight-nav-label) {{
        background: {COLORS["white"]};
        border-color: {COLORS["border"]} !important;
        border-radius: 16px !important;
        padding: 0.55rem 0.75rem 0.45rem !important;
        margin-bottom: 1.1rem;
        box-shadow: 0 8px 22px rgba(15,23,42,0.05);
    }}
    [data-testid="stVerticalBlockBorderWrapper"]:has(.mt-insight-nav-label) .stButton > button {{
        border-radius: 12px !important;
        font-weight: 600 !important;
        font-size: 0.82rem !important;
        min-height: 2.65rem;
        border: 1px solid {COLORS["border"]} !important;
        transition: all 0.18s ease;
    }}
    [data-testid="stVerticalBlockBorderWrapper"]:has(.mt-insight-nav-label) .stButton > button[kind="primary"] {{
        background: linear-gradient(135deg, {COLORS["navy"]}, #2D4A73) !important;
        color: white !important;
        border-color: transparent !important;
        box-shadow: 0 6px 16px rgba(31,58,95,0.25);
    }}
    [data-testid="stVerticalBlockBorderWrapper"]:has(.mt-insight-nav-label) .stButton > button[kind="secondary"] {{
        background: #F8FAFC !important;
        color: {COLORS["slate"]} !important;
    }}
    section[data-testid="stSidebar"] [data-testid="stVerticalBlockBorderWrapper"]:has(.mt-side-label) {{
        background: rgba(15,23,42,0.45);
        border-color: rgba(125,211,252,0.22) !important;
        border-radius: 14px !important;
        padding: 0.55rem 0.65rem 0.6rem !important;
        margin-bottom: 0.85rem;
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.06),
                    0 8px 20px rgba(2,6,23,0.25);
    }}
    .mt-kpi:hover {{
        transform: translateY(-2px);
        box-shadow: 0 10px 22px rgba(15,23,42,0.08);
        border-color: #CBD5E1;
        transition: all 0.18s ease;
    }}
    .mt-card:hover {{
        border-color: #CBD5E1;
        box-shadow: 0 8px 20px rgba(15,23,42,0.06);
    }}
    .mt-step:hover {{
        border-left-color: {COLORS["accent"]};
        background: #FAFBFC;
    }}
    .mt-footer {{
        margin-top: 2rem;
        padding: 0.85rem 0 0.25rem;
        border-top: 1px solid {COLORS["border"]};
        font-size: 0.74rem;
        color: {COLORS["mist"]};
        display: flex;
        flex-wrap: wrap;
        gap: 0.35rem;
        align-items: center;
        justify-content: center;
    }}
    .mt-footer-dot {{
        opacity: 0.45;
    }}
    h3 {{
        color: {COLORS["navy"]} !important;
        letter-spacing: -0.02em;
    }}
    div[data-testid="stForm"] button[kind="primaryFormSubmit"] {{
        background: linear-gradient(180deg, #3B5F8C 0%, {COLORS["navy"]} 55%, #152A45 100%) !important;
        color: #F8FAFC !important;
        border: 1px solid #1E3A5F !important;
        border-radius: 14px !important;
        font-weight: 800 !important;
        letter-spacing: 0.02em;
        padding: 0.7rem 1rem !important;
        min-height: 3rem;
        box-shadow: 0 6px 0 #0B1F3A, 0 14px 28px rgba(31,58,95,0.28),
                    inset 0 1px 0 rgba(255,255,255,0.12) !important;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }}
    div[data-testid="stForm"] button[kind="primaryFormSubmit"]:hover {{
        transform: translateY(-1px);
        box-shadow: 0 7px 0 #0B1F3A, 0 18px 32px rgba(31,58,95,0.34),
                    inset 0 1px 0 rgba(255,255,255,0.15) !important;
    }}
    div[data-testid="stForm"] [data-baseweb="slider"] div[data-testid="stTickBar"] > div {{
        background: linear-gradient(90deg, {COLORS["sky"]}, {COLORS["navy"]}) !important;
    }}
    div[data-testid="stForm"] [data-baseweb="slider"] [role="slider"] {{
        background: {COLORS["navy"]} !important;
        box-shadow: 0 2px 8px rgba(31,58,95,0.35) !important;
    }}
    [data-testid="stAppViewContainer"] [data-baseweb="tab-list"] {{
        gap: 0.35rem;
    }}
</style>
"""