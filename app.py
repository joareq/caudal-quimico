import streamlit as st

# --- Configuración de página ---
st.set_page_config(page_title="Cálculo caudal químico", layout="centered")

# --- Estilos personalizados ---
st.markdown(
    """
    <style>
    /* Número del slider */
    div[data-baseweb="slider"] span {
        font-size: 18px !important;
        color: #00AEEF !important;
        font-weight: bold;
    }
    /* Círculo del slider */
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
        <img src="https://raw.githubusercontent.com/joareq/caudal-quimico/main/logo.png" width="200">
        <h1 style="margin-top: 10px;">CALCULO CAUDAL QUIMICO</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# --- Sliders (uno debajo del otro) ---
gpt = st.slider("Seleccione GPT (galones por mil)", 0.0, 10.0, 1.5, 0.1)
bpm = st.slider("Seleccione BPM (barriles por minuto)", 0.5, 20.0, 5.0, 0.1)

# --- Cálculos ---
gal_per_min = bpm * 42
l_per_min = gal_per_min * 3.785
m3_per_h = l_per_min * 0.06

q_quimico_gal_min = (gpt / 1000) * gal_per_min
q_quimico_l_min = q_quimico_gal_min * 3.785
q_quimico_l_h = q_quimico_l_min * 60

# --- Layout de resultados ---
col1, col2 = st.columns(2)

with col1:
    st.markdown(
        f"""
        <div style="display: flex; align-items: center; gap: 10px; margin-top:20px;">
            <span style="font-size: 28px;">💧</span>
            <h3 style="margin: 0;">Caudal de Agua</h3>
        </div>
        <h2 style="margin: 0; color: white;">{m3_per_h:.2f} m³/h</h2>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown("### Caudal Químico")
    st.write(f"**{q_quimico_gal_min:.2f} gal/min**")
    st.write(f"**{q_quimico_l_min:.2f} l/min**")
    st.write(f"**{q_quimico_l_h:.0f} l/h**")

# --- Imagen decorativa al final ---
st.markdown(
    """
    <div style="text-align: center; margin-top: 20px;">
        <img src="https://raw.githubusercontent.com/joareq/caudal-quimico/main/icono_skid.png" width="120">
    </div>
    """,
    unsafe_allow_html=True
)
