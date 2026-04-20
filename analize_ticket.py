# import joblib
# from pathlib import Path

# def load_model(model_path):
#     model = joblib.load(model_path)
#     return model

# def predict_ticket(model, text):
#     prediction = model.predict([text])[0]
#     confidence = model.predict_proba([text]).max()
#     return prediction, confidence


# def assign_priority(category, confidence):
#     """
#     Reglas iniciales de prioridad con explicación.
#     """

#     if category == "service_outage":
#         return "alta", "Se asignó prioridad alta porque la categoría corresponde a una caída de servicio."

#     elif category == "technical_issue":
#         if confidence >= 0.80:
#             return "alta", "Se asignó prioridad alta porque es una incidencia técnica con alta confianza."
#         return "media", "Se asignó prioridad media porque es una incidencia técnica con confianza moderada."

#     elif category == "account_access":
#         return "media", "Se asignó prioridad media porque el problema está relacionado con acceso a la cuenta."

#     elif category == "billing_payment":
#         return "media", "Se asignó prioridad media porque corresponde a un tema de facturación o pago."

#     elif category == "delivery_shipping":
#         return "baja", "Se asignó prioridad baja porque corresponde a un problema de envío o entrega."

#     return "media", "Se asignó prioridad media por tratarse de un caso general."

# def assign_confidence_status(confidence):
#     if confidence >= 0.85:
#         return "Alta confienza"
#     elif confidence >= 0.60:
#         return "confidencia media"
#     return "revisar manualmente"


# def analyze_ticket( model, text):
#     category, confidence = predict_ticket(model, text)
#     priority, reason  = assign_priority(category, confidence)
#     confidence_status = assign_confidence_status(confidence)

#     result = {
#         "ticket": text,
#         "categoria":category,
#         "confianza": round(float(confidence), 3),
#         "estado_confianza": confidence_status,
#         "prioridad": priority,
#         "motivo": reason
#     }
#     return result

# def main():
#     BASE_DIR = Path(__file__).resolve().parent.parent
#     MODEL_PATH = BASE_DIR /"models/ticket_classifier.joblib"

#     print("Cargando modelo...")
#     model = load_model(MODEL_PATH)
    
#     print("\nSistema Inteligente de Análisis y prioritización de Incidencias")
#     print("Escribe un ticket o escribe 'exit' para salir ")

#     while True:
#         text = input("Ticket: ")
#         if text.lower() == "exit":
#             print("\nSaliendo del sistema")
#             break

#         result = analyze_ticket(model, text)
#         print("\n Resultado del análisis:")
#         print("Categoría :", result["categoria"])
#         print("Confianza :", result["confianza"])
#         print("Estado de Confianza :", result["estado_confianza"])
#         print("Prioridad :", result["prioridad"] )
#         print("Motivo: ", result["motivo"])
#         print("-"*50)

# if __name__ == "__main__":
#     main()



from  __future__ import annotations

from pathlib import Path

from src.config import setup_logger
from src.predict.predictor import predict_ticket
from src.predict.utils import append_prediction_to_csv

logger = setup_logger()
CSV_PATH = Path("data/outputs/predictions.csv")

def main() -> None:
    logger.info("Inicio del sistema de análisis de incidencias")

    print("Sistema Inteligente de Ánalisis y Priorización de Incidencias")
    print("Escribe un ticket o escribe 'exit' para salir")


    while True:
        text = input("Ticket: ").strip()

        if text.lower() == "exit":
            logger.info("Cierre el sistema solicitado por el usuario")
            print("Saliendo del sistema.." )
            break

        if not text:
            logger.warning("Se recibió ticket vacio")
            print("Por favor escribe un ticket válido")
            continue

        try:
            logger.info("Analizando ticket: %s", text[:100])

            result = predict_ticket(text)
            append_prediction_to_csv(CSV_PATH, text, result)

            logger.info(
                "Predicción guardada | categoria=%s | confianza=%.4f | prioridad=%s",
                result["category"],
                result["confidence"],
                result["priority"],
            )

            print("\Resultado del análisis:")
            print(f"Categoría  :{result['category']}")
            print(f"Confianza :{result['confidence']:.3f}")
            #print(f"Estado de confianza :{result['confidence_status']}")
            print(f"Estado de Confianza : {result['confidence_status']}")
            print(f"Prioridad : {result['priority']}")
            print(f"Motivo :{result['reason']}\n")
        except Exception:
            logger.exception("Error durante el análisis de ticket")
            print("Ocurrío un error durante el análisis. Revisa logs/app.log para más detalle")

if __name__ == "__main__":
    main()


    