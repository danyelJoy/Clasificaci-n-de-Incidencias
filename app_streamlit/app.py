import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000/predict"


st.set_page_config(page_title="Clasificador de Incidencias", layout="centered")
st.title("Clasificado de incidencias")
st.markdown("Ingresa un ticket y obtén su clasificación automáticamente.")

text_input = st.text_area("Texto del ticket")

if st.button("Clasificar"):
    if not text_input.strip():
        st.warning("Por favor ingresa texto.")
    else:
        with st.spinner("Analizando..."):
            try:
                response = requests.post(API_URL, json={"text": text_input})
                if response.status_code == 200:
                    result = response.json()
                    st.success("Resultado obtenido")

                    st.subheader("Resultado")
                    st.write(f"**Categoría:**{result['category']}")
                    st.write(f"**Confianza:**{result['confidence']}")
                    st.write(f"**Estado de confianza:**{result['confidence_status']}")
                    st.write(f"**Prioridad:**{result['priority']}")
                    st.write(f"**Motivo:**{result['reason']}")
                    

                else:
                    st.error(f"Error en API: {response.text}")
            except Exception as e:
                st.error(f"No se pudo conectar con la API:{e}")
