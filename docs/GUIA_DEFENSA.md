# Guía breve para la defensa individual

La presentación contiene notas del orador para aproximadamente diez minutos. Practicar sin leer todas las diapositivas.

## Recorrido

1. Explicar el problema y las dos audiencias.
2. Explicar las dos fuentes CSV, la clave tipo + show_id y los nueve duplicados.
3. En Python, filtrar películas: el total debe ser 16.000. Limpiar filtros: 31.991.
4. Abrir Exploración D3 y cambiar de cantidad a calificación.
5. En Power BI, mostrar el ranking y finanzas. Explicar cobertura 22,02% y ROI agregado aproximado 191,68%.
6. Mostrar el historial de Git y la PR #1 integrada. Indicar el estado real de la revisión final.
7. Recomendar completar datos y contrastar candidatos con consumo y costos de licencia.

## Preguntas sobre Python

- Pandas organiza las tablas. Streamlit crea la interfaz. Plotly dibuja gráficos interactivos. Pycountry convierte países a códigos geográficos. D3 dibuja el componente de géneros.
- df0 contiene todo el catálogo y df contiene la selección filtrada.
- filter_catalog recibe tipo, años y géneros y devuelve las filas que coinciden.
- len(df) cuenta títulos filtrados. df.calificacion.mean() calcula el promedio simple mostrado en pantalla.
- groupby agrupa filas y size cuenta registros por grupo.
- Streamlit vuelve a ejecutar el script al cambiar un filtro. st.cache_data conserva la carga de datos para evitar repetirla innecesariamente.
- prep.py prepara los CSV. metrics.py calcula indicadores. filters.py aplica filtros. dashboard/dashboard.py construye la interfaz.
- El componente D3 recibe una tabla agrupada como JSON. Python y Power BI son aplicaciones separadas.

## Límites que debes explicar

Popularidad y votos no son reproducciones. No hay datos de usuarios para retención o churn. El año de estreno es distinto del año de incorporación. Un título puede pertenecer a varios países o géneros, pero se cuenta una vez en cada categoría. El ROI utiliza solo películas con ambos datos financieros y no representa la rentabilidad de la plataforma.

Antes de exponer, comprobar manualmente las tres páginas del PBIX, filtros y mapa Azure. La ejecución en otra máquina requiere Python y dependencias; el acceso .cmd no incluye el intérprete.
