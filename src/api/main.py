from __future__  import annotations
from fastapi import FastAPI
from src.api.routes.predict import router as predict_router

app = FastAPI(
    title="Sistema de Clasificación de Incidencias",
    version="1.2.0",
    description=("API para clasificar tickets de incidencias con NLP, "
    "asignar prioridades y registrar resultados."
    ),
)

app.include_router(predict_router)

@app.get("/", tags=["Root"], summary="Mensaje de bienvenida")
def root() -> dict[str, str]:
    return {"message": "API de clasificación de incidencias activa"}
