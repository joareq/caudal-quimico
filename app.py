import streamlit as st

# --- Configuración de página ---
st.set_page_config(page_title="Caudal Químico", page_icon="💧", layout="wide")

st.title("💧 Calculadora de Caudal Químico (GPT vs BPM)")

# --- Inputs con sliders ---
col1, col2 = st.columns(2)

with col1:
    gpt = st.slider("Seleccione GPT (galones por mil)", min_value=0.0, max_value=10.0, value=1.5, step=0.1)

with col2:
    bpm = st.slider("Seleccione caudal de agua [BPM]", min_value=0.0, max_value=20.0, value=5.0, step=0.5)

# --- Cálculos ---
gal_per_min = bpm * 42
l_per_min = gal_per_min * 3.785
m3_per_h = l_per_min * 0.06

q_quimico_gal_min = (gpt / 1000) * gal_per_min
q_quimico_l_min = q_quimico_gal_min * 3.785
q_quimico_l_h = q_quimico_l_min * 60

# --- Resultados Agua ---
st.markdown("### 🔹 Resultados Agua")
c1, c2, c3 = st.columns(3)
c1.metric("Caudal agua [gal/min]", f"{gal_per_min:.2f}")
c2.metric("Caudal agua [L/min]", f"{l_per_min:.2f}")
c3.metric("Caudal agua [m³/h]", f"{m3_per_h:.2f}")

# --- Resultados Químico ---
st.markdown("### 🔹 Resultados Químico")
c4, c5, c6 = st.columns(3)
c4.metric("Caudal químico [gal/min]", f"{q_quimico_gal_min:.4f}")
c5.metric("Caudal químico [L/min]", f"{q_quimico_l_min:.4f}")
c6.metric("Caudal químico [L/h]", f"{q_quimico_l_h:.2f}")
