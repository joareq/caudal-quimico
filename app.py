import streamlit as st

# --- Configuración de página ---
st.set_page_config(page_title="Cálculo caudal químico", layout="wide")

# --- Estilos personalizados ---
st.markdown(
    """
    <style>
    div[data-testid="stButton"] button {
        background-color: #007BFF;
        color: white;
        font-size: 28px;
        font-weight: bold;
        border: none;
        border-radius: 50%;
        width: 70px;
        height: 70px;
        text-align: center;
        line-height: 70px;
        cursor: pointer;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.3);
        transition: all 0.1s ease-in-out;
    }
    div[data-testid="stButton"] button:hover {
        background-color: #0056b3;
        transform: scale(1.05);
    }
    </style>
    """,
    unsafe_allow_html=True
)

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

# --- Inicializar valores ---
if "gpt" not in st.session_state:
    st.session_state.gpt = 1.5
if "bpm" not in st.session_state:
    st.session_state.bpm = 5.0

# --- Controles GPT ---
st.subheader("Control de GPT")
col1, col2, col3 = st.columns([1, 3, 1])
with col1:
    if st.button("➖ GPT"):
        st.session_state.gpt = max(0.0, st.session_state.gpt - 0.1)
with col2:
    st.session_state.gpt = st.slider(
        "Seleccione GPT (galones por mil)",
        0.0, 10.0, st.session_state.gpt, 0.1, key="gpt_slider"
    )
with col3:
    if st.button("➕ GPT"):
        st.session_state.gpt = min(10.0, st.session_state.gpt + 0.1)

# --- Controles BPM ---
st.subheader("Control de BPM")
col4, col5, col6 = st.columns([1, 3, 1])
with col4:
    if st.button("➖ BPM"):
        st.session_state.bpm = max(0.5, st.session_state.bpm - 0.1)
with col5:
    st.session_state.bpm = st.slider(
        "Seleccione BPM (barriles por minuto)",
        0.5, 20.0, st.session_state.bpm, 0.1, key="bpm_slider"
    )
with col6:
    if st.button("➕ BPM"):
        st.session_state.bpm = min(20.0, st.session_state.bpm + 0.1)

# --- Cálculos ---
gpt = st.session_state.gpt
bpm = st.session_state.bpm

gal_per_min = bpm * 42
l_per_min = gal_per_min * 3.785
m3_per_h = l_per_min * 0.06

q_quimico_gal_min = (gpt / 1000) * gal_per_min
q_quimico_l_min = q_quimico_gal_min * 3.785
q_quimico_l_h = q_quimico_l_min * 60

# --- Resultados Agua ---
st.markdown(
    f"""
    <div style="display: flex; align-items: center; gap: 10px;">
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
c6.metric("Caudal químico [L/h]", f"{q_quimi_
