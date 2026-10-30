import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="ILLARY - UNAJ", page_icon="☀️", layout="wide")
st.title("☀️ ILLARY - QORI SOLAR")
st.subheader("Tu Sol a tu Medida - Proyecto UNAJ Juliaca")
st.caption("Proyecto: Full Power Julls APA | HSP 5.9 SENAMHI | EPIER - UNAJ")

equipos_db = {
    "Foco LED 9W": {"w":9},
    "TV 60W": {"w":60},
    "Laptop 65W": {"w":65},
    "Celular 10W": {"w":10},
    "Refrigeradora 100W": {"w":100},
    "Bomba 500W": {"w":500},
}

HSP = st.sidebar.slider("HSP tu zona SENAMHI", 4.5, 6.5, 5.9, 0.1)
st.sidebar.info("Juliaca 5.9 - Dato SENAMHI")

if 'lista' not in st.session_state: st.session_state.lista = []

with st.form("agregar", clear_on_submit=True):
    col1, col2, col3 = st.columns(3)
    with col1: equipo = st.selectbox("Equipo", list(equipos_db.keys()))
    with col2: horas = st.number_input("Horas/dia", 1, 24, 5)
    with col3: cant = st.number_input("Cantidad", 1, 10, 1)
    agregar = st.form_submit_button("Agregar")
    if agregar:
        st.session_state.lista.append((equipo, horas, cant))

if st.session_state.lista:
    energia_total = 0
    pot_sim = 0
    datos = []
    for eq, h, c in st.session_state.lista:
        w = equipos_db[eq]["w"]
        e = w * h * c
        datos.append([eq, c, h, w, e])
        energia_total += e
        pot_sim += w * c

    df = pd.DataFrame(datos, columns=["Equipo", "Cant", "Horas", "W", "Wh/dia"])
    st.table(df)

    e_ajust = energia_total / 0.75
    panel_w = e_ajust / HSP
    bat_ah = energia_total * 1 / (12 * 0.5)
    inv_w = pot_sim * 1.25

    if energia_total < 500: kit = "BASICO"; costo = 1200; tienda = 1800
    elif energia_total < 1500: kit = "MEDIO"; costo = 2200; tienda = 2800
    else: kit = "DOMICILIARIO"; costo = 6500; tienda = 9000

    col_a, col_b = st.columns(2)
    with col_a:
        st.metric("Consumo total", f"{energia_total} Wh/dia")
        st.write(f"Panel: {panel_w:.0f}W")
        st.write(f"Bateria: {bat_ah:.0f}Ah")
        st.write(f"Inversor: {inv_w:.0f}W")
        st.write(f"Kit: {kit}")
    with col_b:
        fig, ax = plt.subplots()
        ax.pie(df["Wh/dia"], labels=df["Equipo"], autopct='%1.1f%%')
        st.pyplot(fig)
        st.success(f"Ahorro vs tienda: S/ {tienda - costo}")

    if st.button("Limpiar"):
        st.session_state.lista = []
        st.rerun()
else:
    st.info("Agrega equipos. Ej: 4 focos + TV + Cel = 450 Wh Caso Caracoto")
