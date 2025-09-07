import streamlit as st

# --- Configuración de página ---
st.set_page_config(page_title="Cálculo caudal químico", layout="wide")

# --- Estilos personalizados ---
st.markdown(
    """
    <style>
    /* Quitar franja gris oscura de fondo */
    div[data-baseweb="slider"] {
        background: transparent !important;
    }
    div[data-baseweb="slider"] > div {
        background: transparent !important;
    }
    div[data-baseweb="slider"] > div > div {
        background: transparent !important;
    }

    /* Línea del slider */
    div[data-baseweb="slider"] > div {
        height: 0.5rem;
    }

    /* Número del valor */
    div[data-baseweb="slider"] span {
        font-size: 18px !important;
        color: #00AEEF !important; /* azul Hidrofrac */
        font-weight: bold;
    }

    /* El círculo (thumb) */
    div[data-baseweb="slider"] div[role="slider"] {
        background-color: #00AEEF !important;
        border: 2px solid white !important;
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

# --- Cálculos ---
gal_per_min = bpm * 42
l_per_min = gal_per_min * 3.785
m3_per_h = l_per_min * 0.06

q_quimico_gal_min = (gpt / 1000) * gal_per_min
q_quimico_l_min = q_quimico_gal_min * 3.785
q_quimico_l_h = q_quimico_l_min * 60

# --- Resultados Agua ---
st.markdown(
    f"""
    <div style="display: flex; align-items: center; gap: 10px; margin-top:20px;">
        <span style="font-size: 28px;">💧</span>
        <h3 style="margin: 0;">Caudal de Agua</h3>
        <h2 style="margin: 0; padding-left: 15px; color: white;">{m3_per_h:.2f} m³/h</h2>
    </div>
    """,
    unsafe_allow_html=True
)

# --- Resultados Químico ---
st.markdown("### 🔹 Resultados Químico")
c4, c5, c6 = st.columns(3)
c4.metric("Caudal químico [gal/min]", f"{q_quimico_gal_min:.4f}")
c5.metric("Caudal químico [L/min]", f"{q_quimico_l_min:.4f}")
c6.metric("Caudal químico [L/h]", f"{q_quimico_l_h:.2f}")
