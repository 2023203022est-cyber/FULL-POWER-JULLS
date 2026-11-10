import streamlit as st
import re

st.title("🛒 ILLARI JULLS - ¿QUÉ COMPRO?")
st.subheader("Pega tu código de la App 1 y listo")

st.write("Ejemplo de código: P31-B22-I34")

codigo = st.text_input("Pega aquí tu código")

if codigo:
    numeros = re.findall(r"\d+", codigo)
    if len(numeros) >= 3:
        panel_nec = int(numeros[0])
        bat_nec = int(numeros[1])
        inv_nec = int(numeros[2])

        st.write(f"Necesitas: Panel {panel_nec}W, Batería {bat_nec}Ah, Inversor {inv_nec}W")

        # CATÁLOGO
        paneles = [(50, 120), (100, 220), (200, 380), (340, 550), (450, 750)]
        baterias = [(20, 150), (50, 300), (100, 550), (150, 800)]
        inversores = [(100, 180), (300, 280), (500, 450), (1000, 700)]

        def buscar(lista, necesito):
            for valor, precio in lista:
                if valor >= necesito:
                    return valor, precio
            return lista[-1]

        p_val, p_precio = buscar(paneles, panel_nec)
        b_val, b_precio = buscar(baterias, bat_nec)
        i_val, i_precio = buscar(inversores, inv_nec)

        st.success(f"✅ COMPRAR: Panel Solar {p_val}W - S/ {p_precio}")
        st.success(f"✅ COMPRAR: Batería {b_val}Ah - S/ {b_precio}")
        st.success(f"✅ COMPRAR: Inversor {i_val}W - S/ {i_precio}")
        st.success(f"✅ COMPRAR: Cable + Controlador + Soporte")

        total = p_precio + b_precio + i_precio + 120
        st.markdown(f"## TOTAL APROX: S/ {total}")
        st.balloons()
    else:
        st.error("Ese código está mal, cópialo completo de la App 1")
