from __future__ import annotations
from pydantic import BaseModel, Field



class TicketRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Texto del ticket a clasificar",
                      examples=["my internet is down since yesterday"])

class PredictionResponse(BaseModel):
    category: str = Field(
        ...,
        description="Categoría predicha por el modelo",
        examples=["service_outage"],
                           )
    confidence: float = Field(
        ..., 
        description="Probabilidad más alta estimada por el modelo",
        examples=[0.5568],)
    confidence_status: str = Field(
        ...,
        description="Interpretación del nivel de confianza",
        examples=["revisar manualmente"],)
    priority: str = Field(
        ...,
        description="Prioridad asignada por reglas de negocio",
        examples=["Alta"],)
    reason: str = Field(
        ..., 
        description="Motivo de la prioridad asignada",
        examples=["Se asignó prioridad alta porque la categoría corresponde a una caída de servicio"],
    )

class ErrorResponse(BaseModel):
    detail: str