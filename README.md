# StreamView Analytics: EP5 y EP6

Visualización de Datos ADY1104. Presenta Vicente Zepeda Rojas. Revisión: 9 de noviembre de 2026.

## Ejecutar el dashboard

Extraer el ZIP completo y hacer doble clic en ABRIR_PYTHON.cmd. Conservar las carpetas. Se necesita Python 3.11 o superior. El acceso prepara .venv e instala requirements.txt si faltan módulos; ese primer inicio requiere Internet. Mantener la terminal abierta.

Alternativa desde esta carpeta:

```bash
python -m pip install -r requirements.txt
python -m streamlit run dashboard/dashboard.py
```

Power BI: abrir powerbi/StreamView_Contenidos.pbix. Los datos están incorporados. Azure Maps requiere Internet y disponibilidad del servicio. El PBIP y las medidas DAX se incluyen para edición.

## Audiencias

Dirección utiliza Python, Streamlit, Plotly y D3 para explorar catálogo y comparaciones por tipo. Contenidos y Adquisición utiliza las tres páginas de Power BI para títulos, participantes y finanzas. Un clic en una aplicación no filtra la otra.

## Mejoras EP5/EP6

Seis KPIs principales y cuatro secundarios desplegables. Nueva vista Géneros por tipo con mínimo de muestra, tablas y CSV. Colores más contrastantes, líneas con símbolos y trazos distintos, barras con patrones por tipo y tabla alternativa de D3. La crítica aplica los cinco pasos y los sesgos del documento 3.3.1. Ver docs/ep5_ep6/.

Animation en películas: 7,00 (1.226), Documentary: 7,20 (542). Animation en series: 7,65 (1.022), Documentary: 7,50 (129). Las comparaciones editoriales usan nota válida y mínimos de 50 votos en películas y 30 en series. Cada título cuenta una vez dentro de su género; las categorías pueden ser múltiples.

## Datos y KPIs

Dos CSV originales en data/raw/Data_Movies.zip. Catálogo limpio: 31.991 títulos, 16.000 películas y 15.991 series, tras eliminar nueve duplicados por tipo + show_id. La nota general 6,63 usa 27.414 valoraciones válidas. Popularidad mediana 22,07 y media 42,63. Finanzas: 3.523 películas con ambos montos >= USD 1.000, cobertura 22,02% y ROI agregado aproximado 191,68%. El ROI no representa beneficio de StreamView. No hay datos utilizables de consumo, retención, clasificación etaria o costos de licencia.

## Reproducir

```bash
python -m src.etl
python -m src.analisis
python -m src.respuestas_negocio
python -m src.visualizaciones
python -m src.comparacion_tipos
python -m unittest discover -s tests -v
```

El notebook se puede ejecutar desde notebooks/ o la raíz. Jupyter es opcional y no se necesita para abrir el dashboard.

## Estructura

- data/: fuentes ZIP, catálogo limpio, resúmenes y comparación de géneros.
- notebooks/: exploración ejecutada y comparación por tipo.
- dashboard/: interfaz, D3 y topología local del mapa.
- images/: figuras actuales y capturas de la versión optimizada.
- src/: preparación, filtros, métricas, diseño y análisis.
- powerbi/: PBIX, PBIP, modelo y DAX.
- tests/: pruebas de datos, filtros, interfaz y contenedor PBIX.
- docs/ep5_ep6/: evaluación 3.3.1, matriz de pauta, narrativa, guía y evidencias actuales.
- entregables/: informe, resumen y presentación final cuando se consulta el repositorio.

En el paquete de entrega, informe, resumen y presentación están fuera del código, en carpetas numeradas.

## Evidencias y GitHub

Las 16 pruebas automáticas tienen salida completa en docs/ep5_ep6/evidencias/pruebas_automaticas.txt. El notebook tiene seis celdas de código ejecutadas. Los archivos de coincidencia entre Python y Power BI y las 52 consultas al modelo se conservan como evidencia de la revisión del 16 de octubre. Las capturas reales del PBIX son de esa misma revisión. La nueva versión de Python se comprueba y captura en noviembre.

Se utiliza GitHub Flow. PR #1, #2 y #3 integradas. Esta entrega se prepara en mejora/ep5-ep6 con commits de cambios reales y una nueva PR hacia main. Ver docs/ep5_ep6/GITHUB_FLOW.md. No se reconstruye un supuesto historial de trabajo del semestre.
