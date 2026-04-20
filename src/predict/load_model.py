from __future__ import annotations

import joblib
from pathlib import Path
from typing import Any

def load_model(model_path: Path)-> Any:
    """
    Carga del modelo entrenado desde archivo .pkl o .joblib.
    """
    if not model_path.exists():
        raise FileNotFoundError(f"No se encontró el modelo en: {model_path}")
    return joblib.load(model_path)

