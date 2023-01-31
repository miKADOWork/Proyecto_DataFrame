import pandas as pd


# Contador ES MUY OPTIMIZABLE 
def CountForAName(NOMBRE, Dataframe, key_name):
    count = 0

    #  Buscamos la primera possicion donde aparece el nombre 
    for j in range(0, len(Dataframe)):
        if Dataframe[key_name][j] == NOMBRE:
            # Contamos cuantas veces aparece
            count += 1
    return count


# definimos la funcion contador
def CounterStrike(names_without_Repes, Dataframe):
    """
    Entran un conjunto con los nombres y el dataframe aunque este como variabole global mejor pasarlo por si aka
        Set x DataFrame --------------------------> Array [2]
        names_without_Repes, Dataframe -----------> Array[0] = name, Array[1] = #Repes
    """
    Contador = [(a, CountForAName(a, Dataframe, "Asociación")) for a in names_without_Repes]

    return Contador


# --------------------------------------------------------------------------------------------------------------------------
# Leemos el archivo
df = pd.read_csv("subvenciones.csv",
                    encoding="latin1",
                    header=0,
                )

# Oredenamos el dataframe sin eliminar las repetiocones por el nombre
df = df.sort_values(by=['Asociación'])

# Guardamos los nombres de las diferentes asociaciones en un conjunto para eliminar las repeticiones
nombres_sin_repe = list({a for a in df["Asociación"]})

valores = CounterStrike(nombres_sin_repe, df)

# Creamos las futuras columnas
nombres = []
suma =[]
media = []
maxim = []
aux = []

# Para cada nombre.
for nombre in valores:
    print(nombre)
    # Miramos cuando esta el primer valor que sale
    for i in range(0, len(df["Asociación"])):
        if nombre[0] == df["Asociación"][i]:
            for j in range(0, nombre[1]):
                aux.append(df["Importe"][i + j])
            
            i = i + j 
            suma.append(sum(aux))
            media.append(suma[len(suma)-1]/int(nombre[1]))
            maxim.append(max(aux))
            nombres.append(nombre[0]) 
            aux = [] # reseteamos la varible
            break


# Creamos un diccionario que sera convertido a nuestro dataframe
dic = {

        "Asociación": nombres,
        "Suma": suma,
        "Media": media,
        "Maxim": maxim,
}

result = pd.DataFrame(dic)
print(result)
