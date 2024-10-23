from requests.api import request
import streamlit as st
import requests
import json
import re
import os

dify_secret = os.environ['DIFY_APP_KEY']


def validate_url(url):
  # Expresión regular para validar la URL
  pattern = re.compile(r'^https://')

  # Verificar si la URL coincide con el patrón
  if pattern.match(url):
    return True
  else:
    return False


# Título de la aplicación
st.title("TechBrief - CRDZ")

st.markdown("""
Este es un asistente que genera el resumen de noticias de TechCrunch.

En la respuesta obtendrás:

- Un resumen de toda la noticia.
- Una lista de ideas claves.
- Una lista de Insights.

Asegúrate de enviar una URL válida.
""")

# Campo de texto para ingresar la URL
url_input = st.text_input("Enter URL")

# URL base de la API
base_url = "https://api.dify.ai/v1"

# Path de la API
path = "/workflows/run"

# full url
full_url = base_url + path

# Headers
headers = {
    "Authorization": f"Bearer {dify_secret}",
    "Content-Type": "application/json"
}

# Data: inputs[], response_mode, user
data = {
    "inputs": {
        "url": url_input
    },
    "response_mode": "blocking",
    "user": "LiveSession-10"
}

# Botón de enviar
if st.button("Send"):
  # Verificar si se proporcionó una URL
  if url_input:
    # Validar la URL
    if validate_url(url_input):
      try:
        # Enviar solicitud HTTP POST a la URL
        response = requests.post(full_url,
                                 headers=headers,
                                 data=json.dumps(data))

        json = response.json()
        resumen = json['data']['outputs']['resumen']
        
        # Mostrar la respuesta en markdown
        st.markdown(resumen)
      
      except Exception as e:
        # Mostrar mensaje de error si ocurre alguna excepción
        st.error(f"An error occurred: {str(e)}")
    else:
      # Mostrar mensaje de error si la URL no es válida
      st.error("Invalid URL. Please enter a URL that starts with 'https://'")
  else:
    # Mostrar mensaje de error si no se proporcionó una URL
    st.error("Please enter a URL")
