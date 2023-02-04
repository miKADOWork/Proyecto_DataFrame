# --------------------------------------------------------------------------------------------------------------------------
# Importaciones
# --------------------------------------------------------------------------------------------------------------------------

import pandas as pd
import time as tm # Paquete tiempo 
#import regex
from openpyxl.styles import PatternFill, GradientFill
import openpyxl

# --------------------------------------------------------------------------------------------------------------------------
# Variables Globales
# --------------------------------------------------------------------------------------------------------------------------

ENCODING = "latin1"
PATH_TO_DATA = "subvenciones.csv"
NOMBRE_EXCEL_CREADO = "Resumen_Subenciones.xlsx"
COLUMNA_INICIO = 5
FILA_INICIO = 5

# --------------------------------------------------------------------------------------------------------------------------
# Colores de Celdas
# --------------------------------------------------------------------------------------------------------------------------

redFill = PatternFill   (  
                            start_color='FFFF0000',
                            end_color='FFFF0000',
                            fill_type='solid'
                        )

yellowFill = PatternFill   (  
                            start_color="FFFF00",
                            fill_type='solid'
                        )

# --------------------------------------------------------------------------------------------------------------------------
# Funciones
# --------------------------------------------------------------------------------------------------------------------------


def Pinta_Columnas(rango_seleccionado, patron_relleno):
    """
    Entran un string de la forma <columna><numero_inicial>:<columna><numero_final>
    """
    # Separamos el rango en la celda inicial y la final
    rango = rango_seleccionado.split(sep=':') 
    columna_nombre = rango[0][0]
    rango = [
                rango[0].replace(columna_nombre, ""), 
                rango[1].replace(columna_nombre, "")
            ]

    for fila in range(int(rango[0]), int(rango[1])):
        wb.active[columna_nombre + str(fila)].fill = patron_relleno


def Pinta_Filas(rango_seleccionado, patron_relleno): # FALTA ACABARLA
    """
    Entran un string de la forma <fila_inicial><numero>:<fila_final><numero>
    """
    columna_inicial_nombre = ""
    columna_final_nombre = ""
 
    # Separamos el rango en la celda inicial y la final
    rango = rango_seleccionado.split(sep=':')
    for pos in range(0, len(rango[0])):
        columna_inicial_nombre = "".join([i for i in rango[0] if not i.isdigit()])

    for pos in range(0, len(rango[0])):
        columna_final_nombre = "".join([i for i in rango[1] if not i.isdigit()])
    
    # Calculamos la fila sobre la que trabajamos
    fila_de_trabajo = rango[0].replace(columna_inicial_nombre, "")

    rango = [
                columna_inicial_nombre, 
                columna_final_nombre,
            ]

    for columna in range(ord(rango[0])-ord(rango[0]), ord(rango[1]) - ord(rango[0]) + 1):
        wb.active[chr(ord(columna_inicial_nombre) + columna) + fila_de_trabajo].fill = patron_relleno


# --------------------------------------------------------------------------------------------------------------------------
# Programa
# --------------------------------------------------------------------------------------------------------------------------

# Leemos el archivo
df = pd.read_csv(   
                    PATH_TO_DATA,
                    encoding = ENCODING,
                    header = 0,
                )

# Oredenamos el dataf rame sin eliminar las repetiocones por el nombre porque es mas elegante
df = df.sort_values(by = ['Asociación'])
df["Importe"] = df["Importe"].astype(float)

# Ordenamos por nombre las asociaciones para que esten alineados con los datos correctos ya que les hemos hecho un sort pero al eliminar duplicidades con un set quedan desorganizados
Lista_Asociaciones = list({a for a in df["Asociación"]})
Lista_Asociaciones.sort()

dic =   {
            "Asociación":   Lista_Asociaciones,
            "Max":          [float(a) for a in df.groupby(by = 'Asociación',).max()["Importe"]],
            "Suma":         [float(a) for a in df.groupby(by = 'Asociación',).sum()["Importe"]],
            "Media":        [round(a,2) for a in df.groupby(by = 'Asociación',).mean()["Importe"]],
        }

# Machacamos la variable con los nuevos datos obtenidos y eliminamos la lista de asociaciones que ya no nos será de utilidad
df = pd.DataFrame(dic)
del Lista_Asociaciones

# Escribimos estos datos en un archivo de excel 
df.to_excel (
                NOMBRE_EXCEL_CREADO,            # Creamos un libro de excel
                sheet_name = "Datos_Operados",  # Creamos una hoja destino en el libro con los datos del Dataframe
                index = False,                  # No escribe los indices de las filas
                startrow = FILA_INICIO,         # Fila de inicio del volcado del Dataframe
                startcol = COLUMNA_INICIO,      # Columna de inicio del volcado del Dataframe
            )

# Eliminamos el df porque no lo utilizamos mas pero guardamos la forma 
shape_de_df = df.shape
del df

# Damos formato a la tabla que nos a generado ------------------------------------------------------------------------
# Abrimos el arxivo de excel en un Dataframe 
columnas_seleccionadas = chr(ord('A') + COLUMNA_INICIO ) + ":" + chr(ord('A') + COLUMNA_INICIO + shape_de_df[1] - 1)                    # Calculamos las letras de las columnas que seleccionamos del excel
Libro_Excel = pd.read_excel (
                                NOMBRE_EXCEL_CREADO,                                                                                    # Path al archivo en este caso el nombre porque estan en el mismo relative path
                                usecols = columnas_seleccionadas,                                                                       # Calculamos un string que contenga el rango de la tabla con la que queremos trabajar
                                header = FILA_INICIO,                                                                                   # Indicamos la primera fila con datos (que es nuestra cabezera)
                            )

print(Libro_Excel)

# Pintamos todas las columnas
wb =  openpyxl.load_workbook(NOMBRE_EXCEL_CREADO)     # Abrimos el Libro de excel
wb.active = wb["Datos_Operados"]

# Coloreamos la cabezera de la tabla
rango_cabezera = str(chr(ord("A") + COLUMNA_INICIO)) + str(FILA_INICIO + 1) + ":" + str(chr(ord("A") + COLUMNA_INICIO + shape_de_df[1] - 1)) + str(FILA_INICIO + 1) 
Pinta_Filas(rango_cabezera, redFill)

# Coloreamos alternando con dos colores las columnas del resultado
for i in range(0, shape_de_df[1]):
    posicion = chr(ord(columnas_seleccionadas[0]) + i) + str(FILA_INICIO + 2) + ":" + chr(ord(columnas_seleccionadas[0]) + i) + str(shape_de_df[0] + FILA_INICIO + 2) # 1 porque empieza contando en 0 y excel en 1 y el otro por la linea del header 
    if (i%2 == 0):
        Pinta_Columnas(posicion, redFill)
    else:
        Pinta_Columnas(posicion, yellowFill)

# Guardamos los canvios sobrescribiendo el archivo original
wb.save(NOMBRE_EXCEL_CREADO)

# Ponemos en negrita en todas las celdas en las que aparezca la palaba "AMPA" dicha palabra en negrita (Usamos regex)
#df['team'] =  [re.sub(r'[\n\r]*','', str(x)) for x in df['team']]







# Por practicar mas, creamos un archivo de word que contenga estos datos en un informe

##### TODO: 
# Falta que el texto que contiene la columna en las funciones de colorear no solo sea de un caracter por ejemplo podriamos a priori trabajar en la celda BB34 
# Hacer uso de reggex para la mejor simplificacion del codigo posible
# Poner en las celdas con las asociaciones, la palabra AMPA en negrita