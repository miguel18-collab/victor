import glob
from pathlib import Path
import pandas as pd

# -----------------------------
# CONFIGURACION GENERAL
# -----------------------------
CARPETA = Path(__file__).resolve().parent
COLUMNAS_OBJETIVO = [
    "fecha",
    "producto",
    "categoria",
    "cantidad",
    "precio_unitario",
    "vendedor",
    "metodo_pago",
]

# -----------------------------
# FUNCIONES DE NORMALIZACION
# -----------------------------
def normalizar_nombre_columna(nombre: str) -> str:
    nombre = str(nombre).strip().lower()
    nombre = nombre.replace(" ", "").replace("-", "").replace("/", "_")
    nombre = "".join(car for car in nombre if car.isalnum() or car == "_")
    return nombre


def preparar_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [normalizar_nombre_columna(col) for col in df.columns]

    renombres = {
        "fecha_venta": "fecha",
        "fechaventa": "fecha",
        "producto": "producto",
        "categoria": "categoria",
        "cant": "cantidad",
        "cantidad": "cantidad",
        "valor_unitario": "precio_unitario",
        "precio_unitario": "precio_unitario",
        "vendedor": "vendedor",
        "pago": "metodo_pago",
        "metodo_de_pago": "metodo_pago",
        "metodo_pago": "metodo_pago",
    }

    df = df.rename(columns=renombres)
    df = df.loc[:, ~df.columns.duplicated()].copy()
    df = df.reindex(columns=COLUMNAS_OBJETIVO, fill_value=pd.NA)
    return df


# -----------------------------
# FUNCIONES DE LIMPIEZA
# -----------------------------
def limpiar_datos(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    for columna in ["fecha", "producto", "categoria", "vendedor", "metodo_pago"]:
        if columna in df.columns:
            df[columna] = df[columna].astype("string").str.strip()

    if "cantidad" in df.columns:
        df["cantidad"] = pd.to_numeric(df["cantidad"], errors="coerce").fillna(0)

    if "precio_unitario" in df.columns:
        df["precio_unitario"] = pd.to_numeric(df["precio_unitario"], errors="coerce").fillna(0)

    df = df.replace(r"^\s*$", pd.NA, regex=True)
    df = df.dropna(how="all")

    for columna, valor in {
        "fecha": "No especificado",
        "producto": "No especificado",
        "categoria": "No especificado",
        "vendedor": "No especificado",
        "metodo_pago": "No especificado",
    }.items():
        if columna in df.columns:
            df[columna] = df[columna].fillna(valor)

    df = df.drop_duplicates()
    return df


# -----------------------------
# PROCESO PRINCIPAL
# -----------------------------
archivos_csv = sorted(CARPETA.glob("sucursal_*.csv"))
archivos_excel = sorted(CARPETA.glob("sucursal_*.xlsx"))

print("Archivos CSV encontrados:", [archivo.name for archivo in archivos_csv])
print("Archivos Excel encontrados:", [archivo.name for archivo in archivos_excel])

lista_informes = []

for archivo in archivos_csv:
    df = pd.read_csv(archivo)
    df = preparar_dataframe(df)
    lista_informes.append(df)
    print(f"Leídos: {archivo.name} - {len(df)} registros cargados con éxito.")

for archivo in archivos_excel:
    df = pd.read_excel(archivo)
    df = preparar_dataframe(df)
    lista_informes.append(df)
    print(f"Leídos: {archivo.name} - {len(df)} registros cargados con éxito.")

if not lista_informes:
    raise FileNotFoundError("No se encontraron archivos de ventas para consolidar.")

# Consolidar todos los registros en un solo DataFrame con exactamente 7 columnas

df_consolidado = pd.concat(lista_informes, ignore_index=True)
df_consolidado = df_consolidado.loc[:, ~df_consolidado.columns.duplicated()].copy()
df_consolidado = df_consolidado.reindex(columns=COLUMNAS_OBJETIVO)

# Limpieza final
filas_antes = len(df_consolidado)
df_consolidado = limpiar_datos(df_consolidado)
print(f"Filas antes: {filas_antes} - despues: {len(df_consolidado)}")
print("Columnas finales:", df_consolidado.columns.tolist())
print(df_consolidado.head())

salida = CARPETA / "consolidado_limpio.xlsx"
df_consolidado.to_excel(salida, index=False)
print(f"Archivo guardado en: {salida}")


# ============================================
# ANÁLISIS DE NEGOCIO - Bot de Ventas
# (continúa después de tu código de lectura, 
# consolidación y limpieza ya hecho)
# ============================================
import matplotlib.pyplot as plt

# --------------------------------------------
# PREGUNTA 1: ¿Cuánto vendió cada categoría en total?
# (EJEMPLO RESUELTO)
# --------------------------------------------
ventas_categoria = df_consolidado.groupby('categoria')['precio_unitario'].sum()
print(ventas_categoria)

ventas_categoria.plot(kind='bar', title='Ventas por Categoria')
plt.ticklabel_format(style='plain', axis='y')
plt.ylabel('Ventas totales')
plt.xlabel('Categoría')
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("grafico_categoria.png")
plt.show()


# --------------------------------------------
# PREGUNTA 2: ¿Qué porcentaje de las ventas representa 
# cada vendedor?
# --------------------------------------------
# Paso 1: agrupen por vendedor y sumen precio_unitario
# Paso 2: impriman el resultado
# Paso 3: hagan un gráfico de torta (pie) con porcentajes
# Paso 4: guarden como "grafico_vendedor.png"
#---------------------------------------------
ventas_vendedor = df_consolidado.groupby('vendedor')['precio_unitario'].sum()
print(ventas_vendedor)

porcentaje_vendedor = ventas_vendedor / ventas_vendedor.sum() *100
print(porcentaje_vendedor)

plt.figure()
ventas_vendedor.plot(
    kind='pie',
    autopct='%1.1f%%',
    title='porcentaje de ventas por vendedor',
    ylabel=''
)

plt.tight_layout
plt.savefig("grafico_vendedor.png")
plt.show()


# --------------------------------------------
# PREGUNTA 3: ¿Cuál es el producto que más se vende?
# --------------------------------------------
# Paso 1: investiguen la función value_counts()
# Paso 2: apliquenla a la columna producto
# Paso 3: impriman el resultado
#---------------------------------------------
producto_mas_vendido = df_consolidado['producto'].value_counts()
print(producto_mas_vendido)
print(f"/n el producto mas vendido es: {producto_mas_vendido.idxmax()},con{producto_mas_vendido.max()} ventas")


# --------------------------------------------
# PREGUNTA 4: ¿Cómo se distribuyen las ventas según 
# el método de pago?
# --------------------------------------------
# Paso 1: agrupen por metodo_pago y sumen precio_unitario
# Paso 2: impriman el resultado
# Paso 3: hagan el gráfico que consideren más apropiado
# Paso 4: guarden como "grafico_metodo_pago.png"
#---------------------------------------------
ventas_metodo_pago = df_consolidado.groupby('metodo_pago')['precio_unitario'].sum()
print(ventas_metodo_pago)

plt.figure()
ventas_metodo_pago.plot(
    kind='bar',
    title='ventas  por metodo de pago')

plt.xticks(rotation=0)
plt.ticklabel_format(style='plain', axis='y')
plt.ylabel('ventas totales')
plt.xlabel('metodo de pago')
plt.tight_layout()
plt.savefig("grafico_metodo_pago.png")
plt.show()

# --------------------------------------------
# RETO OPCIONAL - Para quien termine las 4 preguntas
# PREGUNTA 5: ¿Cuál es el día de la semana con más ventas?
# --------------------------------------------
# Paso 1: investiguen pd.to_datetime() para convertir la columna 
# fecha a formato de fecha real
# Paso 2: investiguen .dt.day_name() para extraer el día de la semana
# Paso 3: agrupen por ese nuevo dato y sumen las ventas
#---------------------------------------------
df_consolidado['fecha_dt'] = pd.to_datetime(df_consolidado['fecha'], errors='coerce')
df_consolidado['dia_semana'] = df_consolidado['fecha_dt'].dt.day_name()

dias_espanol = {
    'Monday': 'Lunes',
    'Tuesday': 'Martes',
    'Wednesday': 'Miércoles',
    'Thursday': 'Jueves',
    'Friday': 'Viernes',
    'Saturday': 'Sábado',
    'Sunday': 'Domingo'
}

df_consolidado['dia_semana'] = df_consolidado['fecha_dt'].dt.day_name().map(dias_espanol)

ventas_dia_semana = df_consolidado.groupby('dia_semana')['precio_unitario'].sum()
ventas_dia_semana = ventas_dia_semana.sort_values(ascending=False)
print(ventas_dia_semana)

plt.figure()
ventas_dia_semana.plot(
    kind='bar', 
    title='Ventas por Día de la Semana')
plt.ticklabel_format(style='plain', axis='y')
plt.ylabel('Ventas totales')
plt.xlabel('Día de la semana')
plt.xticks(rotation=40)
plt.tight_layout()
plt.savefig("grafico_dia_semana.png")
plt.show()
