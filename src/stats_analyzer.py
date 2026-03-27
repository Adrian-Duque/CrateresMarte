"""
stats_analyzer.py
=================
Módulo de análisis estadístico descriptivo de datasets de cráteres planetarios.

Responsabilidades:
    - Calcular estadísticos descriptivos (media, desviación estándar,
      percentiles, mínimo, máximo).
    - Generar histogramas de distribución de variables.
    - Generar matrices de correlación (mapa de calor).

Uso:
    from src.stats_analyzer import (
        estadisticas_descriptivas,
        generar_histogramas,
        matriz_correlacion,
    )

    stats = estadisticas_descriptivas(df_marte, ['DIAM_CIRCLE_IMAGE', 'DEPTH_RIMFLOOR_TOPOG'])
    generar_histogramas(df_marte, ['DIAM_CIRCLE_IMAGE', 'DEPTH_RIMFLOOR_TOPOG'])
    matriz_correlacion(df_marte, ['log_diam', 'log_depth', 'has_layers'])
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def estadisticas_descriptivas(df: pd.DataFrame, variables: list) -> pd.DataFrame:
    """
    Calcula estadísticas descriptivas para las variables indicadas.

    Estadísticos calculados:
        count, mean, std, min, 25%, 50%, 75%, max.

    Args:
        df (pd.DataFrame): DataFrame preprocesado.
        variables (list[str]): Lista de nombres de columnas a analizar.

    Returns:
        pd.DataFrame: Tabla de estadísticos descriptivos.

    Example:
        >>> stats = estadisticas_descriptivas(df, ['DIAM_CIRCLE_IMAGE'])
        >>> print(stats)
    """
    _validar_columnas(df, variables)
    resumen = df[variables].describe(percentiles=[0.25, 0.5, 0.75])
    return resumen


def generar_histogramas(
    df: pd.DataFrame,
    variables: list,
    bins: int = 50,
    color: str = 'steelblue',
    guardar_en: str = None,
) -> None:
    """
    Genera histogramas de distribución para cada variable indicada.

    Args:
        df (pd.DataFrame): DataFrame preprocesado.
        variables (list[str]): Lista de columnas a visualizar.
        bins (int): Número de intervalos del histograma. Por defecto 50.
        color (str): Color de las barras. Por defecto 'steelblue'.
        guardar_en (str | None): Ruta de fichero para guardar la figura (p. ej.
            'output/histogramas.png'). Si es None, se muestra en pantalla.

    Returns:
        None
    """
    _validar_columnas(df, variables)

    n = len(variables)
    fig, axes = plt.subplots(1, n, figsize=(5 * n, 4))
    if n == 1:
        axes = [axes]

    for ax, var in zip(axes, variables):
        ax.hist(df[var].dropna(), bins=bins, edgecolor='black', color=color, alpha=0.85)
        ax.set_title(f'Distribución: {var}', fontsize=11, fontweight='bold')
        ax.set_xlabel(var)
        ax.set_ylabel('Frecuencia')
        ax.grid(axis='y', linestyle='--', alpha=0.5)

    plt.suptitle('Histogramas de variables de cráteres', fontsize=13, y=1.02)
    plt.tight_layout()

    if guardar_en:
        plt.savefig(guardar_en, bbox_inches='tight', dpi=150)
        print(f"[OK] Figura guardada en '{guardar_en}'.")
    else:
        plt.show()


def matriz_correlacion(
    df: pd.DataFrame,
    variables: list,
    guardar_en: str = None,
) -> None:
    """
    Genera un mapa de calor de la matriz de correlación de Pearson.

    Args:
        df (pd.DataFrame): DataFrame preprocesado.
        variables (list[str]): Lista de columnas a correlacionar.
        guardar_en (str | None): Ruta para guardar la figura. Si es None,
            se muestra en pantalla.

    Returns:
        None
    """
    _validar_columnas(df, variables)

    corr = df[variables].corr()

    plt.figure(figsize=(max(6, len(variables) * 1.5), max(5, len(variables) * 1.2)))
    sns.heatmap(
        corr,
        annot=True,
        fmt='.2f',
        cmap='coolwarm',
        square=True,
        linewidths=0.5,
        vmin=-1,
        vmax=1,
    )
    plt.title('Matriz de correlación de Pearson', fontsize=13, fontweight='bold')
    plt.tight_layout()

    if guardar_en:
        plt.savefig(guardar_en, bbox_inches='tight', dpi=150)
        print(f"[OK] Figura guardada en '{guardar_en}'.")
    else:
        plt.show()


# ---------------------------------------------------------------------------
# Funciones auxiliares privadas
# ---------------------------------------------------------------------------

def _validar_columnas(df: pd.DataFrame, variables: list) -> None:
    """Lanza ValueError si alguna columna no existe en el DataFrame.
    Advierte si alguna columna existe pero está completamente vacía (NaN)."""
    faltantes = [v for v in variables if v not in df.columns]
    if faltantes:
        raise ValueError(
            f"Las siguientes columnas no existen en el DataFrame: {faltantes}\n"
            f"Columnas disponibles: {list(df.columns)}"
        )
    vacias = [v for v in variables if df[v].isna().all()]
    if vacias:
        print(f"[AVISO] Columnas sin datos (todos NaN): {vacias}. "
              f"Los resultados para estas variables estarán vacíos.")
