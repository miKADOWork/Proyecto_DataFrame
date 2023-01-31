import pandas as pd

PATH = "subvenciones.csv"
ENCOUDING = "latin1"

# --------------------------------------------------------------------------------------------------------------------------
# FUNCIONES
# --------------------------------------------------------------------------------------------------------------------------


# Contador ES MUY OPTIMIZABLE 
def CuentaUnNombre(NOMBRE, Dataframe, key_name):
    """
    Args:
        NOMBRE (String): Nombre que queremos contar en el Dataframe
        Dataframe (df): El Dataframe sobre el que queremos contar
        key_name (String): La llave de la columna en la que se encuentran los nombres

    Returns:
        int: # de veces que aparece el nombre buscado
    """
    count = 0

    #  Buscamos la primera possicion donde aparece el nombre 
    for j in range(0, len(Dataframe)):
        if Dataframe[key_name][j] == NOMBRE:
            count += 1
    return count


def CuenteTodosLosNombres(names_without_Repes, Dataframe):
    """
    Entran un conjunto con los nombres y el dataframe aunque este como variabole global mejor pasarlo por si aka
        Set x DataFrame --------------------------> Array [2]
        names_without_Repes, Dataframe -----------> Array[0] = name, Array[1] = #Repes
    """
    
    # Guardamos en un objeto de tipo lista que en cada posicion contiene una tupla de cada nombre diferente que aparece en la columna de nombres y las veces que se repite dentro del df
    Contador = [(a, CuentaUnNombre(a, Dataframe, "Asociación")) for a in names_without_Repes]

    return Contador


# --------------------------------------------------------------------------------------------------------------------------
# PROGRAMA
# --------------------------------------------------------------------------------------------------------------------------

# Leemos el archivo
df = pd.read_csv(
                    PATH,
                    encoding=ENCOUDING,
                    header=0,               
                )

# Oredenamos el dataframe sin eliminar las repetiocones por el nombre
df = df.sort_values(by=['Asociación'])

# Guardamos los nombres de las diferentes asociaciones en un conjunto para eliminar las repeticiones
nombres_sin_repe = list({a for a in df["Asociación"]})

valores = CuenteTodosLosNombres(nombres_sin_repe, df)

# Creamos las futuras columnas como objetos listas vacias 
nombres =     []
suma    =     []
media   =     []
maxim   =     []
aux     =     []

# Para cada nombre
for tupla in valores:
    # Miramos cuando esta el primer valor que sale enla posicion del Dataframe
    for i in range(0, len(df["Asociación"])):
        if tupla[0] == df["Asociación"][i]:
            
            # Iteramos para movernos y añadir en el auxiliar todos los valores de un nombre dado tantas posiciones como en las que aparezca
            for j in range(0, tupla[1]):
                aux.append(df["Importe"][i + j])
            
            i = i + j

            # Calculamos los valores de las nuevas columnas
            suma.append(sum(aux))
            media.append(suma[len(suma)-1]/int(tupla[1]))
            maxim.append(max(aux))
            nombres.append(tupla[0]) 
            aux = [] # reseteamos la varible
            break


# Creamos un diccionario que sera convertido a nuestro dataframe
dic = {

        "Asociación": nombres,
        "Suma"      : suma,
        "Media"     : media,
        "Maxim"     : maxim,
}

# Eliminamos las listas que no utilizamos 
del nombres, suma, media, maxim, aux

# Creamos e imprimimos el Dataframe que queriamos encontrar
result = pd.DataFrame(dic)
print(result)
