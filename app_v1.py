import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("☀️ ILLARY - QORI SOLAR")
st.subheader("Tu Sol a tu Medida - Proyecto UNAJ Juliaca")
st.write("Proyecto: Full Power Julls APA | HSP 5.9 SENAMHI | EPIER - UNAJ")

equipos = {
    "Foco LED 9W": 9,
    "TV 60W": 60,
    "Laptop 65W": 65,
    "Celular 10W": 10,
    "Refrigeradora 100W": 100,
    "Bomba 500W": 500,
}

if "lista" not in st.session_state:
    st.session_state.lista = []

st.markdown("### Equipo")
equipo = st.selectbox("Equipo", list(equipos.keys()))
cant = st.number_input("Cantidad", 1, 20, 1)
horas = st.number_input("Horas", 1, 24, 5)

if st.button("Agregar"):
    w = equipos[equipo]
    st.session_state.lista.append({"Equipo": equipo, "Cant": cant, "Horas": horas, "W": w, "Wh/dia": cant * horas * w})

if st.session_state.lista:
    df = pd.DataFrame(st.session_state.lista)
    st.dataframe(df, use_container_width=True)

    total = df["Wh/dia"].sum()
    st.markdown("Consumo total")
    st.markdown(f"## {total:.0f} Wh/dia")

    hsp = 5.9
    panel = total / hsp * 1.35
    bateria = total / 12 * 2
    potencia_max = (df["W"] * df["Cant"]).sum()
    inversor = potencia_max * 1.25

    if total < 300:
        kit = "BASICO"
    elif total < 800:
        kit = "INTERMEDIO"
    else:
        kit = "COMPLETO"

    st.write(f"Panel: {panel:.0f}W")
    st.write(f"Bateria: {bateria:.0f}Ah")
    st.write(f"Inversor: {inversor:.0f}W")
    st.write(f"Kit: {kit}")

    fig, ax = plt.subplots()
    ax.pie(df["Wh/dia"], labels=df["Equipo"], autopct='%1.1f%%')
    st.pyplot(fig)
else:
    st.write("Elige un equipo y dale a Agregar")
