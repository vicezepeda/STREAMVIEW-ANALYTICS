# StreamView Analytics

Proyecto individual de Visualización de Datos ADY1104. Entrega revisada el 16 de octubre de 2026.

| Audiencia | Herramienta | Archivo |
|---|---|---|
| Directorio y Gerencia General | Python, Streamlit, Plotly y D3 | dashboard/dashboard.py |
| Contenidos y Adquisición | Power BI Desktop | powerbi/StreamView_Contenidos.pbix |

## Abrir Python en Windows

1. Extraer todos los archivos y conservar la estructura de carpetas.
2. Hacer doble clic en ABRIR_PYTHON.cmd desde esta carpeta.
3. Mantener abierta la terminal. El navegador abre la dirección local indicada, normalmente http://localhost:8501. Si está ocupada, el acceso selecciona otro puerto libre hasta 8510.

El acceso busca Python 3.11 o superior. También reconoce el runtime de Codex si está instalado en este equipo. Si faltan paquetes, prepara un entorno .venv e instala requirements.txt desde PyPI; ese primer paso necesita Internet. En otro computador se necesita Python instalado. No se incluyen ejecutables de Python ni entornos que dependan de rutas de otro equipo.

Alternativa desde una terminal situada en esta carpeta:

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python -m streamlit run dashboard/dashboard.py
```

En macOS/Linux, activar con `source .venv/bin/activate`. El dashboard utiliza datos ya procesados. D3 y la topología del mapa están incluidos localmente.

## Abrir Power BI

Abrir powerbi/StreamView_Contenidos.pbix. Contiene tres páginas para Contenidos y Adquisición: contenidos, países y participantes, y finanzas. Incluye los datos. Consultar powerbi/LEEME.md para el proyecto editable PBIP y sus límites. Comprobar visualmente sus filtros, interacciones y mapa en Desktop antes de exponer.

## Reproducir el análisis

```bash
python -m src.etl
python -m src.analisis
python -m src.visualizaciones
python -m src.storytelling
python -m unittest discover -s tests -v
```

El cuaderno notebooks/01_Analisis_Exploratorio_StreamView.ipynb usa el mismo catálogo limpio. Las figuras estáticas se guardan en visualizaciones/. Jupyter es opcional y no se necesita para ejecutar el dashboard.

## Datos y criterios

Data_Movies.zip contiene los dos CSV originales. El catálogo limpio tiene 31.991 títulos: 16.000 películas y 15.991 series, después de eliminar nueve duplicados por tipo + show_id. Los show_id pueden repetirse entre tipos.

Cada título se cuenta una sola vez dentro de cada país o género. Finanzas utiliza 3.523 películas con presupuesto e ingresos de al menos USD 1.000 en ambos campos: cobertura 22,02% y ROI agregado aproximado 191,68%. La política de USD 1.000 es un criterio de limpieza del proyecto y debe revisarse frente a la fuente original. El ROI no incluye todos los costos ni representa el beneficio de StreamView.

La distribución por año de estreno es casi uniforme. Popularidad y votos no equivalen a reproducciones. No hay información utilizable de usuarios, retención, churn, clasificación etaria o duración.

## GitHub Flow

La rama correccion/audiencias-semana9 se publicó y la pull request #1 se integró en main (5596b6d):
https://github.com/vicezepeda/STREAMVIEW-ANALYTICS/pull/1

La integración de la primera corrección en main está verificada. La revisión final de esta entrega se desarrolla en correccion/revision-final-entrega. Se conserva el historial original y las fechas reales de esta corrección. Ver docs/GITHUB_FLOW.md. El paquete de entrega contiene un bundle con el historial Git.

## Organización

- data/: fuentes y catálogo común.
- src/: preparación, filtros, métricas y análisis.
- dashboard/: interfaz Python, D3 y mapa local.
- powerbi/: PBIX, PBIP y medidas DAX.
- notebooks/: análisis exploratorio consistente con los dashboards.
- visualizaciones/: gráficos estáticos exportados.
- tests/: pruebas automáticas.
- docs/: arquitectura, requisitos y documentación.

El paquete final separa informe y presentación en carpetas numeradas. Las versiones anteriores del repositorio son antecedentes y no se incluyen como documentos finales en el paquete de entrega.
