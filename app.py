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

if "Qnom" not in st.session_state:
    st.session_state["Qnom"] = 80.0  # L/h nominal

if "Fnom" not in st.session_state:
    st.session_state["Fnom"] = 50.0  # Hz nominal

if "Fmax" not in st.session_state:
    st.session_state["Fmax"] = 75.0  # Hz máxima (forzada)

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

# --- Sliders principales ---
bpm = st.slider("Seleccione BPM", 0.5, 20.0, 5.0, 0.1)
gpt = st.slider("Seleccione GPT", 0.0, 10.0, 1.5, 0.1)

# --- Cálculos agua y químico ---
gal_per_min = bpm * 42
l_per_min = gal_per_min * 3.785
m3_per_h = l_per_min * 0.06

q_quimico_gal_min = (gpt / 1000) * gal_per_min
q_quimico_l_min = q_quimico_gal_min * 3.785
q_quimico_l_h = q_quimico_l_min * 60  # <<< usamos en cálculos de bomba

# --- Caudal Agua ---
st.subheader("💧 Caudal Agua")

if st.session_state["unidad_agua"] == "m³/h":
    valor_agua = f"{m3_per_h:.1f} m³/h"
else:
    valor_agua = f"{bpm:.2f} BPM"

if st.button(valor_agua, key="btn_agua"):
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
    unidades = ["gal/min", "L/min", "L/h"]
    idx = unidades.index(st.session_state["unidad_quimico"])
    st.session_state["unidad_quimico"] = unidades[(idx + 1) % len(unidades)]
    st.rerun()

# --- Cálculo Bomba ---
st.subheader("⚡ Cálculo Bomba")

# Obtener parámetros configurados
Qnom = st.session_state["Qnom"]
Fnom = st.session_state["Fnom"]
Fmax = st.session_state["Fmax"]

# Calcular Qmax en función de la frecuencia forzada
Qmax = Qnom * (Fmax / Fnom)

Qset = q_quimico_l_h

if Qset > Qmax:
    st.error("⚠️ El caudal químico calculado supera el caudal máximo alcanzable con la frecuencia configurada (Fmax).")
else:
    vel = (Qset / Qmax) * 100
    st.metric("Velocidad [%]", f"{vel:.1f}")

    # Solo mostrar frecuencia si está en configuración
    if st.session_state["show_config"]:
        fset = (Qset / Qmax) * Fmax
        st.metric("Frecuencia [Hz]", f"{fset:.2f}")

# --- CONFIGURACIÓN AL FINAL ---
st.markdown("---")
if st.button("⚙️ Configuración"):
    st.session_state["show_config"] = not st.session_state["show_config"]

if st.session_state["show_config"]:
    st.subheader("⚙️ Parámetros de la Bomba")
    st.session_state["Qnom"] = st.number_input(
        "Caudal nominal bomba [L/h]",
        min_value=1.0,
        value=st.session_state["Qnom"],
        step=1.0
    )
    st.session_state["Fnom"] = st.number_input(
        "Frecuencia nominal bomba [Hz]",
        min_value=1.0,
        value=st.session_state["Fnom"],
        step=1.0
    )
    st.session_state["Fmax"] = st.number_input(
        "Frecuencia máxima de trabajo [Hz]",
        min_value=st.session_state["Fnom"],
        value=st.session_state["Fmax"],
        step=1.0
    )
