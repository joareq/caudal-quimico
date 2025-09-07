import streamlit as st

# =====================  Config  =====================
st.set_page_config(page_title="Cálculo caudal químico", layout="wide")

# =====================  Estilos  =====================
st.markdown("""
<style>
/* ---------- cards de químicos ---------- */
.card {
  width: 120px; height: 120px;
  display:flex; flex-direction:column; align-items:center; justify-content:center;
  border:1px solid #ccc; border-radius:8px;
  font-weight:700; margin:6px; background:transparent; color:#fff;
}

/* número + unidad en cards */
.card .value { font-size:28px; line-height:1; }
.card .unit  { font-size:14px; margin-top:6px; }

/* ---------- botón oculto que usamos sólo para detectar click ---------- */
button[aria-label="agua_card"]{
  position:absolute; left:-99999px; width:0; height:0; padding:0; margin:0; border:0; opacity:0;
}

/* ---------- modo edición de Caudal de Agua: number_input “con look de card” ---------- */
div[data-testid="stNumberInput"].agua-editor{
  width: 120px; height: 120px;
  border:1px solid #ccc; border-radius:8px;
  display:flex; align-items:center; justify-content:center;
  background:transparent; color:#fff; margin:6px;
}
div[data-testid="stNumberInput"].agua-editor label{display:none;}
div[data-testid="stNumberInput"].agua-editor input{
  text-align:center; font-size:28px; font-weight:700;
  background:transparent; color:#fff; border:0; outline:0; width:90%;
}
/* unidad dentro del mismo cuadrado (pseudo-elemento) */
div[data-testid="stNumberInput"].agua-editor:after{
  content: "m³/h";
  position:absolute; bottom:12px; left:0; right:0;
  text-align:center; font-size:14px; font-weight:700; color:#ddd;
}

/* botones de Guardar/Cancelar más compactos */
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
    # editor con look de card (mismo tamaño)
    # usamos key para leer el valor y clase CSS para “parecer” la card
    num = st.number_input(" ", value=float(round(m3_per_h, 2)),
                          step=0.1, label_visibility="collapsed", key="agua_val",
                          format="%.2f")
    # forzamos la clase CSS de este number_input
    st.markdown("""
    <script>
      const nodes = window.parent.document.querySelectorAll("div[data-testid='stNumberInput']");
      if(nodes && nodes.length){ nodes[nodes.length-1].classList.add("agua-editor"); }
    </script>
    """, unsafe_allow_html=True)

    a1, a2 = st.columns(2, gap="small")
    with a1:
      if st.button("✔ Guardar"):
        try:
          val = float(st.session_state.agua_val)
          denom = 42*3.785*0.06
          st.session_state.bpm = max(0.5, min(20.0, val/denom))
        except:  # si no es número válido, no cambiamos
          pass
        st.session_state.edit_agua = False
        st.rerun()
    with a2:
      if st.button("✖ Cancelar"):
        st.session_state.edit_agua = False
        st.rerun()

  else:
    # botón oculto que usaremos para cambiar a modo edición
    st.button("", key="agua_card")
    # tarjeta visible (idéntica a químico) que dispara el click del botón oculto
    st.markdown(
      f"""
      <div class="card"
           onclick="window.parent.document.querySelector('button[aria-label=agua_card]').click();">
        <div class="value">{int(round(m3_per_h))}</div>
        <div class="unit">m³/h</div>
      </div>
      """,
      unsafe_allow_html=True
    )

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
