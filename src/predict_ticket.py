# import joblib
# from pathlib import Path
 

# def load_model(model_path):
#     model = joblib.load(model_path)
#     return model

# def predict_ticket(model, text):

#     prediction = model.predict([text])[0]
#     probs = model.predict_proba([text]).max()

#     return prediction, probs

# def main():
#     BASE_DIR = Path(__file__).resolve().parent.parent
#     MODEL_PATH = BASE_DIR / "models/ticket_classifier.joblib"

#     print("Cargando modelo..")

#     model = load_model(MODEL_PATH)

#     print("\n Escribe un ticket ( o 'exit'): ")

#     while True:
#         text = input("\Ticket:")
#         if text.lower() == "exit":
#             break

#         pred, prob = predict_ticket(model, text)

#         print("\nCategoría:", pred)
#         print("Confianza:", round(prob, 3))

# if __name__ == "__main__":
#     main()
    
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

from src.predict.load_model import load_model
from src.predict.rules import get_confidence_status, assign_priority

MODEL_PATH = Path ("models/modelo_tfidf_lr.pkl")
_model = None

def get_model():
    """
    Carga el modelo solo una vez (lazy loading)
    """
    global _model

    if _model is None:
        _model  = load_model(MODEL_PATH)

    return _model

def predict_ticket(text: str)->Dict[str, Any]:
    """
    Ejecuta la predicción completa para un ticket.
    """
    if not text or not text.strip():
        raise ValueError("El textto del ticket no puede estar vacío.")
    
    model = get_model()

    prediction = model.predict([text].max())
    confidence = float(model.predict_proba([text]).max())
    confidence_status = get_confidence_status(confidence)
    priority, reason = assign_priority(prediction, confidence)

    return {
        "category": prediction,
        "confidence": round(confidence, 4),
        "confidence_status": confidence_status,
        "priority":priority,
        "reason": reason,
    }
