import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

# Configuración de la página
st.set_page_config(
    page_title="Simulación del Campo Magnético",
    page_icon="🧲",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🧲 Simulación del Campo Magnético en un Solenoide")

st.write("""
Esta simulación utiliza el modelo ideal del solenoide:

B = μ₀ · (N/L) · I

donde:
- B = Campo magnético (T)
- μ₀ = Permeabilidad del vacío
- N = Número de espiras
- L = Longitud del solenoide (m)
- I = Corriente (A)
""")

# Constante
mu0 = 4 * np.pi * 1e-7

# Parámetros
st.sidebar.header("Parámetros")

I = st.sidebar.slider("Corriente (A)", 0.0, 10.0, 2.0, 0.1)
N = st.sidebar.slider("Número de espiras", 10, 1000, 200, 10)
L = st.sidebar.slider("Longitud (m)", 0.05, 2.0, 0.50, 0.01)

# Cálculo
n = N / L
B = mu0 * n * I
tab1, tab2, tab3, tab4 = st.tabs([
    "🧲 Visualización",
    "📈 Gráficas",
    "⚖️ Comparación",
    "✅ Validación"
])

with tab1:

    st.subheader("Resultados")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Campo Magnético (T)", f"{B:.6e}")

    with col2:
        st.metric("Densidad de espiras", f"{n:.2f} espiras/m")
            st.subheader("Visualización del Solenoide")

    fig, ax = plt.subplots(figsize=(12,3))

    vueltas = int(N/20)

    for i in range(vueltas):
        x = i
        circ = Circle((x,0),0.45,fill=False,linewidth=2)
        ax.add_patch(circ)

    ax.set_xlim(-1,vueltas+1)
    ax.set_ylim(-1,1)

    ax.set_aspect('equal')
    ax.axis("off")

    st.pyplot(fig)
