import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("☀️ ILLARI JULLS - CON CATÁLOGO")
st.subheader("Tu Sol a tu Medida - Juliaca / Puno")
st.write("Ahora sí puedes elegir, agregar y quitar lo que quieras.")

equipos = {
    "Foco LED 9W": 9,
    "TV 60W": 60,
    "Laptop 65W": 65,
    "Celular 10W": 10,
    "Refrigeradora 100W": 100,
    "Bomba 500W": 500,
}

if "lista2" not in st.session_state:
    st.session_state.lista2 = []

st.markdown("### 1️⃣ Elige tu equipo")
equipo = st.selectbox("Equipo", list(equipos.keys()))
cant = st.number_input("Cantidad", 1, 20, 1, key="cant2")
horas = st.number_input("Horas al día", 1, 24, 5, key="horas2")

c1, c2, c3 = st.columns(3)
with c1:
    if st.button("Agregar"):
        w = equipos[equipo]
        st.session_state.lista2.append({"Equipo": equipo, "Cant": cant, "Horas": horas, "W": w, "Wh/dia": cant * horas * w})
with c2:
    if st.button("Quitar último"):
        if st.session_state.lista2:
            st.session_state.lista2.pop()
with c3:
    if st.button("Borrar todo"):
        st.session_state.lista2 = []

if st.session_state.lista2:
    df = pd.DataFrame(st.session_state.lista2)
    st.dataframe(df, use_container_width=True)
    total = df["Wh/dia"].sum()
    st.markdown(f"### Consumo total: **{total:.0f} Wh/día**")

    hsp = 5.9
    panel_nec = total / hsp * 1.35
    bateria_nec = total / 12 * 2
    potencia_max = (df["W"] * df["Cant"]).sum()
    inversor_nec = potencia_max * 1.25

    st.markdown("### 2️⃣ Lo que necesitas")
    st.write(f"Panel necesario: {panel_nec:.0f}W")
    st.write(f"Batería necesaria: {bateria_nec:.0f}Ah")
    st.write(f"Inversor necesario: {inversor_nec:.0f}W")

    # CATALOGO
    st.markdown("### 3️⃣ Catálogo - Te recomendamos este")
    catalogo_panel = [100, 200, 340, 450, 550]
    catalogo_bat = [50, 100, 150, 200]
    catalogo_inv = [300, 500, 1000, 2000]

    panel_rec = [x for x in catalogo_panel if x >= panel_nec]
    panel_rec = panel_rec[0] if panel_rec else 550
    bat_rec = [x for x in catalogo_bat if x >= bateria_nec]
    bat_rec = bat_rec[0] if bat_rec else 200
    inv_rec = [x for x in catalogo_inv if x >= inversor_nec]
    inv_rec = inv_rec[0] if inv_rec else 2000

    st.success(f"✅ Panel recomendado: {panel_rec}W - S/ {panel_rec * 2} aprox.")
    st.success(f"✅ Batería recomendada: {bat_rec}Ah")
    st.success(f"✅ Inversor recomendado: {inv_rec}W")

    if total < 300:
        kit = "BASICO"
    elif total < 800:
        kit = "INTERMEDIO"
    else:
        kit = "COMPLETO"
    st.write(f"Kit: **{kit}**")

    fig, ax = plt.subplots()
    ax.pie(df["Wh/dia"], labels=df["Equipo"], autopct='%1.1f%%')
    st.pyplot(fig)
else:
    st.info("Todavía no hay nada. Elige un equipo arriba y dale a Agregar. Puedes poner solo focos, solo TV, lo que quieras.")
