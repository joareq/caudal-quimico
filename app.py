import streamlit as st

# --- Configuración de página ---
st.set_page_config(page_title="Cálculo caudal químico", layout="wide")

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

# --- Sliders ---
col1, col2 = st.columns(2)
with col1:
    gpt = st.slider("Seleccione GPT (galones por mil)", 0.0, 10.0, 1.5, 0.1)
with col2:
    bpm = st.slider("Seleccione BPM (barriles por minuto)", 0.5, 20.0, 5.0, 0.1)

# --- Cálculos ---
gal_per_min = bpm * 42
l_per_min = gal_per_min * 3.785
m3_per_h = l_per_min * 0.06

q_quimico_gal_min = (gpt / 1000) * gal_per_min
q_quimico_l_min = q_quimico_gal_min * 3.785
q_quimico_l_h = q_quimico_l_min * 60

# --- Layout Resultados ---
c1, c2 = st.columns(2)

# --- Caudal Agua ---
with c1:
    st.markdown("### 💧 Caudal de Agua")
    caudal_edit = st.number_input("Modificar [m³/h]:", value=round(m3_per_h, 2), step=0.1, label_visibility="collapsed")
    st.markdown(
        f"""
        <div style="border:1px solid #ccc; border-radius:6px; padding:15px; text-align:center; font-size:28px; font-weight:bold;">
            {caudal_edit} m³/h
        </div>
        """,
        unsafe_allow_html=True
    )

# --- Caudal Químico ---
with c2:
    st.markdown("### <img src='https://raw.githubusercontent.com/joareq/caudal-quimico/main/icono_skid.png' width='30'> Caudal Químico", unsafe_allow_html=True)

    st.markdown(
        f"""
        <div style="display:flex; flex-wrap:wrap; gap:10px;">
            <div style="flex:1; border:1px solid #ccc; border-radius:6px; padding:10px; text-align:center; font-size:22px; font-weight:bold;">
                {q_quimico_gal_min:.2f} <br><span style="font-size:14px;">gal/min</span>
            </div>
            <div style="flex:1; border:1px solid #ccc; border-radius:6px; padding:10px; text-align:center; font-size:22px; font-weight:bold;">
                {q_quimico_l_min:.2f} <br><span style="font-size:14px;">l/min</span>
            </div>
            <div style="flex:1 100%; border:1px solid #ccc; border-radius:6px; padding:10px; text-align:center; font-size:22px; font-weight:bold;">
                {q_quimico_l_h:.0f} <br><span style="font-size:14px;">l/h</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
