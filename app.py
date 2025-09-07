import streamlit as st

# --- Configuración de página ---
st.set_page_config(page_title="Cálculo caudal químico", layout="wide")

# --- Inicializar estados ---
if "unidad_agua" not in st.session_state:
    st.session_state["unidad_agua"] = "m³/h"

if "unidad_quimico" not in st.session_state:
    st.session_state["unidad_quimico"] = "gal/min"

# --- Logo y título ---
st.title("Cálculo caudal químico")

# --- Sliders ---
bpm = st.slider("Seleccione BPM (barriles por minuto)", 0.5, 20.0, 5.0, 0.1)
gpt = st.slider("Seleccione GPT (galones por mil)", 0.0, 10.0, 1.5, 0.1)

# --- Cálculos ---
gal_per_min = bpm * 42
l_per_min = gal_per_min * 3.785
m3_per_h = l_per_min * 0.06

q_quimico_gal_min = (gpt / 1000) * gal_per_min
q_quimico_l_min = q_quimico_gal_min * 3.785
q_quimico_l_h = q_quimico_l_min * 60

# --- Caudal Agua ---
st.subheader("💧 Caudal de Agua")

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
st.subheader("🧪 Caudal Químico")

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
