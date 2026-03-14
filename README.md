# 🪐 Sistema de Análisis Exploratorio de Cráteres Planetarios

Sistema interactivo para el análisis y visualización de cráteres de la **Luna** y **Marte** a partir de catálogos científicos del USGS.

---

## 📁 Estructura del proyecto

```
proyecto_crateres/
│
├── data/                          ← Colocar aquí los datasets CSV
│   ├── luna_crateres.csv
│   └── marte_crateres.csv
│
├── src/                           ← Módulos Python del sistema
│   ├── __init__.py                ← Exporta todas las funciones públicas
│   ├── data_loader.py             ← Carga y validación de datasets
│   ├── preprocessor.py            ← Limpieza y transformación de variables
│   ├── stats_analyzer.py          ← Estadísticos descriptivos e histogramas
│   ├── correlation_analyzer.py    ← Correlaciones y scatter plots
│   ├── plot_generator.py          ← Gráficos exploratorios y panel resumen
│   └── map_builder.py             ← Mapas interactivos con Folium
│
├── notebooks/                     ← Notebooks de análisis por planeta
│   ├── analisis_luna.ipynb
│   └── analisis_marte.ipynb
│
├── requirements.txt               ← Dependencias Python
└── README.md                      ← Este fichero
```

---

## ⚙️ Instalación

### 1. Clonar o descomprimir el proyecto

Coloca la carpeta `proyecto_crateres/` en tu entorno de trabajo.

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

O de forma individual:

```bash
pip install pandas numpy matplotlib seaborn folium
```

### 3. Añadir los datasets

Descarga los catálogos de cráteres y colócalos en la carpeta `data/`:

| Fichero                | Fuente                              |
|------------------------|-------------------------------------|
| `luna_crateres.csv`    | USGS Lunar Crater Database          |
| `marte_crateres.csv`   | USGS Mars Crater Consortium         |

---

## 🚀 Uso rápido

### Opción A — Notebooks (recomendado)

Abre el notebook del planeta que quieres analizar y ejecuta las celdas en orden:

```
notebooks/analisis_luna.ipynb    ← Análisis completo de la Luna
notebooks/analisis_marte.ipynb   ← Análisis completo de Marte
```

En **Google Colab**: sube la carpeta del proyecto o monta Google Drive.

### Opción B — Scripts Python

```python
import sys
sys.path.insert(0, 'ruta/a/proyecto_crateres')

from src.data_loader      import cargar_dataset
from src.preprocessor     import preprocesar_dataset
from src.stats_analyzer   import estadisticas_descriptivas, generar_histogramas, matriz_correlacion
from src.plot_generator   import panel_resumen
from src.map_builder      import construir_mapa_marte

# 1. Cargar
df = cargar_dataset('data/marte_crateres.csv', planeta='marte')

# 2. Preprocesar
df = preprocesar_dataset(df, planeta='marte')

# 3. Analizar
print(estadisticas_descriptivas(df, ['DIAM_CIRCLE_IMAGE', 'DEPTH_RIMFLOOR_TOPOG']))

# 4. Visualizar
generar_histogramas(df, ['DIAM_CIRCLE_IMAGE', 'DEPTH_RIMFLOOR_TOPOG'])
matriz_correlacion(df, ['log_diam', 'log_depth', 'has_layers'])
panel_resumen(df, planeta='marte')

# 5. Mapa interactivo
mapa = construir_mapa_marte(df, max_crateres=500)
mapa.save('mapa_marte.html')
```

---

## 📦 Documentación de módulos

---

### `data_loader.py`

Módulo de carga y validación de datasets.

#### `cargar_dataset(ruta_csv, planeta)`

Carga un dataset desde CSV y valida que contiene las columnas requeridas.

| Parámetro  | Tipo  | Descripción                          |
|------------|-------|--------------------------------------|
| `ruta_csv` | `str` | Ruta al fichero CSV                  |
| `planeta`  | `str` | `'luna'` o `'marte'`                 |

**Retorna:** `pd.DataFrame`

**Lanza:**
- `ValueError` — planeta no válido o columnas faltantes
- `FileNotFoundError` — fichero no encontrado

**Columnas requeridas:**

*Luna:* `LAT_CIRC_IMG`, `LON_CIRC_IMG`, `DIAM_CIRC_IMG`, `ARC_IMG`, `PTS_RIM_IMG`

*Marte:* `LATITUDE_CIRCLE_IMAGE`, `LONGITUDE_CIRCLE_IMAGE`, `DIAM_CIRCLE_IMAGE`, `DEPTH_RIMFLOOR_TOPOG`, `NUMBER_LAYERS`

```python
df_luna  = cargar_dataset('data/luna_crateres.csv',  planeta='luna')
df_marte = cargar_dataset('data/marte_crateres.csv', planeta='marte')
```

---

### `preprocessor.py`

Módulo de limpieza y transformación de variables.

#### `preprocesar_dataset(df, planeta)`

Elimina filas nulas y genera variables derivadas. No modifica el DataFrame original.

| Parámetro | Tipo            | Descripción              |
|-----------|-----------------|--------------------------|
| `df`      | `pd.DataFrame`  | DataFrame cargado        |
| `planeta` | `str`           | `'luna'` o `'marte'`     |

**Variables generadas:**

| Variable     | Planeta | Fórmula                            |
|--------------|---------|------------------------------------|
| `log_diam`   | ambos   | `log(1 + DIAM_*)`                  |
| `log_depth`  | Marte   | `log(1 + DEPTH_RIMFLOOR_TOPOG)`    |
| `has_layers` | Marte   | `1` si `NUMBER_LAYERS > 0`, si no `0` |
| `log_err`    | Marte   | `log(1 + ERR_CIRCLE_IMAGE)` (si existe) |

```python
df_luna  = preprocesar_dataset(df_luna,  planeta='luna')
df_marte = preprocesar_dataset(df_marte, planeta='marte')
```

---

### `stats_analyzer.py`

Módulo de análisis estadístico.

#### `estadisticas_descriptivas(df, variables)`

Calcula media, desviación estándar, percentiles (25, 50, 75), mínimo y máximo.

```python
stats = estadisticas_descriptivas(df_marte, ['DIAM_CIRCLE_IMAGE', 'DEPTH_RIMFLOOR_TOPOG'])
print(stats)
```

#### `generar_histogramas(df, variables, bins=50, color='steelblue', guardar_en=None)`

Genera histogramas de distribución para cada variable.

| Parámetro    | Tipo   | Descripción                                         |
|--------------|--------|-----------------------------------------------------|
| `variables`  | `list` | Lista de columnas a visualizar                      |
| `bins`       | `int`  | Número de intervalos. Por defecto `50`              |
| `guardar_en` | `str`  | Ruta para guardar la figura (opcional)              |

```python
generar_histogramas(df_marte, ['DIAM_CIRCLE_IMAGE', 'DEPTH_RIMFLOOR_TOPOG'])
generar_histogramas(df_luna,  ['DIAM_CIRC_IMG'], guardar_en='histograma_luna.png')
```

#### `matriz_correlacion(df, variables, guardar_en=None)`

Genera un mapa de calor de correlaciones de Pearson.

```python
matriz_correlacion(df_marte, ['log_diam', 'log_depth', 'has_layers'])
```

---

### `correlation_analyzer.py`

Módulo de análisis de correlaciones y scatter plots.

#### `calcular_correlacion(df, variables)`

Devuelve la matriz de correlación de Pearson como DataFrame.

```python
corr = calcular_correlacion(df_marte, ['log_diam', 'log_depth', 'has_layers'])
print(corr)
```

#### `scatter_plot(df, x, y, hue=None, titulo=None, guardar_en=None)`

Scatter plot entre dos variables con opción de colorear por una tercera.

```python
scatter_plot(df_marte, x='log_diam', y='log_depth', hue='has_layers')
```

#### `comparar_correlaciones(df_luna, df_marte, vars_luna, vars_marte)`

Muestra en paralelo las matrices de correlación de ambos planetas.

```python
comparar_correlaciones(
    df_luna,  ['log_diam'],
    df_marte, ['log_diam', 'log_depth', 'has_layers']
)
```

---

### `plot_generator.py`

Módulo de gráficos exploratorios avanzados.

#### `boxplot(df, variables, guardar_en=None)`

Diagramas de caja para detectar outliers.

```python
boxplot(df_marte, ['DIAM_CIRCLE_IMAGE', 'DEPTH_RIMFLOOR_TOPOG'])
```

#### `scatter_regresion(df, x, y, guardar_en=None)`

Scatter plot con línea de regresión lineal superpuesta.

```python
scatter_regresion(df_marte, x='log_diam', y='log_depth')
```

#### `panel_resumen(df, planeta, guardar_en=None)`

Panel 2×2 con los gráficos más relevantes del dataset (histogramas, scatter espacial, boxplot).

```python
panel_resumen(df_luna,  planeta='luna')
panel_resumen(df_marte, planeta='marte')
```

---

### `map_builder.py`

Módulo de mapas interactivos con Folium.

#### `construir_mapa_luna(df, max_crateres=500)`

Genera un mapa interactivo con los cráteres lunares.

- Marcadores grises escalados al diámetro del cráter.
- Popup con: nombre, coordenadas, diámetro, arco, puntos del borde.

```python
mapa = construir_mapa_luna(df_luna, max_crateres=300)
display(mapa)           # Mostrar en Jupyter/Colab
mapa.save('luna.html')  # Exportar a HTML
```

#### `construir_mapa_marte(df, max_crateres=500)`

Genera un mapa interactivo con los cráteres marcianos.

- **Rojo** → cráter con capas geológicas (`NUMBER_LAYERS > 0`)
- **Azul** → cráter sin capas geológicas
- Popup con: nombre, coordenadas, diámetro, profundidad, capas, error.

```python
mapa = construir_mapa_marte(df_marte, max_crateres=300)
display(mapa)
mapa.save('marte.html')
```

#### `exportar_mapas(mapa_luna, mapa_marte, ruta_luna, ruta_marte)`

Exporta ambos mapas a ficheros HTML navegables (sin necesidad de Jupyter).

```python
exportar_mapas(mapa_luna, mapa_marte,
               ruta_luna='output/luna.html',
               ruta_marte='output/marte.html')
```

---

## 🔄 Flujo de trabajo completo

```
CSV en data/
     │
     ▼
cargar_dataset()          ← Valida columnas y carga el DataFrame
     │
     ▼
preprocesar_dataset()     ← Elimina nulos, genera log_diam, log_depth, has_layers
     │
     ├──▶ estadisticas_descriptivas()   ← Tabla de estadísticos
     ├──▶ generar_histogramas()         ← Distribución de variables
     ├──▶ matriz_correlacion()          ← Mapa de calor correlaciones
     ├──▶ scatter_regresion()           ← Relación entre variables
     ├──▶ panel_resumen()               ← Panel 2×2 visual
     │
     └──▶ construir_mapa_luna/marte()   ← Mapa interactivo Folium
              │
              └──▶ .save('mapa.html')   ← Exportar a HTML
```

---

## 🐛 Problemas frecuentes

| Error | Causa | Solución |
|-------|-------|----------|
| `FileNotFoundError` | Ruta al CSV incorrecta | Comprueba que el CSV está en `data/` y que la ruta es correcta |
| `ValueError: columnas faltantes` | El CSV no tiene las columnas requeridas | Revisa el nombre de las columnas en el dataset original |
| `ModuleNotFoundError: folium` | Folium no instalado | Ejecuta `pip install folium` |
| El mapa no se muestra | Estás fuera de Jupyter | Exporta el mapa con `.save('mapa.html')` y ábrelo en el navegador |
| `KeyError` en preprocesar | Variable derivada ya existe | Usa siempre el DataFrame original (sin preprocesar) como entrada |

---

## 📋 Requisitos del sistema

- Python **3.8** o superior
- Jupyter Notebook / JupyterLab / Google Colab
- Conexión a internet solo para cargar los tiles del mapa en Folium

---