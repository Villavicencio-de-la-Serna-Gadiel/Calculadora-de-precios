def para_graficos(diccionario):
    claves_diccionario = list(diccionario.keys())
    llaves_diccionario = list(diccionario.values())
    llaves_diccionario.sort()
    claves_diccionario.sort()
    diccionario_graficos = {"Productos": claves_diccionario,
                            "Precios": llaves_diccionario}
    return diccionario_graficos
