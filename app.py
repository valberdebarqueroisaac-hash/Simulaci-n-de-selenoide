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
mostrar_campo = st.sidebar.checkbox(
    "Mostrar líneas de campo",
    value=True
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
# =========================================
# Color según la intensidad del campo
# =========================================

if B < 0.001:
    color_campo = "#1E90FF"      # Azul
    descripcion = "Campo débil"

elif B < 0.003:
    color_campo = "#00CC66"      # Verde
    descripcion = "Campo moderado"

elif B < 0.006:
    color_campo = "#FFD700"      # Amarillo
    descripcion = "Campo fuerte"

else:
    color_campo = "#FF3333"      # Rojo
    descripcion = "Campo muy fuerte"

fig = go.Figure()
        # Elegir el color según la intensidad del campo
if B < 0.001:
    color_solenoide = "#1E90FF"      # Azul
elif B < 0.003:
    color_solenoide = "#00CC66"      # Verde
elif B < 0.006:
    color_solenoide = "#FFD700"      # Amarillo
else:
    color_solenoide = "#FF3333"      # Rojo

fig.add_trace(
    go.Scatter3d(
        x=x,
        y=y,
        z=z,
        mode="lines",
        line=dict(
            color=color_campo,
            width=8
    )
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
# ===============================
# Núcleo del solenoide
# ===============================

for ang in np.linspace(0, 2*np.pi, 16):

    y_nucleo = 0.65 * np.cos(ang)
    z_nucleo = 0.65 * np.sin(ang)

    fig.add_trace(
        go.Scatter3d(
            x=[-longitud/2, longitud/2],
            y=[y_nucleo, y_nucleo],
            z=[z_nucleo, z_nucleo],
            mode="lines",
            line=dict(
                color="lightgray",
                width=2
            ),
            showlegend=False
        )
    )
# ===============================
# Flechas del campo magnético
# ===============================

for pos in np.linspace(-longitud/2 + 1, longitud/2 - 1, 8):

    fig.add_trace(
        go.Cone(
            x=[pos],
            y=[0],
            z=[0],
            u=[1],
            v=[0],
            w=[0],
            sizemode="absolute",
            sizeref=0.45,
            colorscale="Blues",
            showscale=False,
            anchor="tail",
            name="Campo"
        )
    )
# ==========================================
# Líneas del campo magnético
# ==========================================

if mostrar_campo:

    for radio in [2.2, 2.8, 3.4]:

        t = np.linspace(0, 2*np.pi, 200)

        # Lazo alrededor del solenoide
        x_campo = (longitud/2 + 0.3) * np.cos(t)

        y_campo = radio * np.sin(t)

        z_campo = np.zeros_like(t)

        fig.add_trace(
            go.Scatter3d(
                x=x_campo,
                y=y_campo,
                z=z_campo,
                mode="lines",
                line=dict(
                    color="deepskyblue",
                    width=3
                ),
                opacity=0.6,
                showlegend=False
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

        corriente = np.linspace(0, 10, 100)
        B_I = mu0 * (N / L) * corriente

        fig1 = plt.figure(figsize=(6,4))
        plt.plot(corriente, B_I, label="B vs I", linewidth=2)
        plt.scatter(I, B, color="red", s=70)
        plt.xlabel("Corriente (A)")
        plt.ylabel("Campo Magnético (T)")
        plt.grid(True)

        st.pyplot(fig1)

    # ==========================
    # B vs Espiras
    # ==========================
    with col2:

        espiras = np.linspace(10, 2000, 100)
        B_N = mu0 * (espiras / L) * I

        fig2 = plt.figure(figsize=(6,4))
        plt.plot(espiras, B_N, linewidth=2)
        plt.scatter(N, B, color="red", s=70)
        plt.xlabel("Número de espiras")
        plt.ylabel("Campo Magnético (T)")
        plt.grid(True)

        st.pyplot(fig2)

    st.divider()

    # ==========================
    # B vs Longitud
    # ==========================
    longitud = np.linspace(0.05, 2, 100)
    B_L = mu0 * (N / longitud) * I

    fig3 = plt.figure(figsize=(10,4))
    plt.plot(longitud, B_L, linewidth=2)
    plt.scatter(L, B, color="red", s=80)
    plt.xlabel("Longitud (m)")
    plt.ylabel("Campo Magnético (T)")
    plt.grid(True)

    st.pyplot(fig3)
# ==========================================
# PESTAÑA 3 - COMPARACIÓN
# ==========================================

with tab3:

    st.header("Comparación entre dos solenoides")

    colA, colB = st.columns(2)

    # -------------------------
    # SOLENOIDE A
    # -------------------------

    with colA:

        st.subheader("🧲 Solenoide A")

        IA = st.slider(
            "Corriente A (A)",
            0.0,
            10.0,
            I,
            0.1,
            key="IA"
        )

        NA = st.slider(
            "Espiras A",
            10,
            2000,
            N,
            10,
            key="NA"
        )

        LA = st.slider(
            "Longitud A (m)",
            0.05,
            2.0,
            L,
            0.01,
            key="LA"
        )

        BA = mu0 * (NA / LA) * IA

        st.metric(
            "Campo Magnético",
            f"{BA:.5e} T"
        )

    # -------------------------
    # SOLENOIDE B
    # -------------------------

    with colB:

        st.subheader("🧲 Solenoide B")

        IB = st.slider(
            "Corriente B (A)",
            0.0,
            10.0,
            5.0,
            0.1,
            key="IB"
        )

        NB = st.slider(
            "Espiras B",
            10,
            2000,
            1000,
            10,
            key="NB"
        )

        LB = st.slider(
            "Longitud B (m)",
            0.05,
            2.0,
            0.80,
            0.01,
            key="LB"
        )

        BB = mu0 * (NB / LB) * IB

        st.metric(
            "Campo Magnético",
            f"{BB:.5e} T"
        )
        st.divider()

        if BA > BB:

            diferencia = ((BA - BB) / BB) * 100 if BB != 0 else 0

            st.success(
                f"✅ El Solenoide A genera un campo magnético aproximadamente {diferencia:.2f}% mayor."
            )

        elif BB > BA:

            diferencia = ((BB - BA) / BA) * 100 if BA != 0 else 0

            st.success(
                f"✅ El Solenoide B genera un campo magnético aproximadamente {diferencia:.2f}% mayor."
            )

        else:

            st.info("Ambos solenoides generan el mismo campo magnético.")
# ==========================================
# PESTAÑA 4 - VALIDACIÓN
# ==========================================

with tab4:

    st.header("Validación del modelo físico")

    st.markdown("""
Esta sección verifica si la simulación cumple el comportamiento esperado para un **solenoide ideal**.
""")

    st.divider()

    # -----------------------------
    # Validación 1
    # -----------------------------

    st.subheader("1. Proporcionalidad entre B e I")

    I2 = I * 2
    B2 = mu0 * n * I2

    if I > 0:

        razon = B2 / B

        st.write(f"Si la corriente aumenta de **{I:.2f} A** a **{I2:.2f} A**, el campo cambia de:")

        st.write(f"- B₁ = {B:.5e} T")
        st.write(f"- B₂ = {B2:.5e} T")

        st.success(f"Relación B₂/B₁ = {razon:.2f}")

        if abs(razon - 2) < 0.01:
            st.success("✅ Se confirma que B es directamente proporcional a la corriente.")
        else:
            st.error("❌ La proporcionalidad no coincide con el modelo ideal.")

    else:

        st.warning("La corriente es cero; no es posible validar esta relación.")

    st.divider()

    # -----------------------------
    # Validación 2
    # -----------------------------

    st.subheader("2. Efecto del número de espiras")

    N2 = N * 2

    n2 = N2 / L

    B_N = mu0 * n2 * I

    razonN = B_N / B if B != 0 else 0

    st.write(f"Duplicando las espiras ({N} → {N2})")

    st.write(f"B = {B_N:.5e} T")

    st.success(f"Relación = {razonN:.2f}")

    st.divider()

    # -----------------------------
    # Validación 3
    # -----------------------------

    st.subheader("3. Efecto de la longitud")

    L2 = L * 2

    n3 = N / L2

    B_L = mu0 * n3 * I

    razonL = B_L / B if B != 0 else 0

    st.write(f"Duplicando la longitud ({L:.2f} m → {L2:.2f} m)")

    st.write(f"B = {B_L:.5e} T")

    st.success(f"Relación = {razonL:.2f}")

    st.divider()

    st.subheader("Conclusión")

    st.info("""
✅ El comportamiento obtenido coincide con la ecuación del solenoide ideal.

Se verifica que:

• El campo magnético aumenta al incrementar la corriente.

• El campo magnético aumenta al incrementar el número de espiras.

• El campo magnético disminuye cuando aumenta la longitud del solenoide.

Estos resultados son coherentes con el modelo teórico:
B = μ₀·(N/L)·I
""")
