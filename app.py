import streamlit as st

# =====================  Config  =====================
st.set_page_config(page_title="Cálculo caudal químico", layout="wide")

# =====================  Estilos  =====================
st.markdown("""
<style>
/* ---------- cards ---------- */
.card {
  width: 120px; height: 120px;
  display:flex; flex-direction:column; align-items:center; justify-content:center;
  border:1px solid #ccc; border-radius:8px;
  font-weight:700; margin:6px; background:transparent; color:#fff;
}
.card .value { font-size:28px; line-height:1; }
.card .unit  { font-size:14px; margin-top:6px; }

/* ---------- editor (number_input) con look de card ---------- */
div[data-testid="stNumberInput"].agua-editor{
  width: 120px; height: 120px;
  border:1px solid #ccc; border-radius:8px;
  display:flex; align-items:center; justify-content:center;
  background:transparent; color:#fff; margin:6px; position:relative;
}
div[data-testid="stNumberInput"].agua-editor label{display:none;}
div[data-testid="stNumberInput"].agua-editor input{
  text-align:center; font-size:28px; font-weight:700;
  background:transparent; color:#fff; border:0; outline:0; width:90%;
}
div[data-testid="stNumberInput"].agua-editor:after{
  content: "m³/h";
  position:absolute; bottom:12px; left:0; right:0;
  text-align:center; font-size:14px; font-weight:700; color:#ddd;
}

/* botones guardar/cancelar compactos */
div.agua-actions > div > button{ width:100%; }
</style>
""", unsafe_allow_html=True)

# =====================  Estado  =====================
if "bpm" not in st.session_state: st.session_state.bpm = 5.0
if "gpt" not in st.session_state: st.session_state.gpt = 1.5
if "edit_agua" not in st.session_state: st.session_state.edit_agua = False

# =====================  Header  =====================
st.markdown("""
<div style="text-align:center;">
  <img src="https://raw.githubusercontent.com/joareq/caudal-quimico/main/logo.png" width="250">
  <h1 style="margin-top:10px;">CALCULO CAUDAL QUIMICO</h1>
</div>
""", unsafe_allow_html=True)

# =====================  Sliders  =====================
csl1, csl2 = st.columns(2)
with csl1:
  st.session_state.gpt = st.slider("Seleccione GPT (galones por mil)", 0.0, 10.0, st.session_state.gpt, 0.1)
with csl2:
  st.session_state.bpm = st.slider("Seleccione BPM (barriles por minuto)", 0.5, 20.0, st.session_state.bpm, 0.1)

# =====================  Cálculos  =====================
gal_per_min = st.session_state.bpm * 42
l_per_min   = gal_per_min * 3.785
m3_per_h    = l_per_min * 0.06

q_quimico_gal_min = (st.session_state.gpt / 1000) * gal_per_min
q_quimico_l_min   = q_quimico_gal_min * 3.785
q_quimico_l_h     = q_quimico_l_min * 60

# =====================  Layout resultados  =====================
col1, col2 = st.columns(2)

# ---------- Caudal de Agua ----------
with col1:
  st.markdown("### 💧 Caudal de Agua")

  if st.session_state.edit_agua:
    # editor “dentro” del cuadrado (mismo look)
    val = st.number_input(" ", value=float(round(m3_per_h, 2)),
                          step=0.1, format="%.2f",
                          label_visibility="collapsed", key="agua_val")
    # forzamos la clase CSS para que se vea como card
    st.markdown("""
    <script>
      const nodes = window.parent.document.querySelectorAll("div[data-testid='stNumberInput']");
      if(nodes && nodes.length){ nodes[nodes.length-1].classList.add("agua-editor"); }
    </script>
    """, unsafe_allow_html=True)

    a1, a2 = st.columns(2)
    with a1:
      if st.button("✔ Guardar"):
        try:
          val = float(st.session_state.agua_val)
          denom = 42*3.785*0.06
          st.session_state.bpm = max(0.5, min(20.0, val/denom))
        except:
          pass
        st.session_state.edit_agua = False
        st.rerun()
    with a2:
      if st.button("✖ Cancelar"):
        st.session_state.edit_agua = False
        st.rerun()

  else:
    # Botón “oculto” con texto AGUA_EDIT para poder localizarlo desde JS y esconderlo
    trig = st.button("AGUA_EDIT", key="agua_trigger_btn")
    # Ocultar ese botón y asignarle un id para click programático
    st.markdown("""
    <script>
      const btns = Array.from(window.parent.document.querySelectorAll('button'));
      const target = btns.find(b => b.innerText.trim() === 'AGUA_EDIT');
      if (target){
        target.id = 'aguaTriggerBTN';
        target.style.display = 'none';               // lo ocultamos del layout
      }
    </script>
    """, unsafe_allow_html=True)

    # Tarjeta visible; al hacer click llama al botón oculto
    st.markdown(
      f"""
      <div class="card" onclick="const t=window.parent.document.getElementById('aguaTriggerBTN'); if(t) t.click();">
        <div class="value">{int(round(m3_per_h))}</div>
        <div class="unit">m³/h</div>
      </div>
      """,
      unsafe_allow_html=True
    )

    # si el botón oculto fue “clickeado” activamos edición
    if trig:
      st.session_state.edit_agua = True
      st.rerun()

# ---------- Caudal Químico ----------
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
