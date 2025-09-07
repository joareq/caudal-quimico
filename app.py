import streamlit as st

# =====================
# Configuración general
# =====================
st.set_page_config(page_title="Cálculo caudal químico", layout="wide")

# Constantes de conversión
GAL_TO_L = 3.785411784
FACTOR_M3H_POR_BPM = 42 * GAL_TO_L * 0.06  # ≈ 9.5382 m³/h por BPM

# ============
# Encabezado
# ============
st.markdown(
    """
    <div style="text-align:center;">
        <img src="https://raw.githubusercontent.com/joareq/caudal-quimico/main/logo.png" width="250" />
        <h1 style="margin-top:10px;">CALCULO CAUDAL QUIMICO</h1>
    </div>
    """,
    unsafe_allow_html=True,
)

# ===================================
# Estado inicial y funciones de sync
# ===================================
if "bpm" not in st.session_state:
    st.session_state.bpm = 5.0
if "agua_m3h" not in st.session_state:
    st.session_state.agua_m3h = round(st.session_state.bpm * FACTOR_M3H_POR_BPM, 2)
if "edit_agua" not in st.session_state:
    st.session_state.edit_agua = False

def sync_from_bpm():
    st.session_state.agua_m3h = round(st.session_state.bpm * FACTOR_M3H_POR_BPM, 2)

def sync_from_agua():
    st.session_state.bpm = round(st.session_state.agua_m3h / FACTOR_M3H_POR_BPM, 2)

# =========
# Sliders
# =========
csl1, csl2 = st.columns(2)
with csl1:
    gpt = st.slider("Seleccione GPT (galones por mil)", 0.0, 10.0, 1.5, 0.1, key="gpt")
with csl2:
    st.slider(
        "Seleccione BPM (barriles por minuto)",
        0.5,
        20.0,
        key="bpm",
        on_change=sync_from_bpm,
    )

# ===================
# Cálculos hidráulica
# ===================
gal_per_min = st.session_state.bpm * 42
l_per_min = gal_per_min * GAL_TO_L

# ===================
# Cálculos Químico
# ===================
q_quimico_gal_min = (st.session_state.gpt / 1000.0) * gal_per_min
q_quimico_l_min = q_quimico_gal_min * GAL_TO_L
q_quimico_l_h = q_quimico_l_min * 60

# =========
# Estilos
# =========
st.markdown(
    """
    <style>
    .card {
        display:flex; flex-direction:column; justify-content:center; align-items:center;
        width: 140px; height: 140px;
        border:1px solid #888; border-radius:12px; text-align:center;
        background: transparent;
    }
    .card .value { font-size:30px; font-weight:700; line-height:1; }
    .card .unit  { font-size:14px; color:#cfcfcf; margin-top:6px; }
    .stNumberInput input {
        font-size:30px !important;
        font-weight:700 !important;
        text-align:center !important;
    }
    .stNumberInput {
        width: 140px !important;
        height: 140px !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ===================
# Layout de resultados
# ===================
col_agua, col_quim = st.columns(2)

# -------- Caudal de Agua (editable) ----------
with col_agua:
    st.markdown("### 💧 Caudal de Agua")

    if st.session_state.edit_agua:
        st.number_input(
            "Editar caudal (m³/h)",
            min_value=0.0,
            max_value=1000.0,
            step=1.0,
            value=float(st.session_state.agua_m3h),
            key="agua_m3h",
            on_change=sync_from_agua,
            label_visibility="collapsed",
        )
    else:
        if st.button(
            f"**{int(round(st.session_state.agua_m3h))}**\n m³/h",
            key="btn_agua",
            help="Click para editar",
        ):
            st.session_state.edit_agua = True

# -------- Caudal Químico (vista) ----------
with col_quim:
    st.markdown(
        "### <img src='https://raw.githubusercontent.com/joareq/caudal-quimico/main/icono_skid.png' width='25'> Caudal Químico",
        unsafe_allow_html=True,
    )
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            f"<div class='card'><div class='value'>{q_quimico_gal_min:.2f}</div><div class='unit'>gal/min</div></div>",
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f"<div class='card'><div class='value'>{q_quimico_l_min:.2f}</div><div class='unit'>l/min</div></div>",
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            f"<div class='card'><div class='value'>{q_quimico_l_h:.0f}</div><div class='unit'>l/h</div></div>",
            unsafe_allow_html=True,
        )
