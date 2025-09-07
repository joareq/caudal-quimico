import streamlit as st

# --- Configuración de página ---
st.set_page_config(page_title="Cálculo caudal químico", layout="wide")

# --- Inicializar estados ---
if "unidad_agua" not in st.session_state:
    st.session_state["unidad_agua"] = "m³/h"

if "unidad_quimico" not in st.session_state:
    st.session_state["unidad_quimico"] = "gal/min"

if "show_config" not in st.session_state:
    st.session_state["show_config"] = False

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

# --- Botón Configuración ---
if st.button("⚙️ Configuración"):
    st.session_state["show_config"] = not st.session_state["show_config"]

if st.session_state["show_config"]:
    st.subheader("⚙️ Parámetros de la Bomba")
    Qmax = st.number_input("Caudal máximo bomba [L/min]", min_value=1.0, value=100.0, step=1.0, key="Qmax")
    Fmax = st.number_input("Frecuencia máxima variador [Hz]", min_value=1.0, value=75.0, step=1.0, key="Fmax")
else:
    # Valores por defecto si no se configuró
    Qmax = 100.0
    Fmax = 75.0

# --- Sliders principales ---
bpm = st.slider("Seleccione BPM", 0.5, 20.0, 5.0, 0.1)
gpt = st.slider("Seleccione GPT", 0.0, 10.0, 1.5, 0.1)

# --- Cálculos ---
gal_per_min = bpm * 42
l_per_min = gal_per_min * 3.785
m3_per_h = l_per_min * 0.06

q_quimico_gal_min = (gpt / 1000) * gal_per_min
q_quimico_l_min = q_quimico_gal_min * 3.785
q_quimico_l_h = q_quimico_l_min * 60

# --- Caudal Agua ---
st.subheader("💧 Caudal Agua")

if st.session_state["unidad_agua"] == "m³/h":
    valor_agua = f"{m3_per_h:.1f} m³/h"
else:
    valor_agua = f"{bpm:.2f} BPM"

if st.button(valor_agua, key="btn_agua"):
    # Toggle de unidad
    if st.session_state["unidad_agua"] == "m³/h":
        st.session_state["unidad_agua"] = "BPM"
    else:
        st.session_state["unidad_agua"] = "m³/h"
    st.rerun()

# --- Caudal Químico ---
st.markdown(
    "### <img src='https://raw.githubusercontent.com/joareq/caudal-quimico/main/icono_skid.png' width='100'> Caudal Químico",
    unsafe_allow_html=True
)

if st.session_state["unidad_quimico"] == "gal/min":
    valor_q = f"{q_quimico_gal_min:.2f} gal/min"
elif st.session_state["unidad_quimico"] == "L/min":
    valor_q = f"{q_quimico_l_min:.2f} L/min"
else:
    valor_q = f"{q_quimico_l_h:.0f} L/h"

if st.button(valor_q, key="btn_quimico"):
    # Rotar unidades
    unidades = ["gal/min", "L/min", "L/h"]
    idx = unidades.index(st.session_state["unidad_quimico"])
    st.session_state["unidad_quimico"] = unidades[(idx + 1) % len(unidades)]
    st.rerun()

# --- Cálculo Frecuencia según caudal químico ---
st.subheader("⚡ Cálculo Frecuencia Variador")

Qset = q_quimico_l_min  # se toma el caudal químico en L/min

if Qset > Qmax:
    st.error("⚠️ El caudal químico calculado supera el caudal máximo configurado de la bomba.")
else:
    vel = (Qset / Qmax) * 100
    fset = (Qset / Qmax) * Fmax

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Velocidad [%]", f"{vel:.1f}")
    with col2:
        st.metric("Frecuencia [Hz]", f"{fset:.2f}")
