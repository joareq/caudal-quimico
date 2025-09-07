import streamlit as st

# --- Configuración de página ---
st.set_page_config(page_title="Cálculo caudal químico", layout="wide")

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

# --- Sliders ---
col1, col2 = st.columns(2)
with col1:
    gpt = st.slider("Seleccione GPT (galones por mil)", 0.0, 10.0, 1.5, 0.1)
with col2:
    bpm = st.slider("Seleccione BPM (barriles por minuto)", 0.5, 20.0, 5.0, 0.1)

# --- Cálculos automáticos ---
gal_per_min = bpm * 42
l_per_min = gal_per_min * 3.785
m3_per_h_auto = l_per_min * 0.06

# --- Estado editable del caudal de agua ---
if "edit_agua" not in st.session_state:
    st.session_state.edit_agua = False
if "m3_per_h" not in st.session_state:
    st.session_state.m3_per_h = round(m3_per_h_auto, 2)

# --- Layout Agua y Químico ---
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 💧 Caudal de Agua")

    if st.session_state.edit_agua:
        nuevo_valor = st.number_input("Editar m³/h", value=st.session_state.m3_per_h, step=0.1)
        st.session_state.m3_per_h = nuevo_valor
        if st.button("✔ Confirmar"):
            st.session_state.edit_agua = False
    else:
        if st.button(f"**{st.session_state.m3_per_h:.0f} m³/h**", use_container_width=True):
            st.session_state.edit_agua = True

with col2:
    st.markdown("### 🏭 Caudal Químico")

    q_quimico_gal_min = (gpt / 1000) * gal_per_min
    q_quimico_l_min = q_quimico_gal_min * 3.785
    q_quimico_l_h = q_quimico_l_min * 60

    st.markdown(
        f"""
        <div style="border:1px solid #ccc; border-radius:5px; padding:10px; font-size:22px; text-align:center;">
            {q_quimico_gal_min:.2f} gal/min<br>
            {q_quimico_l_min:.2f} l/min<br>
            {q_quimico_l_h:.0f} l/h
        </div>
        """,
        unsafe_allow_html=True
    )
