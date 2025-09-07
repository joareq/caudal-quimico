import streamlit as st

st.set_page_config(page_title="Cálculo caudal químico", layout="wide")

# --- CSS global ---
st.markdown("""
<style>
.card {
  width: 120px; height: 120px;
  display:flex; flex-direction:column; align-items:center; justify-content:center;
  border:1px solid #ccc; border-radius:8px;
  font-weight:bold; margin:6px; background:transparent;
}
.card .value { font-size:28px; }
.card .unit  { font-size:14px; margin-top:6px; }
</style>
""", unsafe_allow_html=True)

# --- Estado inicial ---
if "bpm" not in st.session_state: st.session_state.bpm = 5.0
if "gpt" not in st.session_state: st.session_state.gpt = 1.5
if "m3_per_h" not in st.session_state: st.session_state.m3_per_h = None

# --- Sliders ---
csl1, csl2 = st.columns(2)
with csl1:
    st.session_state.gpt = st.slider("Seleccione GPT (galones por mil)", 0.0, 10.0, st.session_state.gpt, 0.1)
with csl2:
    st.session_state.bpm = st.slider("Seleccione BPM (barriles por minuto)", 0.5, 20.0, st.session_state.bpm, 0.1)

# --- Cálculos ---
gal_per_min = st.session_state.bpm * 42
l_per_min   = gal_per_min * 3.785
m3_per_h    = l_per_min * 0.06

q_quimico_gal_min = (st.session_state.gpt / 1000) * gal_per_min
q_quimico_l_min   = q_quimico_gal_min * 3.785
q_quimico_l_h     = q_quimico_l_min * 60

# --- Layout ---
col1, col2 = st.columns(2)

# Caudal Agua
with col1:
    st.markdown("### 💧 Caudal de Agua")

    # input editable pero con el mismo formato
    agua = st.number_input(
        " ",
        value=float(round(m3_per_h, 2)),
        key="agua_input",
        label_visibility="collapsed",
        step=0.1
    )

    # Mostrar el cuadrado con estilo
    st.markdown(
        f"""
        <div class="card">
            <div class="value">{agua:.0f}</div>
            <div class="unit">m³/h</div>
        </div>
        """, unsafe_allow_html=True
    )

    # recalcular slider BPM si cambia manualmente el caudal agua
    if agua != round(m3_per_h, 2):
        denom = 42*3.785*0.06
        st.session_state.bpm = max(0.5, min(20.0, agua/denom))
        st.rerun()

# Caudal Químico
with col2:
    st.markdown(
        "### <img src='https://raw.githubusercontent.com/joareq/caudal-quimico/main/icono_skid.png' width='30'> Caudal Químico",
        unsafe_allow_html=True
    )
    st.markdown(
        f"""
        <div style="display:flex; gap:10px; flex-wrap:wrap;">
            <div class="card">
                <div class="value">{q_quimico_gal_min:.2f}</div>
                <div class="unit">gal/min</div>
            </div>
            <div class="card">
                <div class="value">{q_quimico_l_min:.2f}</div>
                <div class="unit">l/min</div>
            </div>
            <div class="card">
                <div class="value">{q_quimico_l_h:.0f}</div>
                <div class="unit">l/h</div>
            </div>
        </div>
        """, unsafe_allow_html=True
    )
