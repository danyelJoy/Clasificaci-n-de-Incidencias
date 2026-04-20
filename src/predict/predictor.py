from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

from src.predict.load_model import load_model
from src.predict.rules import get_confidence_status, assign_priority

MODEL_PATH = Path("models/ticket_classifier.joblib")
_model = None


def get_model():
    global _model
    if _model is None:
        _model = load_model(MODEL_PATH)
    return _model

def predict_ticket(text: str)-> Dict[str, Any]:
    """
    Ejecuta la predicción completa para un ticket.
    Devuelve categoría, confianza, estado de confianza, prioridad y motivo
    """
    if not text or not text.strip():
        raise ValueError("El texto del ticket no puede estar vacío.")
    model = get_model()

    prediction = model.predict([text])[0]
    confidence = float(model.predict_proba([text]).max())

    confidence_status = get_confidence_status(confidence)
    priority, reason = assign_priority(prediction, confidence)

    return {
        "category": prediction,
        "confidence":round(confidence,4),
        "confidence_status": confidence_status,
        "priority": priority,
        "reason": reason,
    }