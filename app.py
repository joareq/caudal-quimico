import streamlit as st

# --- Configuración de página ---
st.set_page_config(page_title="Cálculo caudal químico", layout="wide")

# --- Estilos personalizados ---
st.markdown(
    """
    <style>
    /* Ajustar slider */
    div[data-baseweb="slider"] {
        padding-top: 5px;
        padding-bottom: 5px;
    }
    div[data-baseweb="slider"] > div {
        height: 0.5rem;   /* grosor línea */
        background: #222; /* color base */
    }
    div[data-baseweb="slider"] span {
        font-size: 18px !important
