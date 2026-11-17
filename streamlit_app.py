"""Root entrypoint for Streamlit Community Cloud (optional; also use app/streamlit_app.py)."""

from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent
APP_FILE = ROOT / "app" / "streamlit_app.py"

spec = importlib.util.spec_from_file_location("mindtrack_streamlit_app", APP_FILE)
if spec is None or spec.loader is None:
    raise RuntimeError(f"Cannot load MindTrack app from {APP_FILE}")

module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

# exec_module sets __name__ != "__main__", so the app's guard never runs on Cloud.
if hasattr(module, "main"):
    module.main()