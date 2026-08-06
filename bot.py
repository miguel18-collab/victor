# ============================================
# BOT DE VENTAS - Guia de referencia
# Codigo completo hasta donde vamos, con espacios 
# comentados para las partes que ustedes completan
# ============================================

import pandas as pd
import glob

# --------------------------------------------
# PARTE 1: Buscar y leer los archivos (YA VISTO)
# --------------------------------------------
archivos_csv = glob.glob("*.csv")
archivos_xlsx = glob.glob("*.xlsx")

lista_informes = []

for archivo in archivos_csv:
    df = pd.read_csv(archivo)
    lista_informes.append(df)
    print(f"Leido: {archivo} - {len(df)} filas")

for archivo in archivos_xlsx:
    df = pd.read_excel(archivo, engine='openpyxl')
    lista_informes.append(df)
    print(f"Leido: {archivo} - {len(df)} filas")


# --------------------------------------------
# PARTE 2: Consolidar (YA VISTO - primer intento)
# Aqui van a ver el problema de columnas distintas
# --------------------------------------------
df_consolidado = pd.concat(lista_informes, ignore_index=True)
print(df_consolidado.columns)
# En este punto probablemente veas mas de 7 columnas


# --------------------------------------------
# PARTE 3: Renombrar columnas (COMPLETEN USTEDES)
# Identifiquen cual archivo tiene columnas distintas
# --------------------------------------------
for i, df in enumerate(lista_informes):
    if '____' in df.columns:  # completar: nombre de columna unica
        lista_informes[i] = df.rename(columns={
            # completar el diccionario aqui
        })

df_consolidado = pd.concat(lista_informes, ignore_index=True)
print(df_consolidado.columns)  # deberia mostrar exactamente 7


# --------------------------------------------
# PARTE 4: Limpieza de datos (NUEVO - hoy)
# --------------------------------------------

# 4a. Eliminar filas duplicadas
filas_antes = len(df_consolidado)
df_consolidado = df_consolidado.drop_duplicates()
print(f"Filas antes: {filas_antes} - despues: {len(df_consolidado)}")

# 4b. Explorar valores nulos ANTES de decidir que hacer
print(df_consolidado.isnull().sum())

# 4c. Rellenar segun el tipo de columna
# completar: decidan que valor tiene sentido para cada columna con nulos


# --------------------------------------------
# PARTE 5: Guardar el resultado
# --------------------------------------------
df_consolidado.to_excel("consolidado_limpio.xlsx", index=False)
print("Archivo guardado")

# ADVERTENCIA: si vuelven a ejecutar este script, glob va a 
# encontrar tambien "consolidado_limpio.xlsx" y tratar de leerlo 
# como si fuera un archivo de sucursal (dara error).
# Solucion: cambien el patron de busqueda arriba de "*.xlsx" a 
# "sucursal_*.xlsx", o guarden el resultado en una subcarpeta aparte.

