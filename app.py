import streamlit as st
from google.cloud import vision
import io
from PIL import Image
import base64
import os
import tempfile

# Lee las credenciales desde el secreto en formato Base64
def get_credentials_from_secrets():
    import streamlit.secrets as secrets
    base64_credentials = secrets["gcloud"]["credentials"]
    return base64.b64decode(base64_credentials)

# Guarda las credenciales en un archivo temporal
def save_credentials_to_temp_file():
    credentials_data = get_credentials_from_secrets()
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
    with open(temp_file.name, 'wb') as f:
        f.write(credentials_data)
    return temp_file.name

# Configura la variable de entorno para Google Cloud
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = save_credentials_to_temp_file()

def detect_text_google(image):
    client = vision.ImageAnnotatorClient()

    image_byte_array = io.BytesIO()
    image.save(image_byte_array, format='PNG')
    content = image_byte_array.getvalue()

    image = vision.Image(content=content)

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
