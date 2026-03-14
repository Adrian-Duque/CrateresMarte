"""
correlation_analyzer.py
=======================
Módulo de análisis de correlaciones y scatter plots entre variables de cráteres.

Responsabilidades:
    - Calcular la matriz de correlación de Pearson entre variables seleccionadas.
    - Generar scatter plots entre pares de variables.
    - Comparar correlaciones entre los datasets de Luna y Marte.

Uso:
    from src.correlation_analyzer import (
        calcular_correlacion,
        scatter_plot,
        comparar_correlaciones,
    )

    corr = calcular_correlacion(df_marte, ['log_diam', 'log_depth', 'has_layers'])
    scatter_plot(df_marte, x='log_diam', y='log_depth', hue='has_layers')
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def calcular_correlacion(df: pd.DataFrame, variables: list) -> pd.DataFrame:
    """
    Calcula la matriz de correlación de Pearson entre las variables indicadas.

    Args:
        df (pd.DataFrame): DataFrame preprocesado.
        variables (list[str]): Lista de columnas numéricas a correlacionar.

    Returns:
        pd.DataFrame: Matriz de correlación (valores entre -1 y 1).
    """
    _validar_columnas(df, variables)
    return df[variables].corr()


def scatter_plot(
    df: pd.DataFrame,
    x: str,
    y: str,
    hue: str = None,
    titulo: str = None,
    guardar_en: str = None,
) -> None:
    """
    Genera un scatter plot entre dos variables con opción de colorear por una tercera.

    Args:
        df (pd.DataFrame): DataFrame preprocesado.
        x (str): Variable del eje X.
        y (str): Variable del eje Y.
        hue (str | None): Variable categórica para colorear los puntos.
        titulo (str | None): Título del gráfico. Si es None se genera automáticamente.
        guardar_en (str | None): Ruta para guardar la figura. Si es None, se muestra.

    Returns:
        None
    """
    _validar_columnas(df, [x, y])
    if hue:
        _validar_columnas(df, [hue])

    fig, ax = plt.subplots(figsize=(8, 5))

    if hue:
        for valor in sorted(df[hue].unique()):
            subset = df[df[hue] == valor]
            ax.scatter(subset[x], subset[y], label=f'{hue}={valor}', alpha=0.4, s=10)
        ax.legend(title=hue)
    else:
        ax.scatter(df[x], df[y], alpha=0.4, s=10, color='steelblue')

    ax.set_xlabel(x)
    ax.set_ylabel(y)
    ax.set_title(titulo or f'{y} vs {x}', fontsize=12, fontweight='bold')
    ax.grid(linestyle='--', alpha=0.4)
    plt.tight_layout()

    if guardar_en:
        plt.savefig(guardar_en, bbox_inches='tight', dpi=150)
        print(f"[OK] Figura guardada en '{guardar_en}'.")
    else:
        plt.show()


def comparar_correlaciones(
    df_luna: pd.DataFrame,
    df_marte: pd.DataFrame,
    vars_luna: list,
    vars_marte: list,
) -> None:
    """
    Muestra en paralelo las matrices de correlación de Luna y Marte.

    Args:
        df_luna (pd.DataFrame): DataFrame preprocesado de la Luna.
        df_marte (pd.DataFrame): DataFrame preprocesado de Marte.
        vars_luna (list[str]): Variables a correlacionar del dataset Luna.
        vars_marte (list[str]): Variables a correlacionar del dataset Marte.

    Returns:
        None
    """
    corr_luna  = df_luna[vars_luna].corr()
    corr_marte = df_marte[vars_marte].corr()

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    sns.heatmap(corr_luna,  annot=True, fmt='.2f', cmap='coolwarm',
                square=True, ax=axes[0], vmin=-1, vmax=1)
    axes[0].set_title('Correlaciones — Luna', fontweight='bold')

    sns.heatmap(corr_marte, annot=True, fmt='.2f', cmap='coolwarm',
                square=True, ax=axes[1], vmin=-1, vmax=1)
    axes[1].set_title('Correlaciones — Marte', fontweight='bold')

    plt.suptitle('Comparativa de correlaciones entre planetas', fontsize=13)
    plt.tight_layout()
    plt.show()


# ---------------------------------------------------------------------------
# Funciones auxiliares privadas
# ---------------------------------------------------------------------------

def _validar_columnas(df: pd.DataFrame, variables: list) -> None:
    faltantes = [v for v in variables if v not in df.columns]
    if faltantes:
        raise ValueError(
            f"Columnas no encontradas en el DataFrame: {faltantes}\n"
            f"Columnas disponibles: {list(df.columns)}"
        )
