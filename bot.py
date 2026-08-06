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