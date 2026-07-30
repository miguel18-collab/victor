import pandas as pd 
import glob

# exploracion de los datos y diferentes 
# .csv y .xlsx

df_medellin = pd.read_csv("sucursal_medellin.csv")
#print(df_medellin.head(3))

print("\n")

df_bogota = pd.read_excel("sucursal_bogota.xlsx")
#print(df_bogota.head(3))

#print(df_bogota.columns)

print("\n")

#print(df_medellin.columns)

# agrupar archivos por tipo .csv y .xlsx
archivos_csv = glob.glob("*.csv")
archivos_xlsx = glob.glob("*.xlsx")

print(archivos_csv)

print("\n")

print(archivos_xlsx)

#unificar en una lista 
lista_informes = []

for archivo in archivos_csv:
    df = pd.read_csv(archivo)
    lista_informes.append(df)
    print(f"leidos: {archivo} - {len(df)}")
    
print("\n")
    
for archivo in archivos_xlsx:
    df = pd.read_excel(archivo)
    lista_informes.append(df)
    print(f"leido: {archivo} - {len(df)} filas")

#unificar los dataframes
df_consolidado = pd.concat(lista_informes, ignore_index = True)

print(df_consolidado)

#resolver renombrando columnas de bogota

for i, df in enumerate (lista_informes):
    if 'fecha_venta' in df.columns:
        lista_informes[i] = df.rename(colums={
            "fecha_venta": "fecha", "producto": "producto",
            "categoria": "categoria", "cant": "cantidad",
            "valor_unitario": "precio_unitario",
            "vendedor": "vendedor", "pago": "metodo_pago"            
        })

df_consolidado = pd.concat(lista_informes, ignore_index = True)
print(df_consolidado)


