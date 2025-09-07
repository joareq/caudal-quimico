import streamlit as st

# --- Configuración de página ---
st.set_page_config(page_title="Cálculo caudal químico", layout="wide")

# --- Inicializar estados ---
if "unidad_agua" not in st.session_state:
    st.session_state["unidad_agua"] = "m³/h"

if "unidad_quimico" not in st.session_state:
    st.session_state["unidad_quimico"] = "gal/min"

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

# --- Layout principal: sliders a la izquierda, resultados a la derecha ---
col_sliders, col_resultados = st.columns([1, 1])

with col_sliders:
    bpm = st.slider("Seleccione BPM (barriles por minuto)", 0.5, 20.0, 5.0, 0.1)
    gpt = st.slider("Seleccione GPT (galones por mil)", 0.0, 10.0, 1.5, 0.1)

# --- Cálculos hidráulica ---
gal_per_min = bpm * 42
l_per_min = gal_per_min * 3.785
m3_per_h = l_per_min * 0.06

# --- Cálculos químico ---
q_quimico_gal_min = (gpt / 1000) * gal_per_min
q_quimico_l_min = q_quimico_gal_min * 3.785
q_quimico_l_h = q_quimico_l_min * 60

# --- Funciones de cambio de unidad ---
def cambiar_unidad_agua():
    st.session_state["unidad_agua"] = "BPM" if st.session_state["unidad_agua"] == "m³/h" else "m³/h"

def cambiar_unidad_quimico():
    unidades = ["gal/min", "L/min", "L/h"]
    idx = unidades.index(st.session_state["unidad_quimico"])
    st.session_state["unidad_quimico"] = unidades[(idx + 1) % len(unidades)]

# --- Estilos de tarjetas ---
card_style = """
    border:1px solid #555; border-radius:8px;
    padding:20px; width:140px; height:140px;
    text-align:center;
"""

# --- Resultados ---
with col_resultados:
    # --- Caudal de Agua ---
    st.markdown("### 💧 Caudal de Agua")

    if st.session_state["unidad_agua"] == "m³/h":
        valor_agua = m3_per_h
    else:
        valor_agua = bpm

    if st.button(
        f"""
        <div style="{card_style}">
            <div style="font-size:28px; font-weight:bold;">{valor_agua:.1f}</div>
            <div style="font-size:14px; color:gray;">{st.session_state["unidad_agua"]}</div>
        </div>
        """,
        key="agua_card",
        on_click=cambiar_unidad_agua,
        help="Click para cambiar unidad",
        use_container_width=False,
    ):
        pass

    # --- Caudal Químico ---
    st.markdown("### <img src='https://raw.githubusercontent.com/joareq/caudal-quimico/main/icono_skid.png' width='25'> Caudal Químico", unsafe_allow_html=True)

    if st.session_state["unidad_quimico"] == "gal/min":
        valor_q = q_quimico_gal_min
    elif st.session_state["unidad_quimico"] == "L/min":
        valor_q = q_quimico_l_min
    else:
        valor_q = q_quimico_l_h

    if st.button(
        f"""
        <div style="{card_style}">
            <div style="font-size:28px; font-weight:bold;">{valor_q:.2f}</div>
            <div style="font-size:14px; color:gray;">{st.session_state["unidad_quimico"]}</div>
        </div>
        """,
        key="quimico_card",
        on_click=cambiar_unidad_quimico,
        help="Click para cambiar unidad",
        use_container_width=False,
    ):
        pass
