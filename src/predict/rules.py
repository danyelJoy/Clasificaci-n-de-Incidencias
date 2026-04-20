from __future__ import annotations


def get_confidence_status(confidence: float) -> str:
    """Clasifica el nivel de confianza del modelo."""
    if confidence >= 0.80:
        return "alta"
    elif confidence >= 0.60:
        return "media"
    else:
        return "revisar manualmente"
    
def assign_priority(category: str, confidence: float) ->tuple[str, str]:
    """
    Asigna prioridad y motivo con base en la categoria y confianza."""
    if category == "service_outage":
        return(
            "alta",
            "Se asignó prioridad alta porque la categoría corresponde a una caída de servicio"
        )
    if category == "login_issue":
        return(
            "media",
            "Se asignó prioridad media porque el problema afecta el acceso al usuario.."
        )
    if category == "payment_problem":
        return(
            "alta",
            "Se asignó prioridad alta porque el incidente está relacionado con pagos."
        )
    if confidence < 0.60:
        return(
            "media",
            "La confianza del modelo es baja, por lo que se recomienda revisión manual."
        )
    return(
        "baja",
        "Se asignó prioridad bajá porque se detectó una categoría crítica."
    )