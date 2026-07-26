import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import pandas as pd

# ---------------------------------------
# CONFIGURACIÓN
# ---------------------------------------

st.set_page_config(
    page_title="Simulación del Campo Magnético",
    page_icon="🧲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------
# ESTILO
# ---------------------------------------

st.markdown("""
<style>

h1{
    color:#F8F9FA;
}

h2{
    color:#58A6FF;
}

[data-testid="stMetricValue"]{
    font-size:35px;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------
# TÍTULO
# ---------------------------------------

st.title("🧲 Simulación del Campo Magnético en un Solenoide")

st.markdown("""
Explora cómo la corriente, el número de espiras y la longitud afectan el campo magnético generado por un **solenoide ideal**.
""")

st.divider()

# ---------------------------------------
# BARRA LATERAL
# ---------------------------------------

st.sidebar.header("⚙️ Parámetros")

I = st.sidebar.slider(
    "Corriente I (A)",
    0.0,
    10.0,
    3.70,
    0.01
)

N = st.sidebar.slider(
    "Número de espiras N",
    10,
    2000,
    520,
    10
)

L = st.sidebar.slider(
    "Longitud L (m)",
    0.05,
    2.0,
    0.50,
    0.01
)

# ---------------------------------------
# CÁLCULOS
# ---------------------------------------

mu0 = 4*np.pi*1e-7

n = N/L

B = mu0*n*I

# ---------------------------------------
# PANEL LATERAL
# ---------------------------------------

st.sidebar.divider()

st.sidebar.info(f"""

### Información

**Permeabilidad del vacío (μ₀)**

4π × 10⁻⁷ T·m/A

---

**Densidad de espiras**

{n:.2f} espiras/m

---

**Modelo**

Solenoide ideal

""")

# ---------------------------------------
# PESTAÑAS
# ---------------------------------------

tab1, tab2, tab3, tab4 = st.tabs([
    "🧲 Visualización",
    "📈 Gráficas",
    "⚖️ Comparación",
    "✅ Validación"
])
