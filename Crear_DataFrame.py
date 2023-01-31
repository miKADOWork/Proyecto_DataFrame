import pandas as pd

ENCODING = "latin1"
PATH_TO_DATA = "subvenciones.csv"
KEY_COLUMNA_BUSQUEDA = "Asociación"

# --------------------------------------------------------------------------------------------------------------------------
# PROGRAMA
# --------------------------------------------------------------------------------------------------------------------------

# Leemos el archivo
df = pd.read_csv(   
                    PATH_TO_DATA,
                    encoding=ENCODING,
                    header=0,
                )

dic =   {
            "Asociación":   list({a for a in df[KEY_COLUMNA_BUSQUEDA]}),
            "Max":          [a for a in df.groupby(by = KEY_COLUMNA_BUSQUEDA).max()["Importe"]],
            "Suma":         [a for a in df.groupby(by=KEY_COLUMNA_BUSQUEDA).sum()["Importe"]],
            "Media":        [a for a in df.groupby(by=KEY_COLUMNA_BUSQUEDA).mean()["Importe"]],
        }

df = pd.DataFrame(dic)
print(df)
