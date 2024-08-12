import streamlit as st
from google.cloud import vision
import io
from PIL import Image

def detect_text_google(image):
    # Crea un cliente de la API de Google Cloud Vision
    client = vision.ImageAnnotatorClient()

    # Convierte la imagen a bytes usando BytesIO
    image_byte_array = io.BytesIO()
    image.save(image_byte_array, format='PNG')
    content = image_byte_array.getvalue()

    # Crea un objeto Image para enviar a la API
    image = vision.Image(content=content)

    # Realiza la detección de texto
    response = client.text_detection(image=image)
    texts = response.text_annotations
    return texts[0].description if texts else "No text found"

st.markdown("<h1 style='text-align: center;'>ESCÁNER DE DOCUMENTOS</h1>", unsafe_allow_html=True)

# MODO DE SUBIR LA FOTO
col1, col2, col3 = st.columns([2, 3, 4])
col1.subheader("1. MODO")
with col2:
    modo = st.selectbox("", ("SUBE TU IMAGEN", "USAR CAMARA"))

imagen = None
picture = None
with col3:
    if modo == "SUBE TU IMAGEN":
        imagen = st.file_uploader("", type=["png", "jpg", "jpeg"])
    elif modo == "USAR CAMARA":
        picture = st.camera_input("Toma una foto")

image = None
if imagen is not None:
    image = Image.open(imagen)
elif picture is not None:
    image = Image.open(picture)

if image is not None:
    if st.button("ESCANEAR"):
        st.image(image, caption="", use_column_width=True)
        text = detect_text_google(image)
        st.subheader("2. TEXTO :")
        st.code(text)
else:
    st.warning("Por favor, sube una imagen o toma una foto para continuar.")
