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

# --- Diseño principal en dos columnas ---
col_sliders, col_resultados = st.columns([1, 1])

with col_sliders:
    gpt = st.slider("Seleccione GPT (galones por mil)", 0.0, 10.0, 1.5, 0.1)
    bpm = st.slider("Seleccione BPM (barriles por minuto)", 0.5, 20.0, 5.0, 0.1)

# --- Cálculos ---
gal_per_min = bpm * 42
l_per_min = gal_per_min * 3.785
m3_per_h = l_per_min * 0.06

q_quimico_gal_min = (gpt / 1000) * gal_per_min
q_quimico_l_min = q_quimico_gal_min * 3.785
q_quimico_l_h = q_quimico_l_min * 60

with col_resultados:
    # --- Caudal de Agua ---
    st.markdown("### 💧 Caudal de Agua")
    st.markdown(
        f"""
        <div style="text-align:center; border:1px solid #555; border-radius:8px;
                    padding:20px; width:120px; margin:auto;">
            <div style="font-size:28px; font-weight:bold;">{m3_per_h:.0f}</div>
            <div style="font-size:14px;">m³/h</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # --- Caudal Químico ---
    st.markdown("### <img src='https://raw.githubusercontent.com/joareq/caudal-quimico/main/icono_skid.png' width='25'> Caudal Químico", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    c1.markdown(
        f"""
        <div style="text-align:center; border:1px solid #555; border-radius:8px;
                    padding:20px;">
            <div style="font-size:28px; font-weight:bold;">{q_quimico_gal_min:.2f}</div>
            <div style="font-size:14px;">gal/min</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    c2.markdown(
        f"""
        <div style="text-align:center; border:1px solid #555; border-radius:8px;
                    padding:20px;">
            <div style="font-size:28px; font-weight:bold;">{q_quimico_l_min:.2f}</div>
            <div style="font-size:14px;">l/min</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    c3.markdown(
        f"""
        <div style="text-align:center; border:1px solid #555; border-radius:8px;
                    padding:20px;">
            <div style="font-size:28px; font-weight:bold;">{q_quimico_l_h:.0f}</div>
            <div style="font-size:14px;">l/h</div>
        </div>
        """,
        unsafe_allow_html=True
    )
