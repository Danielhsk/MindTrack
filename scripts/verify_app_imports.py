"""Smoke test: run before deploy (`python scripts/verify_app_imports.py`)."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.colab_assets import ASSETS_COLAB_DIR, COLAB_EDA_GALLERY, ML_EXPORT_GALLERY  # noqa: E402
from src.config import FIGURES_DIR  # noqa: E402

assert ASSETS_COLAB_DIR.is_dir(), f"Missing {ASSETS_COLAB_DIR}"
assert COLAB_EDA_GALLERY, "COLAB_EDA_GALLERY empty"
assert ML_EXPORT_GALLERY, "ML_EXPORT_GALLERY empty"
for name, _, _ in ML_EXPORT_GALLERY:
    assert (FIGURES_DIR / name).is_file(), f"Missing {FIGURES_DIR / name}"

APP = ROOT / "app" / "streamlit_app.py"
spec = importlib.util.spec_from_file_location("mindtrack_streamlit_app", APP)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
# Do not call main(); only ensure module loads without ImportError.
spec.loader.exec_module(module)
print("verify_app_imports: OK")