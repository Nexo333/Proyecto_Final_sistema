import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

print("Archivo usado por ANALISTA:")
print(os.path.abspath("comentarios.csv"))

# logo en panel izquierdo

st.sidebar.image("logo_kraft.png", use_container_width=True)

# SECCIÓN DEL ENCABEZADO ----------------------------------------------------------------------------------------------------

# Logo
st.image("analisis_fondo.png", use_container_width=True)

# Barra azul
st.markdown(
    """
    <div style="
        height: 12px;
        background-color: #06477F;
        width: 100%;
        margin-top: 5px;
        margin-bottom: 30px;
    "></div>
    """, unsafe_allow_html=True
)

# Título en la interfaz
st.markdown(
    """
    <h1 style="
        font-size: 42px;
        font-weight: 700;
        white-space: nowrap;
        margin-bottom: 10px;
    ">
        📊 Panel de Análisis de Opiniones
    </h1>
    """,
    unsafe_allow_html=True
)



# SECCION PORCENTAJE DE COMENTARIOS ----------------------------------------------------------------------------------

# Subtítulo y presentación resumen de las opiniones
st.write("Resumen general de las opiniones de los clientes")

# Leemos la base de datos de los comentarios ingresados desde la parte del cliente
df_comentarios = pd.read_csv("comentarios.csv")


print(df_comentarios["categoria"].unique())
print(df_comentarios["categoria"].isna().sum())

# Transformamos a formato de fecha y hora la columna fecha (que no sea solo string),  así pandas lo puede manejar
df_comentarios["fecha"] = pd.to_datetime(
    df_comentarios["fecha"],
    format="mixed",
    dayfirst=True
)

# Cantidad total de los comentarios
total = len(df_comentarios)

# Cantidad por sentimiento
positivos = len(df_comentarios[df_comentarios["sentimiento"] == "positive"])
neutrales = len(df_comentarios[df_comentarios["sentimiento"] == "neutral"])
negativos = len(df_comentarios[df_comentarios["sentimiento"] == "negative"])

# Calculamos en porcentajes
porcentaje_positivos = positivos / total * 100
porcentaje_neutrales = neutrales / total * 100
porcentaje_negativos = negativos / total * 100

# Dividimos la interfaz de streamlit en 4 columnas para colocar cada métrica
col1, col2, col3, col4 = st.columns(4)

col1.metric("💬 Comentarios", total)
col2.metric("😄 Positivos", f"{porcentaje_positivos:.1f}%")
col3.metric("😑 Neutrales", f"{porcentaje_neutrales:.1f}%")
col4.metric("😡 Negativos", f"{porcentaje_negativos:.1f}%")

st.divider()



# SECCION GRÁFICO DE DISTRIBUCIÓN DE SENTIMIENTOS -----------------------------------------------------------------------

# Título
st.subheader("📈 Distribución de sentimientos")

# Subtitulo
st.write("Gráfico de porcentaje de distribución de sentimientos")

# Variables para graficos
valores = [positivos, neutrales, negativos]
etiquetas = ["😄 Positivos", "😑 Neutrales", "😡 Negativos"]
colores = ["#2ECC71", "#F4D03F", "#E74C3C"]

fig, ax = plt.subplots(figsize=(7, 4))

ax.pie(
    valores,
    colors=colores,
    autopct=lambda p: f"{p:.1f}%" if p > 0 else "",
    startangle=90,
    textprops={"fontsize": 11}
)

ax.legend(
    etiquetas,
    title="Sentimiento",
    loc="center left",
    bbox_to_anchor=(1, 0.5)
)

ax.axis("equal")

st.pyplot(fig)

# Análisis --------------

# Resumen de la gráfica
st.markdown(f"""
📝 De un total de: **{total} comentarios:**

Hay **{positivos} comentarios positivos**, que representan el **{porcentaje_positivos:.1f}%**.

Hay **{neutrales} comentarios neutrales**, que representan el **{porcentaje_neutrales:.1f}%**.

Hay **{negativos} comentarios negativos**, que representan el **{porcentaje_negativos:.1f}%**.
""")

st.divider()



# SECCION CATEGORÍAS MÁS COMENTADAS -----------------------------------------------------------------------

# Titulo
st.subheader("📦 Categorías más comentadas")

# Subtitulo
st.write("Categorías con mayor participación de los clientes")

# Diccionario para mostrar las categorías en español
nombres_categorias = {
    "apparel": "Ropa",
    "automotive": "Automotriz",
    "baby_product": "Productos para bebés",
    "beauty": "Belleza",
    "book": "Libros",
    "camera": "Cámaras",
    "digital_ebook_purchase": "Libros digitales",
    "drugstore": "Farmacia",
    "electronics": "Electrónica",
    "furniture": "Muebles",
    "grocery": "Supermercado",
    "home": "Hogar",
    "home_improvement": "Mejoras para el hogar",
    "industrial_supplies": "Suministros industriales",
    "jewelry": "Joyería",
    "kitchen": "Cocina",
    "lawn_and_garden": "Jardín",
    "luggage": "Equipaje",
    "musical_instruments": "Instrumentos musicales",
    "office_product": "Productos de oficina",
    "other": "Otros",
    "pc": "Computadoras",
    "personal_care_appliances": "Cuidado personal",
    "pet_products": "Productos para mascotas",
    "shoes": "Calzado",
    "sports": "Deportes",
    "toy": "Juguetes",
    "video_games": "Videojuegos",
    "watch": "Relojes",
    "wireless": "Dispositivos inalámbricos"
}

# Contar comentarios por categoría
categorias_comentadas = (
    df_comentarios["categoria"]
    .value_counts()
    .head(10)
)

# Traducir los nombres al español
categorias_comentadas.index = categorias_comentadas.index.map(
    nombres_categorias
)

# Crear gráfico
fig, ax = plt.subplots(figsize=(8, 4))

barras = ax.barh(
    categorias_comentadas.index,
    categorias_comentadas.values,
    height=0.35,       # Barras más delgadas
    alpha=0.45         # Barras más claras / transparentes
)

# Mostrar cantidad al final de cada barra
for barra in barras:

    valor = barra.get_width()

    ax.text(
        valor + 0.08,
        barra.get_y() + barra.get_height() / 2,
        f"{int(valor)}",
        va="center",
        fontsize=10
    )

# Categoría con más comentarios arriba
ax.invert_yaxis()

# Quitar títulos de los ejes
ax.set_xlabel("")
ax.set_ylabel("")

# Quitar bordes del gráfico
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["bottom"].set_visible(True)
ax.spines["left"].set_visible(False)

# Quitar pequeñas marcas del eje Y
ax.tick_params(
    axis="y",
    length=0,
    labelsize=11
)

# Dejar espacio para los números
ax.set_xlim(0, categorias_comentadas.max() * 1.15)

plt.tight_layout()

st.pyplot(fig)

# # Análisis --------------
total_comentarios = len(df_comentarios)

# Total de categorías diferentes que recibieron comentarios
total_categorias = df_comentarios["categoria"].nunique()

# Categoría con más comentarios
categoria_mas_comentada = categorias_comentadas.index[0]
cantidad_mas_comentada = categorias_comentadas.iloc[0]

# Porcentaje de la categoría más comentada
porcentaje_mas_comentada = (
    cantidad_mas_comentada / total_comentarios
) * 100

# Tres categorías más comentadas
top_3 = categorias_comentadas.head(3)

cantidad_top_3 = top_3.sum()

porcentaje_top_3 = (
    cantidad_top_3 / total_comentarios
) * 100

# Resumen
st.markdown(f"""
📝 **Nivel de participación:**

Categoría con más comentarios: **{categoria_mas_comentada}** - **{cantidad_mas_comentada} comentarios** - representan el **{porcentaje_mas_comentada:.1f}%** del total.

Se han recibido opiniones en **{total_categorias} categorías diferentes**.

Las **3 categorías más comentadas** acumulan **{cantidad_top_3} comentarios**, equivalentes al **{porcentaje_top_3:.1f}%** del total.
""")

st.divider()



# SECCION CATEGORÍAS CON MÁS COMENTARIOS NEGATIVOS ------------------------------------------------------------------------

# Título
st.subheader("🚨 Categorías con más comentarios negativos")

# Subtitulo
st.write("Se indica el número de comentarios por categoría")

# Filtrar solamente comentarios negativos
df_negativos = df_comentarios[
    df_comentarios["sentimiento"] == "negative"
].copy()


# Contar comentarios negativos por categoría
categorias_negativas = (
    df_negativos["categoria"]
    .value_counts()
    .head(10)
)


# Traducir nombres de categorías al español
categorias_negativas.index = categorias_negativas.index.map(
    nombres_categorias
)


# Verificar que existan comentarios negativos
if len(categorias_negativas) > 0:

    # Crear gráfico
    fig, ax = plt.subplots(figsize=(8, 4))

    barras = ax.barh(
        categorias_negativas.index,
        categorias_negativas.values,
        height=0.35,
        alpha=0.45
    )

    # Mostrar cantidad al final de cada barra
    for barra in barras:

        valor = barra.get_width()

        ax.text(
            valor + 0.08,
            barra.get_y() + barra.get_height() / 2,
            f"{int(valor)}",
            va="center",
            fontsize=10
        )

    # Categoría con más negativos arriba
    ax.invert_yaxis()

    # Quitar títulos de los ejes
    ax.set_xlabel("")
    ax.set_ylabel("")

    # Quitar bordes
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_visible(True)
    ax.spines["left"].set_visible(False)

    # Quitar marcas del eje Y
    ax.tick_params(
        axis="y",
        length=0,
        labelsize=11
    )

    # Espacio para mostrar los valores
    ax.set_xlim(
        0,
        categorias_negativas.max() * 1.15
    )

    plt.tight_layout()

    st.pyplot(fig)

else:

    st.info("No existen comentarios negativos registrados.")

# Análisis --------------

# Filtrar solamente comentarios negativos
comentarios_negativos = df_comentarios[
    df_comentarios["sentimiento"] == "negative"
]

# Total de comentarios negativos
total_negativos = len(comentarios_negativos)

# Número de categorías que tienen comentarios negativos
categorias_con_negativos = comentarios_negativos["categoria"].nunique()

# Contar comentarios negativos por categoría
negativos_por_categoria = (
    comentarios_negativos["categoria"]
    .value_counts()
)

# Mayor cantidad de comentarios negativos en una categoría
mayor_cantidad_negativos = negativos_por_categoria.max()

# Categorías que tienen esa cantidad máxima
categorias_mas_negativas = negativos_por_categoria[
    negativos_por_categoria == mayor_cantidad_negativos
].index

# Traducir los nombres al español
categorias_mas_negativas = [
    nombres_categorias.get(categoria, categoria)
    for categoria in categorias_mas_negativas
]

# Resumen
st.markdown(f"""
📝 **Análisis de comentarios negativos:**

Se han registrado **{total_negativos} comentarios negativos** distribuidos en **{categorias_con_negativos} categorías diferentes**.
""")

if len(categorias_mas_negativas) > 1:

    st.markdown(
        f"""
Actualmente **no existe una sola categoría que concentre la mayor cantidad de comentarios negativos**, 
ya que **{len(categorias_mas_negativas)} categorías** registran la misma cantidad máxima de 
**{mayor_cantidad_negativos} comentario(s) negativo(s)**.
        """
    )

else:

    st.markdown(
        f"""
La categoría con mayor cantidad de comentarios negativos es 
**{categorias_mas_negativas[0]}**, con **{mayor_cantidad_negativos} comentario(s) negativo(s)**.
        """
    )

st.divider()


# SECCION PORCENTAJE DE COMENTARIOS NEGATIVOS POR CATEGORÍA ------------------------------------

st.subheader("📉 Porcentaje de comentarios negativos por categoría")

st.write(
    "Proporción de comentarios negativos respecto al total de opiniones de cada categoría."
)


# Cantidad total de comentarios por categoría
total_por_categoria = (
    df_comentarios["categoria"]
    .value_counts()
)


# Cantidad de comentarios negativos por categoría
negativos_por_categoria = (
    df_comentarios[
        df_comentarios["sentimiento"] == "negative"
    ]["categoria"]
    .value_counts()
)


# Calcular porcentaje de negativos
porcentaje_negativos = (
    negativos_por_categoria
    .div(total_por_categoria)
    .fillna(0)
    * 100
)


# Ordenar de mayor a menor
porcentaje_negativos = (
    porcentaje_negativos
    .sort_values(ascending=False)
    .head(10)
)


# Traducir nombres de categorías al español
porcentaje_negativos.index = porcentaje_negativos.index.map(
    nombres_categorias
)


# Verificar que existan datos
if len(porcentaje_negativos) > 0:

    # Crear gráfico
    fig, ax = plt.subplots(figsize=(8, 4))

    barras = ax.barh(
        porcentaje_negativos.index,
        porcentaje_negativos.values,
        height=0.35,
        alpha=0.45
    )


    # Mostrar porcentaje al final de cada barra
    for barra in barras:

        valor = barra.get_width()

        ax.text(
            valor + 1,
            barra.get_y() + barra.get_height() / 2,
            f"{valor:.1f}%",
            va="center",
            fontsize=10
        )


    # Mayor porcentaje arriba
    ax.invert_yaxis()


    # Quitar títulos de ejes
    ax.set_xlabel("")
    ax.set_ylabel("")


    # Quitar números del eje X
    ax.set_xticks([])


    # Quitar bordes
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["left"].set_visible(False)


    # Quitar marcas del eje Y
    ax.tick_params(
        axis="y",
        length=0,
        labelsize=11
    )


    # El porcentaje nunca puede superar 100
    ax.set_xlim(0, 110)

    plt.tight_layout()

    st.pyplot(fig)


    # Análisis --------------

    mayor_porcentaje = porcentaje_negativos.max()

    categorias_mayor_porcentaje = porcentaje_negativos[
        porcentaje_negativos == mayor_porcentaje
    ].index.tolist()


    st.markdown("📝 **Nivel de comentarios negativos:**")


    # Varias categorías empatadas
    if len(categorias_mayor_porcentaje) > 1:

        categorias_texto = ", ".join(categorias_mayor_porcentaje)

        st.markdown(
            f"""
Las categorías con mayor proporción de comentarios negativos son **{categorias_texto}**, 
con un **{mayor_porcentaje:.1f}% de comentarios negativos** en cada una.
            """
        )


    # Una sola categoría
    else:

        st.markdown(
            f"""
La categoría con mayor proporción de comentarios negativos es 
**{categorias_mayor_porcentaje[0]}**, con un **{mayor_porcentaje:.1f}% de comentarios negativos**.
            """
        )


else:

    st.info("No existen datos suficientes para realizar el análisis.")

st.divider()


# SECCION EVOLUCIÓN DE OPINIONES EN EL TIEMPO ------------------------------------

st.subheader("📈 Opiniones en el tiempo")

st.write("Evolución de los comentarios positivos, neutrales y negativos a lo largo del tiempo."
)

df_comentarios["dia"] = df_comentarios["fecha"].dt.date

evolucion = (
    df_comentarios
    .groupby(["dia", "sentimiento"])
    .size()
    .unstack(fill_value=0)
)

evolucion = evolucion.rename(columns={
    "positive": "Positivos",
    "neutral": "Neutrales",
    "negative": "Negativos"
})

st.line_chart(evolucion)

st.write("Tendencia de las opiniones recibidas, destacando los días de mayor actividad y la evolución de los comentarios positivos, neutrales y negativos a lo largo del tiempo")

st.divider()

# SECCION FILTRO DE LOS COMENTARIOS  ------------------------------------

st.subheader("🔎 Filtros")


# Crear copia del DataFrame
df_filtrado = df_comentarios.copy()


# Filtro por sentimiento
sentimiento_seleccionado = st.selectbox(
    "Sentimiento",
    ["Todos", "Positivos", "Neutrales", "Negativos"]
)


# Filtro por categoría
categoria_seleccionada = st.selectbox(
    "Categoría",
    ["Todas"] + list(nombres_categorias.values())
)


# Aplicar filtro de sentimiento
if sentimiento_seleccionado == "Positivos":

    df_filtrado = df_filtrado[
        df_filtrado["sentimiento"] == "positive"
    ]

elif sentimiento_seleccionado == "Neutrales":

    df_filtrado = df_filtrado[
        df_filtrado["sentimiento"] == "neutral"
    ]

elif sentimiento_seleccionado == "Negativos":

    df_filtrado = df_filtrado[
        df_filtrado["sentimiento"] == "negative"
    ]


# Aplicar filtro de categoría
if categoria_seleccionada != "Todas":

    categoria_original = next(
        codigo
        for codigo, nombre in nombres_categorias.items()
        if nombre == categoria_seleccionada
    )

    df_filtrado = df_filtrado[
        df_filtrado["categoria"] == categoria_original
    ]


# Obtener fecha mínima y máxima
fecha_minima = df_comentarios["fecha"].min().date()
fecha_maxima = df_comentarios["fecha"].max().date()


# Filtro por fecha
rango_fechas = st.date_input(
    "Rango de fechas",
    value=(fecha_minima, fecha_maxima),
    min_value=fecha_minima,
    max_value=fecha_maxima
)


# Aplicar filtro de fechas
if len(rango_fechas) == 2:

    fecha_inicio = rango_fechas[0]
    fecha_fin = rango_fechas[1]

    df_filtrado = df_filtrado[
        (df_filtrado["fecha"].dt.date >= fecha_inicio) &
        (df_filtrado["fecha"].dt.date <= fecha_fin)
    ]


# Mostrar cantidad encontrada
st.write(
    "Comentarios encontrados:",
    len(df_filtrado)
)

# SECCION COMENTARIOS RECIENTES ------------------------------------

st.subheader("💬 Comentarios recientes")

comentarios_recientes = df_filtrado.sort_values(
    by="fecha",
    ascending=False
).head(10)

comentarios_recientes = comentarios_recientes[
    ["fecha", "comentario", "sentimiento", "confianza"]
].copy()

comentarios_recientes["sentimiento"] = comentarios_recientes["sentimiento"].replace({
    "positive": "😊 Positivo",
    "neutral": "😐 Neutral",
    "negative": "😡 Negativo"
})

comentarios_recientes["confianza"] = (
    comentarios_recientes["confianza"] * 100
).round(1)

st.dataframe(
    comentarios_recientes,
    hide_index=True,
    width="stretch",
    column_config={
        "fecha": "Fecha",
        "comentario": "Comentario",
        "sentimiento": "Sentimiento",
        "confianza": st.column_config.NumberColumn(
            "Confianza",
            format="%.1f%%"
        )
    }
)

st.divider()

# SECCION COMENTARIOS NEGATIVOS RECIENTES ------------------------------------

st.subheader("🚨 Comentarios negativos recientes")


# Obtener todos los comentarios negativos
comentarios_negativos = df_comentarios[
    df_comentarios["sentimiento"] == "negative"
].copy()


# Cantidad total de comentarios negativos
total_negativos = len(comentarios_negativos)


# Mostrar indicador
st.metric(
    "Comentarios que requieren atención",
    total_negativos
)


# Ordenar TODOS los comentarios del más reciente al más antiguo
comentarios_negativos = comentarios_negativos.sort_values(
    by="fecha",
    ascending=False
)


# Convertir confianza a porcentaje
comentarios_negativos["confianza"] = (
    comentarios_negativos["confianza"] * 100
).round(1)


# Seleccionar columnas
comentarios_negativos = comentarios_negativos[
    ["fecha", "comentario", "confianza"]
]


# --------------------------------------------------
# MOSTRAR LOS 10 MÁS RECIENTES
# --------------------------------------------------

st.write("Mostrando los 10 comentarios negativos más recientes")

comentarios_recientes = comentarios_negativos.head(10)


st.dataframe(
    comentarios_recientes,
    hide_index=True,
    width="stretch",
    column_config={
        "fecha": "Fecha",
        "comentario": "Comentario",
        "confianza": st.column_config.NumberColumn(
            "Confianza",
            format="%.1f%%"
        )
    }
)


# --------------------------------------------------
# MOSTRAR TODOS LOS COMENTARIOS NEGATIVOS
# --------------------------------------------------

if st.button("🔎 Ver todos los comentarios negativos"):

    st.write(
        f"Mostrando los **{total_negativos} comentarios negativos** registrados:"
    )

    st.dataframe(
        comentarios_negativos,
        hide_index=True,
        width="stretch",
        column_config={
            "fecha": "Fecha",
            "comentario": "Comentario",
            "confianza": st.column_config.NumberColumn(
                "Confianza",
                format="%.1f%%"
            )
        }
    )

st.divider()




# SECCION CONFIANZA DE LAS PREDICCIONES ------------------------------------

st.subheader("🎯 Confianza de las predicciones")


# Calcular confianza promedio
confianza_promedio = df_comentarios["confianza"].mean() * 100

st.metric(
    "Confianza promedio",
    f"{confianza_promedio:.1f}%"
)


# Seleccionar predicciones con menos del 70% de confianza
baja_confianza = df_comentarios[
    df_comentarios["confianza"] < 0.70
].copy()


# Total de predicciones
total_predicciones = len(df_comentarios)


# Cantidad de predicciones con baja confianza
total_baja_confianza = len(baja_confianza)


# Calcular porcentaje de predicciones con baja confianza
porcentaje_baja_confianza = (
    total_baja_confianza / total_predicciones
) * 100


# Mostrar información de baja confianza
st.markdown(
    f"""
🔎 **Predicciones con baja confianza:** {total_baja_confianza} de {total_predicciones} 
(**{porcentaje_baja_confianza:.1f}%**)
"""
)


st.caption(
    "Estas predicciones pueden requerir revisión debido a que el modelo "
    "presenta una confianza inferior al 70%."
)


# Traducir los sentimientos al español
baja_confianza["sentimiento"] = baja_confianza["sentimiento"].replace({
    "positive": "😊 Positivo",
    "neutral": "😐 Neutral",
    "negative": "😡 Negativo"
})


# Convertir confianza a porcentaje
baja_confianza["confianza"] = (
    baja_confianza["confianza"] * 100
).round(1)


# Seleccionar columnas que se mostrarán
baja_confianza = baja_confianza[
    ["comentario", "sentimiento", "confianza"]
]


# Mostrar tabla
st.dataframe(
    baja_confianza,
    hide_index=True,
    width="stretch",
    column_config={
        "comentario": "Comentario",
        "sentimiento": "Sentimiento",
        "confianza": st.column_config.NumberColumn(
            "Confianza",
            format="%.1f%%"
        )
    }
)

st.divider()

