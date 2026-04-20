from  __future__ import annotations
    
from pathlib import Path

from fastapi import FastAPI,  HTTPException
from pydantic import BaseModel, Field

from src.config import setup_logger
from src.predict.predictor import predict_ticket
from src.predict.utils import append_prediction_to_csv

app = FastAPI(
    title="Sistema de Clasificación de Incidencias",
    version="1.0.0",
    description="API para clasificar tickets de incidencias con NPL"
)

logger = setup_logger()
CSV_PATH = Path("data/outputs/predictions.csv")

class TicketRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Texto del ticket a clasificar",
                      example="my internet is down since yesterday")

class PredictionResponse(BaseModel):
    category: str = Field(..., example="service_outage")
    confidence: float = Field(..., example=0.5568)
    confidence_status: str = Field(...,examples="revisar manualmente")
    priority: str = Field(...,example="Alta")
    reason: str = Field(
        ..., example="Se asignó prioridad alta porque la categoría corresponde a una caída de servicio"
    )

@app.get("/", summary="Mensaje de bienvenida")
def root() -> dict:
    """
    Endpoint base para verificar que la API está activa
    """
    return {"message":"API de clasificación de incidencias activa"}

@app.get("/health", summary="Estado de salud del servicio")
def health() -> dict:
    """Endpoint para validar que el servicio está disponible"""
    return{"status": "ok"}

@app.post("/predict", response_model=PredictionResponse,
          summary="Clasificar ticket de incidencia",
          descripcion="Recibe el texto de un ticket, ejecuta la predicción y devuelve la categoría, confianza, prioridad y motivo.")

def predict(request: TicketRequest)-> PredictionResponse:
    """Ejecuta la clasificación de un ticket usando el modelo entrenado.
    """
    try:
        logger.info("Solicitud recibida en /predict")
        result = predict_ticket(request.text)
        append_prediction_to_csv(CSV_PATH, request.text, result)

        logger.info(
            "Predicción API | categoría=%s | confianza=%.4f | prioridad=%s",
              result["category"],
              result["confidence"],
              result["priority"],
        )
        return PredictionResponse (**result)
    except ValueError as e:
        logger.warning("Error de validación: %s", str(e))
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        logger.exception("Error interno durante la predicción")
        raise HTTPException(status_code=500, detail="Error interno del servidor")