import streamlit as st
import funciones as f
import pandas as p
archivo_csv = "productos_precios.csv"
open(archivo_csv).close()
def nombre_pagina():
    st.set_page_config(page_title = "Calculadora de precios")
def cambiar_archivo():
    open(archivo_csv, "w").close()
    df = p.DataFrame(f.para_graficos(productos_precios()))
    df.to_csv(archivo_csv, index = False)
def cargar_productos_precios(archivo):
    productos_precios_actual = {}
    dt = p.read_csv(archivo)
    for _, fila in dt.iterrows():
        productos_precios_actual[fila["Productos"]] = fila["Precios"]
    return productos_precios_actual
def productos_precios():
    if "productos_precios" not in st.session_state:
        st.session_state.productos_precios = cargar_productos_precios(archivo_csv)
    return st.session_state.productos_precios
def filtro_productos_precios():
    filtrado = productos_precios().copy()
    if len(productos_precios()):
        for producto,precio in productos_precios().items():
            if precio < st.session_state.intervalo_precios:
                filtrado.pop(producto)
    return filtrado
def restablecido():
    if "restablecido" not in st.session_state:
        st.session_state.restablecido = True
    return st.session_state.restablecido
def titulos():
    st.title("Calculadora de precios")
    st.write('''Indique los productos, analízalos en
                gráficas y calcule precios.''')
    st.caption("De Villavicencio de la Serna Gadiel")
def sidebar():
    def registrar_productos():
        with st.expander("Registrar productos"):
            with st.form("Registrar producto"):
                producto = st.text_input("Nombre del producto")
                precio = st.number_input("Precio del producto",
                                         min_value = 0.00,
                                         step = 1.00)
                registrar = st.form_submit_button("Registrar")
            if registrar:
                if len(producto) and precio > 0:
                    productos_precios()[producto.lower()] = precio
                    st.success("Registrado con éxito")
                else:
                    if not len(producto):
                        st.warning("El producto tiene que tener un nombre.")
                    if precio <= 0:
                        st.warning("El precio tiene que ser mayor a cero.")
            eliminar = st.button("Eliminar productos")
            if eliminar:
                productos_precios().clear()
                open(archivo_csv, "w").close()
    def filtros():
        with st.expander("Filtros"):
            with st.form("Configurar filtro"):
                st.slider('''Filtrar por precio
                                  números menores a''',
                                key = "intervalo_precios")
                registrar = st.form_submit_button("Registrar")
            if registrar:
                st.success("Registrado con éxito")
                st.session_state.restablecido = False
            restablecer = st.button("Restablecer")
            if restablecer:
                st.session_state.restablecido = True
    with st.sidebar:
        st.header("Opciones")
        registrar_productos()
        filtros()
def tab1(productos_precios_actual):
    with productos:
        st.header("Productos")
        st.write('''Aquí podrá revisar los productos y
                    filtrarlos según sus características.''')
        if not st.session_state.restablecido:
            st.info(f"Mayores a {st.session_state.intervalo_precios}")
        if len(productos_precios_actual):
            dt = p.DataFrame(f.para_graficos(productos_precios_actual))
            st.dataframe(dt)
def tab2(productos_precios_actual):
    productos_precios_graficos = f.para_graficos(productos_precios_actual)
    with analisis:
        st.header("Análisis")
        st.write('''Aquí se mostrarán el análisis, en gráficos
                    sobre los productos''')
        if not st.session_state.restablecido:
            st.info(f"Mayores a {st.session_state.intervalo_precios}")
        if len(productos_precios_actual):
            grafico_barras, grafico_lineas, grafico_areas =\
            st.tabs(["Gráfico de barras", "Gráfico de líneas",
                     "Gráfico de áreas"])
            with grafico_barras:
                st.bar_chart(productos_precios_graficos)
            with grafico_lineas:
                st.line_chart(productos_precios_graficos)
            with grafico_areas:
                st.area_chart(productos_precios_graficos)
def tab3():
    if "suma" not in st.session_state:
        st.session_state.suma = 0
    with calculo_precios:
        st.header("Calculo de precios")
        st.write('''Al presionar la tecla Enter se enviará el formulario,
                    ya sea al escribir el nombre del producto o la cantidad
                    de kilos.''')
        with st.form("Añadir producto"):
            producto = st.text_input("Nombre del producto")
            kilos = st.number_input("Kilos",
                                    min_value = 0.00,
                                    step = 1.00)
            calcular = st.form_submit_button("Calcular")
        if calcular:
            try:
                st.session_state.suma += productos_precios()[producto.lower()]*kilos
                st.info(f"La cantidad es {st.session_state.suma}.")
            except KeyError:
                st.warning("No se ha podido encontrar el producto.")
        restablecer = st.button("Restablecer")
        if restablecer:
            st.session_state.suma = 0
nombre_pagina()
titulos()
sidebar()
productos, analisis, calculo_precios =\
st.tabs(["Productos", "Análisis", "Calculo de precios"])
if restablecido():
    diccionario = productos_precios()
else:
    diccionario = filtro_productos_precios()
tab1(diccionario)
tab2(diccionario)
tab3()
cambiar_archivo()
