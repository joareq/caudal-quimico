import streamlit as st

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

# --- Inicializar estado ---
if "agua_val" not in st.session_state:
    st.session_state.agua_val = 48  # valor inicial m³/h
if "edit_mode" not in st.session_state:
    st.session_state.edit_mode = False

# --- Sincronizar slider con valor agua ---
# agua_val (m³/h) → bpm (barriles/min)
st.session_state.bpm = st.session_state.agua_val / 2.52 / 42  

col1, col2 = st.columns(2)
with col1:
    gpt = st.slider("Seleccione GPT (galones por mil)", 0.0, 10.0, 1.5, 0.1)
with col2:
    bpm = st.slider(
        "Seleccione BPM (barriles por minuto)",
        0.5, 20.0, float(st.session_state.bpm), 0.1,
        key="bpm_slider"
    )

# --- Cálculos ---
gal_per_min = bpm * 42
l_per_min = gal_per_min * 3.785
m3_per_h = l_per_min * 0.06

q_quimico_gal_min = (gpt / 1000) * gal_per_min
q_quimico_l_min = q_quimico_gal_min * 3.785
q_quimico_l_h = q_quimico_l_min * 60

# --- CSS tarjetas ---
st.markdown("""
<style>
.card {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    width: 120px;
    height: 120px;
    border: 1px solid #888;
    border-radius: 8px;
    text-align: center;
    cursor: pointer;
}
.card .value {
    font-size: 28px;
    font-weight: bold;
}
.card .unit {
    font-size: 14px;
    color: #ccc;
}
</style>
""", unsafe_allow_html=True)

# --- Mostrar resultados ---
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 💧 Caudal de Agua")

    if st.session_state.edit_mode:
        new_val = st.number_input(
            "Editar caudal (m³/h)", 
            value=float(st.session_state.agua_val), 
            step=1.0,
            key="agua_edit"
        )
        st.session_state.agua_val = int(new_val)
        st.session_state.edit_mode = False  # vuelve a mostrar tarjeta
    else:
        if st.button(
            f"{st.session_state.agua_val} m³/h", 
            key="agua_card"
        ):
            st.session_state.edit_mode = True

with col2:
    st.markdown("### <img src='https://raw.githubusercontent.com/joareq/caudal-quimico/main/icono_skid.png' width='25'> Caudal Químico", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"<div class='card'><div class='value'>{q_quimico_gal_min:.2f}</div><div class='unit'>gal/min</div></div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='card'><div class='value'>{q_quimico_l_min:.2f}</div><div class='unit'>l/min</div></div>", unsafe_allow_html=True)
    with c3:
        st.markdown(f"<div class='card'><div class='value'>{q_quimico_l_h:.0f}</div><div class='unit'>l/h</div></div>", unsafe_allow_html=True)
