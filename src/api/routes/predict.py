
from  __future__ import annotations
    
from pathlib import Path
from typing import Any

from fastapi import APIRouter,  HTTPException, status

from src.config import setup_logger
from src.api.schemas import TicketRequest, PredictionResponse, ErrorResponse
from src.predict.predictor import predict_ticket
from src.predict.utils import append_prediction_to_csv

router = APIRouter(prefix="", tags=["Prediction"])


logger = setup_logger()
CSV_PATH = Path("data/outputs/predictions.csv")



@router.get("/", summary="Mensaje de bienvenida")
def root() -> dict:
    """
    Endpoint base para verificar que la API está activa
    """
    return {"message":"API de clasificación de incidencias activa"}

@router.get("/health", summary="Estado del servicio", status_code=status.HTTP_200_OK,)
def health() -> dict[str, str]:
    """Endpoint para validar que el servicio está disponible"""
    return{"status": "ok"}

@router.post("/predict", response_model=PredictionResponse,
        status_code=status.HTTP_200_OK,
        summary="Clasificador del ticket de incidencia",
        description="Recibe el texto de un ticket, ejecuta la predicción y devuelve la categoría, confianza, prioridad y motivo.",
        responses={
             400:{"model": ErrorResponse, "description": "Error de validación"},
             500:{"model": ErrorResponse, "description": "Error interno del servidor"}
        })

def predict(request: TicketRequest)-> PredictionResponse:
    """Ejecuta la clasificación de un ticket usando el modelo entrenado.
    """
    try:
        logger.info("Solicitud recibida en /predict")
        result: dict[str, Any] = predict_ticket(request.text)
        append_prediction_to_csv(CSV_PATH, request.text, result)

        logger.info(
            "Predicción API | categoria=%s | confianza=%.4f | prioridad=%s",
              result["category"],
              result["confidence"],
              result["priority"],
        )
        return PredictionResponse (**result)
    except ValueError as e:
        logger.warning("Error de validación: %s", str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception:
        logger.exception("Error interno durante la predicción")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor")