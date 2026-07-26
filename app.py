import streamlit as st
import numpy as np

# Configuración de la página
st.set_page_config(page_title="Simulación de Solenoide", layout="wide")

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

st.subheader("Resultados")

col1, col2 = st.columns(2)

with col1:
    st.metric("Campo magnético (T)", f"{B:.6e}")

with col2:
    st.metric("Densidad de espiras (espiras/m)", f"{n:.2f}")

st.success("Mueve los deslizadores de la izquierda para observar cómo cambia el campo magnético.")
