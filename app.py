import streamlit as st

st.set_page_config(page_title="Cálculo caudal químico", layout="wide")

# --- CSS ---
st.markdown("""
<style>
.card {
  width: 120px; height: 120px;
  display:flex; flex-direction:column; align-items:center; justify-content:center;
  border:1px solid #ccc; border-radius:8px;
  font-weight:bold; margin:6px; background:transparent;
  cursor:pointer;
}
.card .value { font-size:28px; }
.card .unit  { font-size:14px; margin-top:6px; }
.card input {
  text-align:center;
  font-size:28px;
  font-weight:bold;
  width:90%;
  border:none;
  background:transparent;
  color:white;
}
</style>
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

# --- Layout ---
col1, col2 = st.columns(2)

# Caudal Agua
with col1:
    st.markdown("### 💧 Caudal de Agua")

    if st.session_state.edit_agua:
        nuevo = st.text_input(
            " ", value=str(int(round(m3_per_h))),
            label_visibility="collapsed", key="agua_input"
        )

        st.markdown(
            f"""
            <div class="card">
                <input type="number" value="{nuevo}" id="agua_val">
                <div class="unit">m³/h</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button("✔ Guardar"):
            try:
                val = float(st.session_state.agua_input)
                denom = 42*3.785*0.06
                st.session_state.bpm = max(0.5, min(20.0, val/denom))
            except:
                pass
            st.session_state.edit_agua = False
            st.rerun()
        if st.button("✖ Cancelar"):
            st.session_state.edit_agua = False
            st.rerun()

    else:
        if st.button("", key="agua_card", help="Haz clic para editar"):
            st.session_state.edit_agua = True
            st.rerun()
        st.markdown(
            f"""
            <div class="card" onclick="window.parent.document.querySelector('button[kind=primary][data-testid=stButton][aria-label=agua_card]').click();">
                <div class="value">{int(round(m3_per_h))}</div>
                <div class="unit">m³/h</div>
            </div>
            """,
            unsafe_allow_html=True
        )

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
        """,
        unsafe_allow_html=True
    )
