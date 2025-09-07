import streamlit as st

# --- Configuración de página ---
st.set_page_config(page_title="Cálculo caudal químico", layout="centered")

# --- Estilos personalizados ---
st.markdown(
    """
    <style>
    .box {
        border: 1px solid white;
        padding: 15px;
        border-radius: 5px;
        display: inline-block;
        margin: 5px;
        text-align: center;
        min-width: 120px;
    }
    .big {
        font-size: 28px;
        font-weight: bold;
    }
    .unit {
        font-size: 16px;
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

# --- Sliders ---
gpt = st.slider("Seleccione GPT (galones por mil)", 0.0, 10.0, 1.5, 0.1)
bpm = st.slider("Seleccione BPM (barriles por minuto)", 0.5, 20.0, 5.0, 0.1)

# --- Cálculos ---
gal_per_min = bpm * 42
l_per_min = gal_per_min * 3.785
m3_per_h = l_per_min * 0.06

q_quimico_gal_min = (gpt / 1000) * gal_per_min
q_quimico_l_min = q_quimico_gal_min * 3.785
q_quimico_l_h = q_quimico_l_min * 60

# --- Layout ---
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 💧 Caudal de Agua")
    st.markdown(
        f"<div class='box'><span class='big'>{m3_per_h:.0f}</span><br><span class='unit'>m³/h</span></div>",
        unsafe_allow_html=True
    )

with col2:
    st.markdown("### <img src='https://raw.githubusercontent.com/joareq/caudal-quimico/main/icono_skid.png' width='40'> Caudal Químico",
                unsafe_allow_html=True)
    st.markdown(
        f"""
        <div>
            <div class='box'><span class='big'>{q_quimico_gal_min:.2f}</span><br><span class='unit'>gal/min</span></div>
            <div class='box'><span class='big'>{q_quimico_l_min:.2f}</span><br><span class='unit'>l/min</span></div>
            <div class='box'><span class='big'>{q_quimico_l_h:.0f}</span><br><span class='unit'>l/h</span></div>
        </div>
        """,
        unsafe_allow_html=True
    )
