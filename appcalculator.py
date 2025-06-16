import streamlit as st
import pandas as pd
import plotly.graph_objects as go

@st.cache_data
def cargar_datos():
    cols = ["nombre_ocupacion", "departamento", "Ingreso_laboral_primario"]
    return pd.read_excel("Chamba.xlsx", usecols=cols)

df = cargar_datos()

st.title("Visualización de Ingreso Laboral por Ocupación y Departamento")

departamento_map = {
    1: "Chuquisaca",
    2: "La Paz",
    3: "Cochabamba",
    4: "Oruro",
    5: "Potosi",
    6: "Tarija",
    7: "Santa Cruz",
    8: "Beni",
    9: "Pando"
}

df['nombre_departamento'] = df['departamento'].map(departamento_map)

ocupacion_seleccionada = st.selectbox(
    "Selecciona una ocupación:", 
    sorted(df['nombre_ocupacion'].unique())
)

departamentos_filtrados = df[df['nombre_ocupacion'] == ocupacion_seleccionada]['nombre_departamento'].unique()
departamento_seleccionado = st.selectbox(
    "Selecciona un departamento:", 
    sorted(departamentos_filtrados)
)

df_filtrado = df[
    (df['nombre_ocupacion'] == ocupacion_seleccionada) &
    (df['nombre_departamento'] == departamento_seleccionado)
]

if df_filtrado.empty:
    st.warning("No hay datos disponibles para la selección.")
else:

    ingreso_promedio = df_filtrado['Ingreso_laboral_primario'].mean()
    ingreso_min = df_filtrado['Ingreso_laboral_primario'].min()
    ingreso_max = df_filtrado['Ingreso_laboral_primario'].max()

    # Crear gráfico 
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=ingreso_promedio,
        number={'prefix': "Bs ", 'valueformat': '.0f'},
        gauge={
            'axis': {'range': [0, ingreso_max]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, ingreso_min], 'color': "lightgray"},
                {'range': [ingreso_min, ingreso_promedio], 'color': "gray"},
                {'range': [ingreso_promedio, ingreso_max], 'color': "lightblue"},
            ],
        },
        title={'text': "Promedio de Ingreso Laboral"}
    ))

    st.plotly_chart(fig)
