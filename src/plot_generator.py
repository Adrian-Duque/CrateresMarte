"""
plot_generator.py
=================
Módulo de generación de gráficos exploratorios para datasets de cráteres.

Responsabilidades:
    - Histogramas individuales y múltiples.
    - Diagramas de caja (boxplot) por variable.
    - Scatter plots con línea de regresión.
    - Panel de visualización resumen (dashboard estático).

Uso:
    from src.plot_generator import (
        boxplot,
        scatter_regresion,
        panel_resumen,
    )

    boxplot(df_marte, ['DIAM_CIRCLE_IMAGE', 'DEPTH_RIMFLOOR_TOPOG'])
    scatter_regresion(df_marte, x='log_diam', y='log_depth')
    panel_resumen(df_marte, planeta='marte')
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Configuración global de estilo
sns.set_theme(style='whitegrid', palette='muted')


def boxplot(
    df: pd.DataFrame,
    variables: list,
    guardar_en: str = None,
) -> None:
    """
    Genera diagramas de caja (boxplot) para detectar outliers y distribución.

    Args:
        df (pd.DataFrame): DataFrame preprocesado.
        variables (list[str]): Variables a visualizar.
        guardar_en (str | None): Ruta para guardar la figura.

    Returns:
        None
    """
    n = len(variables)
    fig, axes = plt.subplots(1, n, figsize=(4 * n, 5))
    if n == 1:
        axes = [axes]

    for ax, var in zip(axes, variables):
        ax.boxplot(df[var].dropna(), patch_artist=True,
                   boxprops=dict(facecolor='steelblue', alpha=0.6))
        ax.set_title(var, fontsize=10, fontweight='bold')
        ax.set_ylabel('Valor')
        ax.grid(axis='y', linestyle='--', alpha=0.5)

    plt.suptitle('Distribución por boxplot', fontsize=13)
    plt.tight_layout()
    _guardar_o_mostrar(guardar_en)


def scatter_regresion(
    df: pd.DataFrame,
    x: str,
    y: str,
    guardar_en: str = None,
) -> None:
    """
    Genera un scatter plot con línea de regresión lineal superpuesta.

    Útil para visualizar la relación diámetro–profundidad en cráteres marcianos.

    Args:
        df (pd.DataFrame): DataFrame preprocesado.
        x (str): Variable independiente (eje X).
        y (str): Variable dependiente (eje Y).
        guardar_en (str | None): Ruta para guardar la figura.

    Returns:
        None
    """
    fig, ax = plt.subplots(figsize=(8, 5))

    ax.scatter(df[x], df[y], alpha=0.3, s=8, color='steelblue', label='Datos')

    # Línea de regresión
    mask = df[[x, y]].dropna().index
    m, b = np.polyfit(df.loc[mask, x], df.loc[mask, y], 1)
    x_line = np.linspace(df[x].min(), df[x].max(), 200)
    ax.plot(x_line, m * x_line + b, color='red', linewidth=2, label=f'Regresión (m={m:.2f})')

    ax.set_xlabel(x)
    ax.set_ylabel(y)
    ax.set_title(f'Relación {x} → {y}', fontsize=12, fontweight='bold')
    ax.legend()
    ax.grid(linestyle='--', alpha=0.4)
    plt.tight_layout()
    _guardar_o_mostrar(guardar_en)


def panel_resumen(
    df: pd.DataFrame,
    planeta: str,
    guardar_en: str = None,
) -> None:
    """
    Genera un panel de visualización resumen (2×2) con las variables clave del dataset.

    Para Luna:
        - Histograma de diámetros
        - Histograma de log_diam
        - Scatter latitud vs longitud
        - Boxplot de diámetros

    Para Marte:
        - Histograma de diámetros
        - Histograma de profundidades
        - Scatter log_diam vs log_depth
        - Distribución de capas geológicas

    Args:
        df (pd.DataFrame): DataFrame preprocesado.
        planeta (str): 'luna' o 'marte'.
        guardar_en (str | None): Ruta para guardar la figura.

    Returns:
        None
    """
    fig, axes = plt.subplots(2, 2, figsize=(13, 9))
    fig.suptitle(f'Panel resumen — {planeta.capitalize()}', fontsize=14, fontweight='bold')

    if planeta == 'luna':
        axes[0, 0].hist(df['DIAM_CIRC_IMG'].dropna(), bins=50, color='slategray', edgecolor='black')
        axes[0, 0].set_title('Distribución de diámetros')
        axes[0, 0].set_xlabel('Diámetro (km)')

        axes[0, 1].hist(df['log_diam'].dropna(), bins=50, color='cornflowerblue', edgecolor='black')
        axes[0, 1].set_title('Distribución log(diámetro)')
        axes[0, 1].set_xlabel('log(1 + diámetro)')

        axes[1, 0].scatter(df['LON_CIRC_IMG'], df['LAT_CIRC_IMG'], s=1, alpha=0.3, color='dimgray')
        axes[1, 0].set_title('Distribución espacial')
        axes[1, 0].set_xlabel('Longitud')
        axes[1, 0].set_ylabel('Latitud')

        axes[1, 1].boxplot(df['DIAM_CIRC_IMG'].dropna(), patch_artist=True,
                           boxprops=dict(facecolor='steelblue', alpha=0.6))
        axes[1, 1].set_title('Boxplot de diámetros')

    elif planeta == 'marte':
        axes[0, 0].hist(df['DIAM_CIRCLE_IMAGE'].dropna(), bins=50, color='salmon', edgecolor='black')
        axes[0, 0].set_title('Distribución de diámetros')
        axes[0, 0].set_xlabel('Diámetro (km)')

        axes[0, 1].hist(df['DEPTH_RIMFLOOR_TOPOG'].dropna(), bins=50, color='sandybrown', edgecolor='black')
        axes[0, 1].set_title('Distribución de profundidades')
        axes[0, 1].set_xlabel('Profundidad (km)')

        axes[1, 0].scatter(df['log_diam'], df['log_depth'], s=2, alpha=0.3, color='firebrick')
        axes[1, 0].set_title('log(diámetro) vs log(profundidad)')
        axes[1, 0].set_xlabel('log_diam')
        axes[1, 0].set_ylabel('log_depth')

        capas = df['NUMBER_LAYERS'].value_counts().sort_index()
        axes[1, 1].bar(capas.index.astype(str), capas.values, color='peru', edgecolor='black')
        axes[1, 1].set_title('Distribución de capas geológicas')
        axes[1, 1].set_xlabel('Número de capas')
        axes[1, 1].set_ylabel('Frecuencia')

    for ax in axes.flat:
        ax.grid(linestyle='--', alpha=0.4)

    plt.tight_layout()
    _guardar_o_mostrar(guardar_en)


# ---------------------------------------------------------------------------
# Función auxiliar interna
# ---------------------------------------------------------------------------

def _guardar_o_mostrar(guardar_en: str) -> None:
    if guardar_en:
        plt.savefig(guardar_en, bbox_inches='tight', dpi=150)
        print(f"[OK] Figura guardada en '{guardar_en}'.")
    else:
        plt.show()
