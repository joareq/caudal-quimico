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

# --- Inicializar estados ---
if "bpm" not in st.session_state:
    st.session_state.bpm = 5.0
if "gpt" not in st.session_state:
    st.session_state.gpt = 1.5
if "edit_mode" not in st.session_state:
    st.session_state.edit_mode = False

# --- Sliders ---
col1, col2 = st.columns(2)
with col1:
    st.session_state.gpt = st.slider(
        "Seleccione GPT (galones por mil)", 
        0.0, 10.0, st.session_state.gpt, 0.1, key="gpt_slider"
    )
with col2:
    st.session_state.bpm = st.slider(
        "Seleccione BPM (barriles por minuto)", 
        0.5, 20.0, st.session_state.bpm, 0.1, key="bpm_slider"
    )

# --- Cálculos ---
gal_per_min = st.session_state.bpm * 42
l_per_min = gal_per_min * 3.785
m3_per_h = l_per_min * 0.06

q_quimico_gal_min = (st.session_state.gpt / 1000) * gal_per_min
q_quimico_l_min = q_quimico_gal_min * 3.785
q_quimico_l_h = q_quimico_l_min * 60

# --- Estilo CSS para cuadros cuadrados ---
st.markdown(
    """
    <style>
    .card {
        width: 120px; 
        height: 120px; 
        display: flex; 
        flex-direction: column; 
        align-items: center; 
        justify-content: center; 
        border: 1px solid #ccc; 
        border-radius: 8px; 
        font-weight: bold; 
        margin: 5px;
        background-color: transparent;
    }
    .value {
        font-size: 26px;
    }
    .unit {
        font-size: 14px;
        margin-top: 5px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Layout Resultados ---
c1, c2 = st.columns(2)

# --- Caudal Agua (editable) ---
with c1:
    st.markdown("### 💧 Caudal de Agua")

    if st.session_state.edit_mode:
        nuevo_valor = st.number_input(
            "Modificar [m³/h]:", 
            value=round(m3_per_h, 2), 
            step=0.1, 
            label_visibility="collapsed"
        )
        if nuevo_valor != m3_per_h and nuevo_valor > 0:
            st.session_state.bpm = (nuevo_valor / 0.06) / 3.785 / 42
            st.session_state.edit_mode = False
            st.rerun()
    else:
        if st.button(
            f"""
            <div class="card">
                <div class="value">{m3_per_h:.0f}</div>
                <div class="unit">m³/h</div>
            </div>
            """, 
            unsafe_allow_html=True
        ):
            st.session_state.edit_mode = True
            st.rerun()

# --- Caudal Químico ---
with c2:
    st.markdown(
        "### <img src='https://raw.githubusercontent.com/joareq/caudal-quimico/main/icono_skid.png' width='30'> Caudal Químico", 
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div style="display:flex; gap:10px; flex-wrap:wrap;">
            <div class="card">
                <div class="value">{q_quimico_gal_min:.2f}</div>
                <div class="unit">gal/min</div>
            </div>
            <div class="card">
                <div class="value">{q_quimico_l_min:.2f}</div>
                <div class="unit">l/min</div>
            </div>
            <div class="card">
                <div class="value">{q_quimico_l_h:.0f}</div>
                <div class="unit">l/h</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
