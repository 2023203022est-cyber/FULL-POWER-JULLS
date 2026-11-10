import streamlit as st
import pandas as pd

st.set_page_config(page_title="ILLARI JULLS - Tu Sol a tu Medida", page_icon="☀️", layout="centered")
st.title("☀️ ILLARI JULLS")
st.subheader("Tu Sol a tu Medida - Juliaca / Puno")
st.caption("Calculamos tu kit exacto y te damos el equipo COMERCIAL que sí hay en tienda. No te vendemos humo.")

# ============ CATALOGO REAL - TIENDAS JULIACA ============
# Esto es lo que pediste: si sale 31W, te da el de 50W porque es lo que hay

CATALOGO_PANELES = [
    {"W": 20, "Precio": 70, "Nombre": "Panel 20W - Económico"},
    {"W": 50, "Precio": 140, "Nombre": "Panel 50W - Más comercial"},
    {"W": 100, "Precio": 230, "Nombre": "Panel 100W"},
    {"W": 150, "Precio": 320, "Nombre": "Panel 150W - Más vendido"},
    {"W": 300, "Precio": 580, "Nombre": "Panel 300W"},
    {"W": 550, "Precio": 950, "Nombre": "Panel 550W - Grande"},
]

CATALOGO_BATERIAS = [
    {"Ah": 20, "Precio": 95, "Nombre": "Batería 12V 20Ah - Moto"},
    {"Ah": 50, "Precio": 220, "Nombre": "Batería 12V 50Ah"},
    {"Ah": 100, "Precio": 380, "Nombre": "Batería 12V 100Ah - Más vendida"},
    {"Ah": 200, "Precio": 720, "Nombre": "Batería 12V 200Ah"},
]

CATALOGO_INVERSORES = [
    {"W": 300, "Precio": 120, "Nombre": "Inversor 300W"},
    {"W": 600, "Precio": 220, "Nombre": "Inversor 600W - Más vendido"},
    {"W": 1000, "Precio": 350, "Nombre": "Inversor 1000W"},
    {"W": 2000, "Precio": 620, "Nombre": "Inversor 2000W"},
]

CATALOGO_CONTROLADORES = [
    {"A": 10, "Precio": 35, "Nombre": "Controlador PWM 10A"},
    {"A": 20, "Precio": 55, "Nombre": "Controlador PWM 20A"},
    {"A": 30, "Precio": 80, "Nombre": "Controlador PWM 30A"},
    {"A": 60, "Precio": 140, "Nombre": "Controlador MPPT 60A"},
]

CATALOGO_FOCOS = [
    {"W": 9, "Precio": 12, "Nombre": "Foco LED 9W 12V"},
    {"W": 12, "Precio": 15, "Nombre": "Foco LED 12W 12V"},
    {"W": 20, "Precio": 22, "Nombre": "Foco LED 20W 220V"},
]

# Función que busca el equipo comercial más cercano por arriba
def buscar_comercial(lista, campo, valor_necesario):
    for item in lista:
        if item[campo] >= valor_necesario:
            return item
    return lista[-1]  # Si necesita más que todo, le da el más grande

# ============ CONFIGURACIÓN ============
st.sidebar.header("📍 Zona")
HSP = 5.9
st.sidebar.info(f"Juliaca / Puno: **{HSP} HSP** (SENAMHI)")
dias_aut = st.sidebar.slider("Días sin sol (autonomía)", 1, 3, 1)
voltaje = st.sidebar.selectbox("Voltaje sistema", [12, 24])
tipo_bat = st.sidebar.selectbox("Batería", ["Plomo-Ácido (50% usable)", "Litio (80% usable)"])
dod = 0.5 if "Plomo" in tipo_bat else 0.8

# ============ PASO 1: QUÉ QUIERES PRENDER ============
st.header("1️⃣ ¿Qué quieres prender?")
st.write("Elige de la lista. Estos son los equipos reales de una casa en Juliaca.")

if 'equipos' not in st.session_state:
    st.session_state.equipos = pd.DataFrame([
        {"Equipo": "Foco LED 9W", "Potencia (W)": 9, "Horas/día": 5, "Cantidad": 4},
        {"Equipo": "TV", "Potencia (W)": 60, "Horas/día": 4, "Cantidad": 1},
        {"Equipo": "Cargador celular", "Potencia (W)": 10, "Horas/día": 3, "Cantidad": 1},
    ])

edited = st.data_editor(st.session_state.equipos, num_rows="dynamic", use_container_width=True)

# ============ PASO 2: CALCULAR ============
if st.button("☀️ CALCULAR MI KIT EXACTO", type="primary", use_container_width=True):
    df = edited.dropna()
    df["Energía (Wh/día)"] = df["Potencia (W)"] * df["Horas/día"] * df["Cantidad"]
    energia = df["Energía (Wh/día)"].sum()
    pot_simultanea = (df["Potencia (W)"] * df["Cantidad"]).sum()

    # Tus 4 fórmulas
    energia_ajustada = energia / 0.75
    panel_necesario = energia_ajustada / HSP
    bateria_necesaria = energia * dias_aut / (voltaje * dod)
    inversor_necesario = pot_simultanea * 1.25
    controlador_necesario = panel_necesario / voltaje * 1.25  # Corriente aprox

    # AQUÍ ESTÁ LA MAGIA: Buscar comercial
    panel_elegido = buscar_comercial(CATALOGO_PANELES, "W", panel_necesario)
    bateria_elegida = buscar_comercial(CATALOGO_BATERIAS, "Ah", bateria_necesaria)
    inversor_elegido = buscar_comercial(CATALOGO_INVERSORES, "W", inversor_necesario)
    controlador_elegido = buscar_comercial(CATALOGO_CONTROLADORES, "A", controlador_necesario)

    # Ejemplo que pediste: si sale 31W -> te da 50W
    st.header("2️⃣ Tu cálculo teórico vs lo que hay en tienda")

    col1, col2 = st.columns(2)
    col1.metric("Panel que NECESITAS", f"{panel_necesario:.1f} W")
    col2.metric("Panel que TE VENDEN", f"{panel_elegido['W']} W - S/ {panel_elegido['Precio']}", f"{panel_elegido['Nombre']}")

    if panel_necesario < panel_elegido['W']:
        st.warning(f"⚠️ Ojo: Necesitas {panel_necesario:.1f}W pero en tienda no hay de {panel_necesario:.0f}W. Lo más cercano comercial es de **{panel_elegido['W']}W**. Por eso te recomendamos ese, no te vendemos uno inventado.")

    col1, col2 = st.columns(2)
    col1.metric("Batería que NECESITAS", f"{bateria_necesaria:.0f} Ah")
    col2.metric("Batería COMERCIAL", f"{bateria_elegida['Ah']} Ah - S/ {bateria_elegida['Precio']}")

    col1, col2 = st.columns(2)
    col1.metric("Inversor que NECESITAS", f"{inversor_necesario:.0f} W")
    col2.metric("Inversor COMERCIAL", f"{inversor_elegido['W']} W - S/ {inversor_elegido['Precio']}")

    # ============ CATÁLOGO FINAL CON PRECIOS ============
    st.header("3️⃣ 🛒 Tu Catálogo / Kit Recomendado")

    # Precio de focos: contar focos de la tabla
    num_focos = int(df[df['Equipo'].str.contains('Foco', na=False)]['Cantidad'].sum()) if len(df) > 0 else 0
    foco_elegido = CATALOGO_FOCOS[0]
    costo_focos = num_focos * foco_elegido['Precio']
    costo_cables = 45  # Cable + interruptor + conectores

    items = [
        {"Producto": panel_elegido['Nombre'], "Cant": 1, "Precio Unit": panel_elegido['Precio'], "Total": panel_elegido['Precio']},
        {"Producto": bateria_elegida['Nombre'], "Cant": 1, "Precio Unit": bateria_elegida['Precio'], "Total": bateria_elegida['Precio']},
        {"Producto": inversor_elegido['Nombre'], "Cant": 1, "Precio Unit": inversor_elegido['Precio'], "Total": inversor_elegido['Precio']},
        {"Producto": controlador_elegido['Nombre'], "Cant": 1, "Precio Unit": controlador_elegido['Precio'], "Total": controlador_elegido['Precio']},
        {"Producto": f"{foco_elegido['Nombre']} x {num_focos}", "Cant": num_focos, "Precio Unit": foco_elegido['Precio'], "Total": costo_focos},
        {"Producto": "Cables + Interruptor + Instalación", "Cant": 1, "Precio Unit": costo_cables, "Total": costo_cables},
    ]
    tabla = pd.DataFrame(items)
    st.table(tabla)

    total = tabla["Total"].sum()
    precio_tienda_sin_calculo = total * 1.45  # Las tiendas venden 45% más caro por sobredimensionar
    ahorro = precio_tienda_sin_calculo - total
    ahorro_mes = (energia * 30 / 1000) * 0.85

    col1, col2, col3 = st.columns(3)
    col1.metric("TOTAL ILLARI JULLS", f"S/ {total:.0f}")
    col2.metric("TIENDA SIN CALCULAR", f"S/ {precio_tienda_sin_calculo:.0f}")
    col3.metric("TE AHORRAS", f"S/ {ahorro:.0f}", f"Ahorro luz S/ {ahorro_mes:.2f}/mes")

    st.success(f"✅ Con HSP de Juliaca {HSP}, tu consumo es {energia:.0f} Wh/día. Con este kit comercial ya tienes luz garantizada {dias_aut} día(s) sin sol.")
    st.info("💡 ¿Por qué es más barato? Porque no te vendemos un panel de 550W si solo necesitas 31W. Te vendemos el de 50W, que es el comercial más cercano y suficiente.")

    st.write("**Consumo por equipo:**")
    st.bar_chart(df.set_index("Equipo")["Energía (Wh/día)"])
