"""
preprocessor.py
===============
Módulo de limpieza y transformación de datasets de cráteres planetarios.

Responsabilidades:
    - Eliminar filas con valores nulos.
    - Convertir tipos de datos.
    - Generar variables derivadas (transformaciones logarítmicas, flags binarios).

Variables generadas:
    Luna:
        - log_diam   → log(1 + DIAM_CIRC_IMG)

    Marte:
        - log_diam   → log(1 + DIAM_CIRCLE_IMAGE)
        - log_depth  → log(1 + DEPTH_RIMFLOOR_TOPOG)
        - log_err    → log(1 + error de localización, si existe)
        - has_layers → 1 si NUMBER_LAYERS > 0, 0 en caso contrario

Uso:
    from src.preprocessor import preprocesar_dataset

    df_luna  = preprocesar_dataset(df_luna,  planeta='luna')
    df_marte = preprocesar_dataset(df_marte, planeta='marte')
"""

import pandas as pd
import numpy as np


def preprocesar_dataset(df: pd.DataFrame, planeta: str) -> pd.DataFrame:
    """
    Limpia y transforma el dataset para su análisis posterior.

    El DataFrame original NO se modifica (se trabaja sobre una copia).

    Args:
        df (pd.DataFrame): DataFrame original cargado con `cargar_dataset`.
        planeta (str): 'luna' o 'marte'.

    Returns:
        pd.DataFrame: DataFrame preprocesado con variables derivadas añadidas.
    """
    df = df.copy()
    registros_antes = len(df)

    # ------------------------------------------------------------------
    # 1. Eliminar filas con valores nulos solo en columnas esenciales
    #    (no eliminar por columnas opcionales como profundidad o capas)
    # ------------------------------------------------------------------
    if planeta == 'luna':
        cols_esenciales = ['DIAM_CIRC_IMG', 'LAT_CIRC_IMG', 'LON_CIRC_IMG']
    elif planeta == 'marte':
        cols_esenciales = ['DIAM_CIRCLE_IMAGE', 'LATITUDE_CIRCLE_IMAGE', 'LONGITUDE_CIRCLE_IMAGE']
    else:
        cols_esenciales = []

    cols_existentes = [c for c in cols_esenciales if c in df.columns]
    df.dropna(subset=cols_existentes, inplace=True)
    registros_eliminados = registros_antes - len(df)

    # ------------------------------------------------------------------
    # 2. Variables derivadas según el planeta
    # ------------------------------------------------------------------
    if planeta == 'luna':
        df['log_diam'] = np.log1p(df['DIAM_CIRC_IMG'])

    elif planeta == 'marte':
        df['log_diam'] = np.log1p(df['DIAM_CIRCLE_IMAGE'])

        # log_depth es opcional: solo si hay datos válidos en la columna
        if df['DEPTH_RIMFLOOR_TOPOG'].notna().any():
            df['log_depth'] = np.log1p(df['DEPTH_RIMFLOOR_TOPOG'])
        else:
            df['log_depth'] = np.nan
            print("[AVISO] 'DEPTH_RIMFLOOR_TOPOG' sin datos. 'log_depth' se creó vacío.")

        # has_layers: NUMBER_LAYERS puede tener mixed types o NaN
        if 'NUMBER_LAYERS' in df.columns:
            df['NUMBER_LAYERS'] = pd.to_numeric(df['NUMBER_LAYERS'], errors='coerce')
            if df['NUMBER_LAYERS'].notna().any():
                df['has_layers'] = (df['NUMBER_LAYERS'] > 0).astype(int)
            else:
                df['has_layers'] = 0
                print("[AVISO] 'NUMBER_LAYERS' sin datos. 'has_layers' se estableció a 0.")
        else:
            df['has_layers'] = 0

        # Error de localización (columna opcional)
        if 'ERR_CIRCLE_IMAGE' in df.columns and df['ERR_CIRCLE_IMAGE'].notna().any():
            df['log_err'] = np.log1p(df['ERR_CIRCLE_IMAGE'])

    print(
        f"[OK] Preprocesamiento completado para '{planeta}'.\n"
        f"     Registros válidos: {len(df):,}  "
        f"(eliminados por nulos: {registros_eliminados:,})"
    )
    return df
