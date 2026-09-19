# Importamos las librerías necesarias

import streamlit as st
import pandas as pd
from transformers import pipeline
from datetime import datetime
import os

print("Archivo usado por CLIENTE:")
print(os.path.abspath("comentarios.csv"))

# Logo en el panel izquierdo
st.sidebar.image("logo_kraft.png", use_container_width=True)

# Encabezado
st.image("Tu_opinion_fondo.png", use_container_width=True)

# Barra azul verdoso
st.markdown(
    """
    <div style="
        height: 12px;
        background-color: #16343D;
        width: 100%;
        margin-top: 5px;
        margin-bottom: 30px;
    "></div>
    """, unsafe_allow_html=True
)

# Cargamos el modelo
@st.cache_resource
def cargar_modelo():
    return pipeline(
        "text-classification",
        model="clapAI/mmBERT-small-multilingual-sentiment",
        device=0
    )

modelo_sentimientos = cargar_modelo()

# Variable para guardar los comentarios emitidos desde interfaz de cliente
def guardar_comentario(
    comentario,
    categoria,
    sentimiento,
    confianza
):

    nuevo_comentario = pd.DataFrame({
        "fecha": [
            datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        ],
        "comentario": [
            comentario
        ],
        "categoria": [
            categoria
        ],
        "sentimiento": [
            sentimiento
        ],
        "confianza": [
            confianza
        ]
    })


    # Si el archivo ya existe, agregar el comentario
    if os.path.exists("comentarios.csv"):

        nuevo_comentario.to_csv("comentarios.csv", mode="a", header=False, index=False)

    # Si no existe, crear el archivo
    else:

        nuevo_comentario.to_csv("comentarios.csv", index=False)


# INTERFAZ --------------------------------------------------------------------------------------

st.markdown(
    """
    <h1 style="
        font-size: 38px;
        font-weight: 700;
        white-space: nowrap;
        margin-bottom: 10px;
    ">
        📱 Qué te parecieron nuestros productos?
    </h1>
    """,
    unsafe_allow_html=True
)

st.write("Tu opinión siempre nos ayuda a mejorar! 🤓")



# Traducimos categorías de Amazon --------------------------------------------------

categorias = {
    "Automotriz": "automotive",
    "Belleza": "beauty",
    "Calzado": "shoes",
    "Cámaras": "camera",
    "Cocina": "kitchen",
    "Computadoras": "pc",
    "Cuidado personal": "personal_care_appliances",
    "Deportes": "sports",
    "Dispositivos inalámbricos": "wireless",
    "Electrónica": "electronics",
    "Equipaje": "luggage",
    "Farmacia": "drugstore",
    "Hogar": "home",
    "Instrumentos musicales": "musical_instruments",
    "Jardín": "lawn_and_garden",
    "Joyería": "jewelry",
    "Juguetes": "toy",
    "Libros": "book",
    "Libros digitales": "digital_ebook_purchase",
    "Mejoras para el hogar": "home_improvement",
    "Muebles": "furniture",
    "Otros": "other",
    "Productos de oficina": "office_product",
    "Productos para bebés": "baby_product",
    "Productos para mascotas": "pet_products",
    "Relojes": "watch",
    "Ropa": "apparel",
    "Suministros industriales": "industrial_supplies",
    "Supermercado": "grocery",
    "Videojuegos": "video_games"
}


# Seleccionamos la categoría --------------------------------------------------

categoria_seleccionada = st.selectbox("Escoge la categoría del producto que compraste por favor:", list(categorias.keys()))

# Obtener el nombre original utilizado por Amazon
categoria = categorias[categoria_seleccionada]

# Limpiar comentario después de enviarlo
if st.session_state.get("comentario_enviado", False):

    st.session_state["comentario"] = ""

# Escribimos el comentario --------------------------------------------------

comentario = st.text_area("Escribe aquí el comentario sobre el producto:", key="comentario")

# Analizamos y guardamos --------------------------------------------------

if st.button("Enviar comentario"):

    if comentario:

        # Analizar comentario con mmBERT
        resultado = modelo_sentimientos(comentario)[0]

        sentimiento = resultado["label"]
        confianza = resultado["score"]


        # Guardar resultado
        guardar_comentario(
            comentario,
            categoria,
            sentimiento,
            confianza
        )

        # Indicar que el comentario fue enviado
        st.session_state["comentario_enviado"] = True

        # Recargar la interfaz
        st.rerun()

if st.session_state.get("comentario_enviado", False):

    st.success("¡Gracias por compartir tu opinión!")

    st.session_state["comentario_enviado"] = False


df_comentarios = pd.read_csv("comentarios.csv")

print(df_comentarios.shape)
print(df_comentarios.tail())


# Barra azul verdoso
st.markdown("""
    <div style="
        height: 12px;
        background-color: #16343D;
        width: 100%;
        margin-top: 5px;
        margin-bottom: 30px;
    "></div>
    """, unsafe_allow_html=True
)


