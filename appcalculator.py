import streamlit as st
import pandas as pd
import plotly.graph_objects as go

@st.cache_data
def cargar_datos():
    cols = ["nombre_ocupacion", "departamento", "Ingreso_laboral_primario"]
    return pd.read_excel("Chamba.xlsx", usecols=cols)

df = cargar_datos()

st.markdown(
    "<h1 style='text-align: center;'>Calculadora de promedios de salarios en Bolivia</h1>",
    unsafe_allow_html=True
)

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

departamentos_filtrados = list(sorted(df[df['nombre_ocupacion'] == ocupacion_seleccionada]['nombre_departamento'].unique()))
departamentos_filtrados.insert(0, "Bolivia")  # Agregamos la opción Bolivia al inicio

departamento_seleccionado = st.selectbox(
    "Selecciona un departamento:", 
    departamentos_filtrados
)

if departamento_seleccionado == "Bolivia":
    df_filtrado = df[df['nombre_ocupacion'] == ocupacion_seleccionada]
else:
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

fig = go.Figure(go.Indicator(
    mode="gauge+number",
    value=ingreso_promedio,
    number={
        'prefix': "Bs ",
        'valueformat': ',.0f',
        'font': {'size': 30, 'color': "#1F2937", 'family': "Roboto"}
    },
    gauge={
        'axis': {
            'range': [0, ingreso_max],
            'tickcolor': "#6B7280",
            'tickwidth': 1
        },
        'bar': {'color': "#0f172a", 'thickness': 0.3},
        'bgcolor': "white",
        'borderwidth': 0,
        'steps': [
            {'range': [0, ingreso_min], 'color': "#E5E7EB"},
            {'range': [ingreso_min, ingreso_promedio], 'color': "#9CA3AF"},
            {'range': [ingreso_promedio, ingreso_max], 'color': "#475569"},
        ],
        'threshold': {
            'line': {'color': "#DC2626", 'width': 4},
            'thickness': 0.75,
            'value': ingreso_promedio
        }
    },
    title={
        'text': "<b style='color:#1F2937;'>Promedio de Ingreso Laboral</b>",
        'font': {'size': 22}
    }
))

fig.update_layout(
    paper_bgcolor="white",
    margin=dict(t=60, b=20, l=30, r=30)
)

st.plotly_chart(fig)

st.markdown(
    "<hr><p style='text-align: center; font-size: 14px;'>Nota. Powered by Statly Go con datos del INE y encuestas propias</p>",
    unsafe_allow_html=True
)
