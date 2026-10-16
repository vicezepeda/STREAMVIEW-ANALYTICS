# Guía para la defensa individual de Vicente

La exposición dispone de 10 minutos y hasta 5 minutos de preguntas según EP4. El PowerPoint incluye un guion en las notas. Ensayar antes de exponer y mantener el ZIP extraído.

## Demostración breve

1. Abrir ABRIR_PYTHON.cmd. Mostrar 31.991 títulos, mediana 22,07 y calificación 6,63. Quitar Serie del filtro para mostrar 16.000 películas. Limpiar filtros.
2. Abrir Exploración D3 y cambiar cantidad por calificación promedio. Explicar que comparte los filtros de Python.
3. Abrir powerbi/StreamView_Contenidos.pbix. En Contenidos, seleccionar Drama: 14.769, 6,76 y 22,68. Volver a seleccionar para limpiar. Mostrar la página de países y finanzas. Explicar MUSD, cobertura 22,02% y ROI aproximado 191,68%.
4. Mostrar el repositorio, commits, ramas y PR. La rama correccion/kpis-evidencias-defensa contiene la última corrección. No afirmar que está en main mientras la nueva PR siga abierta.

## Si preguntan por el código Python

- dashboard/dashboard.py construye la interfaz. load_clean() carga el CSV. filter_catalog() aplica tipo, años y género. El DataFrame resultante alimenta todos los KPIs.
- src/prep.py une los CSV, limpia montos menores de USD 1.000 y elimina duplicados por tipo + show_id. explode() separa categorías y elimina repeticiones dentro de un título.
- src/metrics.py contiene las métricas compartidas. rated_catalog() exige votos > 0 y nota > 0 y <= 10. kpis_catalogo() calcula la mediana con median() y la nota simple con mean().
- src/respuestas_negocio.py forma muestras con votos suficientes y calcula correlaciones por tipo. Pearson describe asociación lineal. Spearman compara rangos. No demuestran causalidad.
- src/visualizaciones.py exporta figuras con Matplotlib. La figura f8 usa Seaborn para la dispersión por tipo.
- D3 recibe un JSON de los géneros filtrados y recalcula la escala y las barras al cambiar la medida.
- Streamlit facilita construir esta interfaz en Python. Dash sería otra alternativa para la misma aplicación. No se implementaron las dos.

## Respuestas clave

La nota antigua incluía ceros. Ahora se promedian 27.414 valoraciones utilizables: 6,63. Con mínimos 50/30 la nota es 6,65 y ponderada por votos 6,97. No son la misma métrica.

La popularidad tiene mediana 22,07 y media 42,63. Se eligió mediana para representar un catálogo con valores extremos.

El ROI = (ingresos totales - presupuesto total) / presupuesto total. Solo entran las mismas 3.523 películas en ambos totales. No representa beneficio de la plataforma.

La pauta plantea un contexto con usuarios y consumo, pero los archivos aportados son de catálogo. El proyecto limita sus conclusiones a esos datos. Falta clasificación etaria y no se inventa un filtro sin fuente.
