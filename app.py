import streamlit as st

# --- Configuración de página ---
st.set_page_config(page_title="Cálculo caudal químico", layout="wide")

# --- Inicializar estado de unidad ---
if "unidad_agua" not in st.session_state:
    st.session_state.unidad_agua = "m³/h"

# --- Logo y título centrados ---
st.markdown(
    """
    <div style="text-align: center;">
        <img src="https://raw.githubusercontent.com/joareq/caudal-quimico/main/logo.png" width="250">
        <h1 style="margin-top: 10px;">CALCULO CAUDAL QUIMICO</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# --- Diseño principal en dos columnas ---
col_sliders, col_resultados = st.columns([1, 1])

with col_sliders:
    gpt = st.slider("Seleccione GPT (galones por mil)", 0.0, 10.0, 1.5, 0.1)
    bpm = st.slider("Seleccione BPM (barriles por minuto)", 0.5, 20.0, 5.0, 0.1)

# --- Cálculos ---
gal_per_min = bpm * 42
l_per_min = gal_per_min * 3.785
m3_per_h = l_per_min * 0.06

q_quimico_gal_min = (gpt / 1000) * gal_per_min
q_quimico_l_min = q_quimico_gal_min * 3.785
q_quimico_l_h = q_quimico_l_min * 60

# --- Convertir caudal de agua si está en barriles ---
if st.session_state.unidad_agua == "m³/h":
    valor_agua = m3_per_h
    unidad = "m³/h"
else:
    valor_agua = bpm
    unidad = "BPM"

with col_resultados:
    # --- Caudal de Agua ---
    st.markdown("### 💧 Caudal de Agua")
    if st.button(f"{valor_agua:.0f} {unidad}", key="toggle_agua"):
        # Cambiar unidad al pulsar
        if st.session_state.unidad_agua == "m³/h":
            st.session_state.unidad_agua = "BPM"
        else:
            st.session_state.unidad_agua = "m³/h"
        st.rerun()   # ✅ ahora funciona con la versión nueva

    # --- Caudal Químico ---
    st.markdown(
        "### <img src='https://raw.githubusercontent.com/joareq/caudal-quimico/main/icono_skid.png' width='25'> Caudal Químico",
        unsafe_allow_html=True
    )

    c1, c2, c3 = st.columns(3)
    c1.metric("gal/min", f"{q_quimico_gal_min:.2f}")
    c2.metric("l/min", f"{q_quimico_l_min:.2f}")
    c3.metric("l/h", f"{q_quimico_l_h:.0f}")
