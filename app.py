import streamlit as st

# Configuración
st.set_page_config(page_title="Cálculo caudal químico", layout="centered")

# Sliders de referencia
gpt = st.slider("Seleccione GPT (galones por mil)", 0.0, 10.0, 1.5, 0.1)
bpm = st.slider("Seleccione BPM (barriles por minuto)", 0.5, 20.0, 5.0, 0.1)

# Cálculo automático
gal_per_min = bpm * 42
l_per_min = gal_per_min * 3.785
m3_per_h_auto = l_per_min * 0.06

# --- Permitir al usuario modificar manualmente ---
st.markdown("### 💧 Caudal de Agua (editable)")
m3_per_h = st.number_input("Modificar m³/h:", value=round(m3_per_h_auto, 2), step=0.1)

# --- Caudal químico calculado ---
q_quimico_gal_min = (gpt / 1000) * gal_per_min
q_quimico_l_min = q_quimico_gal_min * 3.785
q_quimico_l_h = q_quimico_l_min * 60

col1, col2 = st.columns(2)
with col1:
    st.metric("Caudal Agua [m³/h]", f"{m3_per_h:.2f}")

with col2:
    st.markdown("### ⚗️ Caudal Químico")
    st.metric("gal/min", f"{q_quimico_gal_min:.2f}")
    st.metric("l/min", f"{q_quimico_l_min:.2f}")
    st.metric("l/h", f"{q_quimico_l_h:.0f}")
