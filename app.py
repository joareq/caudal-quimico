import streamlit as st

# --- Configuración de página ---
st.set_page_config(page_title="Cálculo caudal químico", layout="wide")

# --- Estilos personalizados ---
st.markdown(
    """
    <style>
    /* Mantener el estilo original del slider, solo personalizamos colores */
    div[data-baseweb="slider"] span {
        font-size: 18px !important;
        color: #00AEEF !important;  /* azul Hidrofrac para el número */
        font-weight: bold;
    }
    div[data-baseweb="slider"] div[role="slider"] {
        background-color: #00AEEF !important; /* círculo azul */
        border: 2px solid white !important;   /* borde blanco */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Logo y título ---
st.markdown(
    """
    <div style="text-align: center;">
        <img src="https://raw.githubusercontent.com/joareq/caudal-quimico/main/logo.png" width="250">
        <h1 style="margin-top: 10px;">CALCULO CAUDAL QUIMICO</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# --- Sliders principales ---
col1, col2 = st.columns(2)
with col1:
    gpt = st.slider("Seleccione GPT (galones por mil)", 0.0, 10.0, 1.5, 0.1)
with col2:
    bpm = st.slider("Seleccione BPM (barriles por minuto)", 0.5, 20.0, 5.0, 0.1)

#
