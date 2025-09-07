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

# --- Sliders principales ---
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

# --- Estado para edición ---
if "edit_mode" not in st.session_state:
    st.session_state.edit_mode = False

# --- CSS ---
st.markdown("""
<style>
.card {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    width: 120px;
    height: 120px;
    border: 1px solid #888;
    border-radius: 8px;
    text-align: center;
    cursor: pointer;
}
.card .value {
    font-size: 28px;
    font-weight: bold;
}
.card .unit {
    font-size: 14px;
    color: #ccc;
}
</style>
""", unsafe_allow_html=True)

# --- Resultados ---
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 💧 Caudal de Agua")

    # Botón oculto
    trig = st.button("AGUA_EDIT", key="agua_trigger_btn")
    st.markdown("""
    <style>
    button[kind="secondary"] p:contains("AGUA_EDIT"),
    button:has(> div p:contains("AGUA_EDIT")) {
        display:none !important;
    }
    </style>
    """, unsafe_allow_html=True)

    if trig:
        st.session_state.edit_mode = not st.session_state.edit_mode

    if st.session_state.edit_mode:
        new_val = st.number_input("Editar caudal agua (m³/h)", value=float(m3_per_h), step=1.0)
        m3_per_h = new_val
    else:
        st.markdown(
            f"""
            <div class="card" onclick="Array.from(window.parent.document.querySelectorAll('button'))
                .filter(b => b.innerText.trim() === 'AGUA_EDIT')
                .forEach(b => b.click());">
              <div class="value">{int(round(m3_per_h))}</div>
              <div class="unit">m³/h</div>
            </div>
            """,
            unsafe_allow_html=True
        )

with col2:
    st.markdown("### <img src='https://raw.githubusercontent.com/joareq/caudal-quimico/main/icono_skid.png' width='25'> Caudal Químico", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""
        <div class="card">
          <div class="value">{q_quimico_gal_min:.2f}</div>
          <div class="unit">gal/min</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="card">
          <div class="value">{q_quimico_l_min:.2f}</div>
          <div class="unit">l/min</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="card">
          <div class="value">{q_quimico_l_h:.0f}</div>
          <div class="unit">l/h</div>
        </div>
        """, unsafe_allow_html=True)
