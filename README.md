# Sistema Inteligente de Clasificación de Incidencias

Proyecto de Machine Learning y Backend que clasifica automáticamente tickets de soporte en categorías y asigna prioridades usando NLP.

---

##  Descripción

Este proyecto implementa un sistema de clasificación de incidencias basado en procesamiento de lenguaje natural (NLP), capaz de:

* Clasificar tickets en categorías (ej. `service_outage`, `login_issue`, etc.)
* Estimar la confianza de la predicción
* Determinar si requiere revisión manual
* Asignar una prioridad automática
* Generar un motivo explicativo
* Exponer el modelo como una API REST con FastAPI

---

##  Problema

En sistemas de soporte, los tickets llegan como texto libre, lo que dificulta:

* Clasificación rápida
* Priorización eficiente
* Automatización del flujo de atención

Este proyecto resuelve ese problema mediante un modelo de NLP y reglas de negocio.

---

##  Solución

Se desarrolló un pipeline completo que incluye:

### 1. Preprocesamiento y etiquetado

* Dataset: TWCS (Twitter Customer Support)
* Etiquetado mediante reglas (weak supervision)

### 2. Modelo de Machine Learning

* TF-IDF (vectorización de texto)
* Logistic Regression (clasificación)
* Accuracy aproximada: ~92%

### 3. Motor de reglas

* Clasificación de nivel de confianza
* Asignación de prioridad basada en categoría y confianza

### 4. Persistencia

* Registro de predicciones en CSV

### 5. Observabilidad

* Logging del sistema

### 6. API REST

* FastAPI
* Endpoint `/predict`
* Documentación automática (Swagger)

---

##  Tecnologías utilizadas

* Python 3
* scikit-learn
* pandas
* FastAPI
* Pydantic
* Uvicorn
* joblib
* logging

---

### Request

```json
POST /predict

{
  "text": "my internet is down since yesterday"
}
```

### Response

```json
{
  "category": "service_outage",
  "confidence": 0.5568,
  "confidence_status": "revisar manualmente",
  "priority": "alta",
  "reason": "Se asignó prioridad alta porque la categoría corresponde a una caída de servicio."
}
```

---

##  Cómo ejecutar el proyecto

### 1. Clonar repositorio

```bash
git clone [https://github.com/tu-usuario/incidencias_ia.git](https://github.com/danyelJoy/Clasificaci-n-de-Incidencias.git)

```

### 2. Crear entorno virtual

```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Entrenar modelo

```bash
python train_model.py
```

### 5. Ejecutar API

```bash
uvicorn src.api.main:app --reload
```

### 6. Abrir documentación

```
http://127.0.0.1:8000/docs
```

---

##  Estructura del proyecto

```bash
src/
├── api/
│   └── main.py
├── predict/
│   ├── predictor.py
│   ├── rules.py
│   ├── load_model.py
│   └── utils.py
├── labeling.py
├── predict_ticket.py
├── preprocessing.py
├── train_model.py
├── config.py

models/
data/
logs/
```

---

##  Posibles mejoras

* Endpoint batch (`/predict-batch`)
* Dashboard con Streamlit
* Deploy en la nube (Render / Railway)
* Base de datos en lugar de CSV
* Mejora del modelo (embeddings, deep learning)

---

##  Autor
#D.R.M
Proyecto desarrollado como parte de portafolio en Inteligencia Artificial y Automatización.

---

## Valor del proyecto

Este proyecto demuestra:

* Construcción de pipeline completo de ML
* Integración de modelo con backend (FastAPI)
* Buenas prácticas de ingeniería (logging, estructura modular)
* Capacidad de llevar un modelo a producción
