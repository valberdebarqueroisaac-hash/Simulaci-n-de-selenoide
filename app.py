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
# ==========================================
# PESTAÑA 1
# ==========================================

with tab1:

    st.subheader("Visualización del Solenoide")

    col1, col2 = st.columns([3,1])

    with col1:

        vueltas = max(5, int(N/20))

        theta = np.linspace(
            0,
            vueltas*2*np.pi,
            800
        )

        radio = 1

        longitud = L*8

        x = np.linspace(
            -longitud/2,
            longitud/2,
            len(theta)
        )

        y = radio*np.cos(theta)

        z = radio*np.sin(theta)

        fig = go.Figure()

        fig.add_trace(
            go.Scatter3d(
                x=x,
                y=y,
                z=z,
                mode="lines",
                line=dict(
                    color="orange",
                    width=8
                ),
                name="Solenoide"
            )
        )
        fig.update_layout(

            height=650,

            scene=dict(

                xaxis_visible=False,
                yaxis_visible=False,
                zaxis_visible=False,

                bgcolor="black",

                camera=dict(
                    eye=dict(
                        x=1.8,
                        y=1.5,
                        z=1
                    )
                )

            ),

            margin=dict(
                l=0,
                r=0,
                b=0,
                t=0
            )

        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )
# ==========================================
# PESTAÑA 2 - GRÁFICAS
# ==========================================

with tab2:

    st.header("Análisis Gráfico")

    col1, col2 = st.columns(2)

    # ==========================
    # B vs Corriente
    # ==========================

    with col1:

        corriente = np.linspace(0,10,100)

        B_I = mu0*(N/L)*corriente

        fig1 = plt.figure(figsize=(6,4))

        plt.plot(corriente,B_I,label="B vs I",linewidth=2)

        plt.scatter(I,B,color="red",s=70)

        plt.xlabel("Corriente (A)")
        plt.ylabel("Campo Magnético (T)")
        plt.grid(True)

        st.pyplot(fig1)

    # ==========================
    # B vs Espiras
    # ==========================

    with col2:

     st.metric(
        "Campo Magnético",
        f"{B:.5e} T"
    )

     st.metric(
        "Densidad",
        f"{n:.2f}"
    )

     st.metric(
        "Espiras",
        N
    )

     st.metric(
        "Corriente",
        f"{I:.2f} A"
    )

        espiras = np.linspace(10,2000,100)

        B_N = mu0*(espiras/L)*I

        fig2 = plt.figure(figsize=(6,4))

        plt.plot(espiras,B_N,linewidth=2)

        plt.scatter(N,B,color="red",s=70)

        plt.xlabel("Número de espiras")

        plt.ylabel("Campo Magnético (T)")

        plt.grid(True)

        st.pyplot(fig2)

    st.divider()

    # ==========================
    # B vs Longitud
    # ==========================

    longitud = np.linspace(0.05,2,100)

    B_L = mu0*(N/longitud)*I

    fig3 = plt.figure(figsize=(10,4))

    plt.plot(longitud,B_L,linewidth=2)

    plt.scatter(L,B,color="red",s=80)

    plt.xlabel("Longitud (m)")

    plt.ylabel("Campo Magnético (T)")

    plt.grid(True)

    st.pyplot(fig3)
# ==========================================
# Líneas del campo magnético
# ==========================================

intensidad = max(4, int(B * 800000))

for r in np.linspace(1.8, 3.2, 5):

    theta2 = np.linspace(0, 2*np.pi, 120)

    x2 = np.linspace(-longitud/2, longitud/2, 120)

    y2 = r*np.cos(theta2)

    z2 = r*np.sin(theta2)

    fig.add_trace(

        go.Scatter3d(

            x=x2,
            y=y2,
            z=z2,

            mode="lines",

            line=dict(

                color="cyan",

                width=intensidad

            ),

            opacity=0.35,

            showlegend=False

        )

    )
with col2:

st.divider()

st.subheader("Intensidad del campo")

if B < 0.001:
    st.info("🟦 Campo magnético débil")
elif B < 0.003:
    st.success("🟩 Campo magnético medio")
elif B < 0.006:
    st.warning("🟨 Campo magnético fuerte")
else:
    st.error("🟥 Campo magnético muy intenso")
