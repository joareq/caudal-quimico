import streamlit as st

# --- Configuración de página ---
st.set_page_config(page_title="Cálculo caudal químico", layout="wide")

# --- Inicializar estados ---
if "unidad_agua" not in st.session_state:
    st.session_state["unidad_agua"] = "m³/h"

if "unidad_quimico" not in st.session_state:
    st.session_state["unidad_quimico"] = "gal/min"

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
col_sliders, col_resultados = st.columns([1, 1])
with col_sliders:
    bpm = st.slider("Seleccione BPM (barriles por minuto)", 0.5, 20.0, 5.0, 0.1)
    gpt = st.slider("Seleccione GPT (galones por mil)", 0.0, 10.0, 1.5, 0.1)

# --- Cálculos ---
gal_per_min = bpm * 42
l_per_min = gal_per_min * 3.785
m3_per_h = l_per_min * 0.06

q_quimico_gal_min = (gpt / 1000) * gal_per_min
q_quimico_l_min = q_quimico_gal_min * 3.785
q_quimico_l_h = q_quimico_l_min * 60

# --- Estilo de los cuadros ---
def render_card(valor, unidad, key):
    return f"""
    <div onclick="fetch('/_stcore/{key}', {{method: 'POST'}})"
         style="cursor:pointer; border:1px solid #555; border-radius:8px;
                padding:20px; width:140px; height:140px;
                display:flex; flex-direction:column;
                align-items:center; justify-content:center;
                text-align:center;">
        <div style="font-size:28px; font-weight:bold;">{valor}</div>
        <div style="font-size:14px; color:gray;">{unidad}</div>
    </div>
    """

# --- Funciones de cambio de unidad ---
def cambiar_unidad_agua():
    st.session_state["unidad_agua"] = "BPM" if st.session_state["unidad_agua"] == "m³/h" else "m³/h"

def cambiar_unidad_quimico():
    unidades = ["gal/min", "L/min", "L/h"]
    idx = unidades.index(st.session_state["unidad_quimico"])
    st.session_state["unidad_quimico"] = unidades[(idx + 1) % len(unidades)]

# --- Resultados ---
with col_resultados:
    # --- Caudal Agua ---
    st.markdown("### 💧 Caudal de Agua")

    if st.session_state["unidad_agua"] == "m³/h":
        valor_agua = f"{m3_per_h:.1f}"
    else:
        valor_agua = f"{bpm:.2f}"

    if st.button("agua", key="agua_btn", label_visibility="collapsed"):
        cambiar_unidad_agua()
    st.markdown(render_card(valor_agua, st.session_state["unidad_agua"], "agua_btn"), unsafe_allow_html=True)

    # --- Caudal Químico ---
    st.markdown("### <img src='https://raw.githubusercontent.com/joareq/caudal-quimico/main/icono_skid.png' width='25'> Caudal Químico", unsafe_allow_html=True)

    if st.session_state["unidad_quimico"] == "gal/min":
        valor_q = f"{q_quimico_gal_min:.2f}"
    elif st.session_state["unidad_quimico"] == "L/min":
        valor_q = f"{q_quimico_l_min:.2f}"
    else:
        valor_q = f"{q_quimico_l_h:.0f}"

    if st.button("quimico", key="quimico_btn", label_visibility="collapsed"):
        cambiar_unidad_quimico()
    st.markdown(render_card(valor_q, st.session_state["unidad_quimico"], "quimico_btn"), unsafe_allow_html=True)
