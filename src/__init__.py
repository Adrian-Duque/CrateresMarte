"""
src — Paquete principal del sistema de análisis de cráteres planetarios.

Módulos disponibles:
    data_loader          → Carga y validación de datasets CSV.
    preprocessor         → Limpieza y transformación de variables.
    stats_analyzer       → Estadísticos descriptivos e histogramas.
    correlation_analyzer → Matrices de correlación y scatter plots.
    plot_generator       → Gráficos exploratorios y panel resumen.
    map_builder          → Mapas interactivos con Folium.
"""

from .data_loader          import cargar_dataset
from .preprocessor         import preprocesar_dataset
from .stats_analyzer       import estadisticas_descriptivas, generar_histogramas, matriz_correlacion
from .correlation_analyzer import calcular_correlacion, scatter_plot, comparar_correlaciones
from .plot_generator       import boxplot, scatter_regresion, panel_resumen
from .map_builder          import construir_mapa_luna, construir_mapa_marte, exportar_mapas

__all__ = [
    'cargar_dataset',
    'preprocesar_dataset',
    'estadisticas_descriptivas',
    'generar_histogramas',
    'matriz_correlacion',
    'calcular_correlacion',
    'scatter_plot',
    'comparar_correlaciones',
    'boxplot',
    'scatter_regresion',
    'panel_resumen',
    'construir_mapa_luna',
    'construir_mapa_marte',
    'exportar_mapas',
]
