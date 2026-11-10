import streamlit as st
import pandas as pd

st.title("☀️ ILLARI JULLS")
st.subheader("Tu Sol a tu Medida - Juliaca / Puno")
st.write("Calculamos tu kit exacto según lo que quieres prender.")

st.markdown("### 1️⃣ ¿Qué quieres prender?")

if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame([
        {"Equipo": "Foco LED", "Potencia (W)": 9, "Horas/día": 5, "Cantidad": 4},
        {"Equipo": "TV", "Potencia (W)": 60, "Horas/día": 4, "Cantidad": 1},
        {"Equipo": "Cargador celular", "Potencia (W)": 10, "Horas/día": 3, "Cantidad": 3},
    ])

df = st.data_editor(st.session_state.df, num_rows="dynamic", use_container_width=True)
st.session_state.df = df

df["Energía (Wh/día)"] = df["Potencia (W)"] * df["Horas/día"] * df["Cantidad"]
total_wh = df["Energía (Wh/día)"].sum()

st.markdown(f"### Consumo total: **{total_wh:.0f} Wh/día**")

hsp = st.slider("Horas de sol en Juliaca (HSP)", 4.0, 6.5, 5.9)
potencia_panel = total_wh / hsp

st.success(f"Necesitas un panel de **{potencia_panel:.0f} W**")
st.info("Este es el cálculo exacto, sin catálogo comercial. Es el Prototipo 1 - el original.")

st.markdown("### Tabla de consumo")
st.dataframe(df, use_container_width=True)
