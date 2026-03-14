"""
data_loader.py
==============
Módulo de carga y validación de datasets de cráteres planetarios.

Responsabilidades:
    - Leer archivos CSV y construir DataFrames.
    - Validar la estructura del dataset (columnas esperadas, tipos).
    - Informar de registros cargados y posibles errores.

Uso:
    from src.data_loader import cargar_dataset

    df_luna  = cargar_dataset('data/luna_crateres.csv',  planeta='luna')
    df_marte = cargar_dataset('data/marte_crateres.csv', planeta='marte')
"""

import pandas as pd

# ---------------------------------------------------------------------------
# Columnas mínimas esperadas por planeta
# ---------------------------------------------------------------------------
COLUMNAS_LUNA = [
    'LAT_CIRC_IMG',
    'LON_CIRC_IMG',
    'DIAM_CIRC_IMG',
    'ARC_IMG',
    'PTS_RIM_IMG',
]

COLUMNAS_MARTE = [
    'LATITUDE_CIRCLE_IMAGE',
    'LONGITUDE_CIRCLE_IMAGE',
    'DIAM_CIRCLE_IMAGE',
    'DEPTH_RIMFLOOR_TOPOG',
    'NUMBER_LAYERS',
]

PLANETAS_VALIDOS = ('luna', 'marte')


def cargar_dataset(ruta_csv: str, planeta: str) -> pd.DataFrame:
    """
    Carga un dataset de cráteres desde un fichero CSV y valida su estructura.

    Args:
        ruta_csv (str): Ruta al fichero CSV.
        planeta (str): Identificador del planeta. Valores válidos: 'luna', 'marte'.

    Returns:
        pd.DataFrame: DataFrame con los datos del catálogo.

    Raises:
        ValueError: Si el planeta no es válido o faltan columnas obligatorias.
        FileNotFoundError: Si no se encuentra el fichero en la ruta indicada.
    """
    if planeta not in PLANETAS_VALIDOS:
        raise ValueError(
            f"Planeta '{planeta}' no reconocido. "
            f"Use uno de: {PLANETAS_VALIDOS}"
        )

    try:
        df = pd.read_csv(ruta_csv)
    except FileNotFoundError:
        raise FileNotFoundError(
            f"No se encontró el fichero '{ruta_csv}'. "
            "Comprueba la ruta e inténtalo de nuevo."
        )

    columnas_esperadas = COLUMNAS_LUNA if planeta == 'luna' else COLUMNAS_MARTE
    columnas_faltantes = [c for c in columnas_esperadas if c not in df.columns]

    if columnas_faltantes:
        raise ValueError(
            f"El dataset no contiene las columnas requeridas: {columnas_faltantes}\n"
            f"Columnas encontradas: {list(df.columns)}"
        )

    print(
        f"[OK] Dataset '{planeta}' cargado desde '{ruta_csv}'.\n"
        f"     Registros: {len(df):,}  |  Columnas: {len(df.columns)}"
    )
    return df
