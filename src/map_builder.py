"""
map_builder.py
==============
Módulo de construcción de mapas interactivos de cráteres planetarios con Folium.

Responsabilidades:
    - Generar mapas interactivos para la Luna y Marte.
    - Representar cráteres como marcadores proporcionales al diámetro.
    - Mostrar popups con las propiedades del cráter al hacer clic.
    - Exportar los mapas a ficheros HTML.

Uso:
    from src.map_builder import construir_mapa_luna, construir_mapa_marte

    mapa_luna  = construir_mapa_luna(df_luna,   max_crateres=500)
    mapa_marte = construir_mapa_marte(df_marte, max_crateres=500)

    # Mostrar en Jupyter/Colab
    display(mapa_luna)

    # Exportar a HTML
    mapa_luna.save('mapa_luna.html')
    mapa_marte.save('mapa_marte.html')
"""

import pandas as pd
import folium


# ---------------------------------------------------------------------------
# Constantes de configuración visual
# ---------------------------------------------------------------------------
RADIO_MIN     = 2       # Radio mínimo del marcador en píxeles
DIVISOR_RADIO = 50      # Divisor para escalar el diámetro al radio visual
OPACIDAD      = 0.6

# Tiles planetarios (OpenPlanetaryMap / NASA)
TILE_LUNA = (
    'https://s3.amazonaws.com/opmbuilder/301_moon/tiles/w/hillshaded-albedo/{z}/{x}/{y}.png',
    'LOLA/USGS'
)
TILE_MARTE = (
    'https://cartocdn-gusc.global.ssl.fastly.net/opmbuilder/api/v1/map/named/opm-mars-basemap-v0-1/all/{z}/{x}/{y}.png',
    'OpenPlanetaryMap'
)


def construir_mapa_luna(df: pd.DataFrame, max_crateres: int = 500) -> folium.Map:
    """
    Construye un mapa interactivo con los cráteres lunares.

    Los marcadores se escalan proporcionalmente al diámetro del cráter.
    Al hacer clic en un marcador se muestra un popup con sus propiedades.

    Args:
        df (pd.DataFrame): DataFrame preprocesado del dataset Luna.
            Debe contener: LAT_CIRC_IMG, LON_CIRC_IMG, DIAM_CIRC_IMG.
        max_crateres (int): Número máximo de cráteres a representar.
            Por defecto 500 (para rendimiento en notebook).

    Returns:
        folium.Map: Objeto mapa con los marcadores añadidos.
    """
    mapa = folium.Map(
        location=[0, 0],
        zoom_start=2,
        tiles=None,
    )
    # Tile de la Luna (OpenPlanetaryMap)
    tile_url, tile_attr = TILE_LUNA
    folium.TileLayer(
        tiles=tile_url,
        attr=tile_attr,
        name='Superficie lunar',
    ).add_to(mapa)

    # Normalizar longitudes de [0,360) a [-180,180) para Folium
    muestra = _normalizar_longitudes(df.head(max_crateres), ['LON_CIRC_IMG'])
    total   = len(muestra)

    for i, (_, row) in enumerate(muestra.iterrows()):
        radio       = max(RADIO_MIN, row['DIAM_CIRC_IMG'] / DIVISOR_RADIO)
        popup_html  = _popup_luna(row)

        folium.CircleMarker(
            location   = [row['LAT_CIRC_IMG'], row['LON_CIRC_IMG']],
            radius     = radio,
            color      = '#555555',
            fill       = True,
            fill_color = '#aaaaaa',
            fill_opacity = OPACIDAD,
            popup      = folium.Popup(popup_html, max_width=280),
            tooltip    = f"Ø {row['DIAM_CIRC_IMG']:.1f} km",
        ).add_to(mapa)

    print(f"[OK] Mapa lunar generado con {total} cráteres.")
    return mapa


def construir_mapa_marte(df: pd.DataFrame, max_crateres: int = 500) -> folium.Map:
    """
    Construye un mapa interactivo con los cráteres marcianos.

    Los marcadores se colorean en rojo si el cráter tiene capas geológicas
    (NUMBER_LAYERS > 0) y en azul en caso contrario.

    Args:
        df (pd.DataFrame): DataFrame preprocesado del dataset Marte.
            Debe contener: LATITUDE_CIRCLE_IMAGE, LONGITUDE_CIRCLE_IMAGE,
            DIAM_CIRCLE_IMAGE, DEPTH_RIMFLOOR_TOPOG, NUMBER_LAYERS.
        max_crateres (int): Número máximo de cráteres a representar.

    Returns:
        folium.Map: Objeto mapa con los marcadores añadidos.
    """
    mapa = folium.Map(
        location=[0, 0],
        zoom_start=2,
        tiles=None,
    )
    # Tile de Marte (OpenPlanetaryMap)
    tile_url, tile_attr = TILE_MARTE
    folium.TileLayer(
        tiles=tile_url,
        attr=tile_attr,
        name='Superficie marciana',
    ).add_to(mapa)

    # Leyenda de colores
    _agregar_leyenda_marte(mapa)

    # Normalizar longitudes de [0,360) a [-180,180) para Folium
    muestra = _normalizar_longitudes(df.head(max_crateres), ['LONGITUDE_CIRCLE_IMAGE'])

    for _, row in muestra.iterrows():
        radio      = max(RADIO_MIN, row['DIAM_CIRCLE_IMAGE'] / DIVISOR_RADIO)
        n_capas    = row.get('NUMBER_LAYERS', 0)
        tiene_capas = pd.notna(n_capas) and n_capas > 0
        color      = '#cc3300' if tiene_capas else '#0055aa'
        popup_html = _popup_marte(row)

        folium.CircleMarker(
            location     = [row['LATITUDE_CIRCLE_IMAGE'], row['LONGITUDE_CIRCLE_IMAGE']],
            radius       = radio,
            color        = color,
            fill         = True,
            fill_color   = color,
            fill_opacity = OPACIDAD,
            popup        = folium.Popup(popup_html, max_width=300),
            tooltip      = f"Ø {row['DIAM_CIRCLE_IMAGE']:.1f} km",
        ).add_to(mapa)

    print(f"[OK] Mapa marciano generado con {len(muestra)} cráteres.")
    return mapa


def exportar_mapas(mapa_luna: folium.Map, mapa_marte: folium.Map,
                   ruta_luna: str = 'mapa_luna.html',
                   ruta_marte: str = 'mapa_marte.html') -> None:
    """
    Exporta ambos mapas a ficheros HTML navegables.

    Los ficheros HTML generados pueden abrirse directamente en cualquier
    navegador web sin necesidad de Jupyter.

    Args:
        mapa_luna (folium.Map): Mapa lunar generado con construir_mapa_luna.
        mapa_marte (folium.Map): Mapa marciano generado con construir_mapa_marte.
        ruta_luna (str): Ruta de salida para el mapa lunar.
        ruta_marte (str): Ruta de salida para el mapa marciano.

    Returns:
        None
    """
    mapa_luna.save(ruta_luna)
    mapa_marte.save(ruta_marte)
    print(f"[OK] Mapa lunar guardado en  '{ruta_luna}'.")
    print(f"[OK] Mapa marciano guardado en '{ruta_marte}'.")


# ---------------------------------------------------------------------------
# Funciones privadas auxiliares
# ---------------------------------------------------------------------------

def _normalizar_longitudes(df: pd.DataFrame, cols_lon: list) -> pd.DataFrame:
    """Convierte longitudes de rango [0, 360) a [-180, 180) para Folium/Leaflet."""
    df = df.copy()
    for col in cols_lon:
        if col in df.columns:
            mask = df[col] > 180
            df.loc[mask, col] = df.loc[mask, col] - 360
    return df

def _popup_luna(row: pd.Series) -> str:
    nombre = row.get('CRATER_NAME', row.get('NAME', 'Sin nombre'))
    return f"""
    <div style="font-family: Arial, sans-serif; font-size: 12px; min-width: 200px;">
        <b style="font-size:14px;">🌕 Cráter lunar</b><br><hr style="margin:4px 0">
        <b>Nombre:</b> {nombre}<br>
        <b>Latitud:</b>  {row['LAT_CIRC_IMG']:.4f}°<br>
        <b>Longitud:</b> {row['LON_CIRC_IMG']:.4f}°<br>
        <b>Diámetro:</b> {row['DIAM_CIRC_IMG']:.2f} km<br>
        <b>Arco imagen:</b> {row.get('ARC_IMG', 'N/D')}<br>
        <b>Puntos borde:</b> {row.get('PTS_RIM_IMG', 'N/D')}
    </div>
    """


def _popup_marte(row: pd.Series) -> str:
    nombre = row.get('CRATER_NAME', row.get('NAME', 'Sin nombre'))
    profundidad = f"{row['DEPTH_RIMFLOOR_TOPOG']:.2f} km" if pd.notna(row.get('DEPTH_RIMFLOOR_TOPOG')) else 'N/D'
    n_capas = int(row['NUMBER_LAYERS']) if pd.notna(row.get('NUMBER_LAYERS')) else 'N/D'
    return f"""
    <div style="font-family: Arial, sans-serif; font-size: 12px; min-width: 220px;">
        <b style="font-size:14px;">🔴 Cráter marciano</b><br><hr style="margin:4px 0">
        <b>Nombre:</b> {nombre}<br>
        <b>Latitud:</b>  {row['LATITUDE_CIRCLE_IMAGE']:.4f}°<br>
        <b>Longitud:</b> {row['LONGITUDE_CIRCLE_IMAGE']:.4f}°<br>
        <b>Diámetro:</b>    {row['DIAM_CIRCLE_IMAGE']:.2f} km<br>
        <b>Profundidad:</b> {profundidad}<br>
        <b>Capas geológicas:</b> {n_capas}<br>
        <b>Error localización:</b> {row.get('ERR_CIRCLE_IMAGE', 'N/D')}
    </div>
    """


def _agregar_leyenda_marte(mapa: folium.Map) -> None:
    """Inyecta una leyenda de colores en el mapa marciano."""
    leyenda_html = """
    <div style="position: fixed; bottom: 30px; left: 30px; z-index: 1000;
                background: white; padding: 10px 14px; border-radius: 8px;
                border: 1px solid #ccc; font-family: Arial; font-size: 12px;">
        <b>Leyenda — Marte</b><br>
        <span style="color:#cc3300;">●</span> Con capas geológicas<br>
        <span style="color:#0055aa;">●</span> Sin capas geológicas<br>
        <i>Tamaño ∝ diámetro del cráter</i>
    </div>
    """
    mapa.get_root().html.add_child(folium.Element(leyenda_html))
