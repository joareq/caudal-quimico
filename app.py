import streamlit as st

# --- Config de página ---
st.set_page_config(page_title="Cálculo caudal químico", layout="wide")

# --- CSS: estilo de los cuadrados ---
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

/* Botón cuadrado para Caudal Agua */
.square-btn > div.stButton > button {
  width: 120px; height: 120px;
  border:1px solid #ccc; border-radius:8px;
  background:transparent; color:#fff; font-weight:bold;
  font-size:28px; line-height:1.1; white-space:pre-line;
  display:flex; flex-direction:column; align-items:center; justify-content:center;
  padding:0;
}
</style>
""", unsafe_allow_html=True)

# --- Logo + título ---
st.markdown("""
<div style="text-align:center;">
  <img src="https://raw.githubusercontent.com/joareq/caudal-quimico/main/logo.png" width="250">
  <h1 style="margin-top:10px;">CALCULO CAUDAL QUIMICO</h1>
</div>
""", unsafe_allow_html=True)

# --- Estado inicial ---
if "bpm" not in st.session_state: st.session_state.bpm = 5.0
if "gpt" not in st.session_state: st.session_state.gpt = 1.5
if "edit_agua" not in st.session_state: st.session_state.edit_agua = False

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

# --- Layout resultados ---
col1, col2 = st.columns(2)

# ============ Caudal de Agua ============
with col1:
    st.markdown("### 💧 Caudal de Agua")

    if st.session_state.edit_agua:
        nuevo = st.number_input("Modificar [m³/h]:", value=round(m3_per_h, 2), step=0.1, label_visibility="collapsed")
        cc1, cc2 = st.columns([1,1])
        with cc1:
            if st.button("Guardar"):
                denom = 42*3.785*0.06
                st.session_state.bpm = max(0.5, min(20.0, float(nuevo)/denom))
                st.session_state.edit_agua = False
                st.rerun()
        with cc2:
            if st.button("Cancelar"):
                st.session_state.edit_agua = False
                st.rerun()
    else:
        # Botón cuadrado igual que los de químico
        st.markdown('<div class="square-btn">', unsafe_allow_html=True)
        if st.button(f"{int(round(m3_per_h))}\n m³/h", key="btn_agua"):
            st.session_state.edit_agua = True
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ============ Caudal Químico ============
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
        """,
        unsafe_allow_html=True
    )
