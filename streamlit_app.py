"""Root entrypoint for Streamlit Community Cloud.

Cloud ejecuta este archivo (no app/streamlit_app.py). set_page_config debe ser
el primer comando Streamlit, antes de importar app/ (donde hay @st.cache_data).
"""

from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

st.set_page_config(
    page_title="MindTrack",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.streamlit_app import main

main()