# Dashboard para Contenidos y Adquisición

Abrir StreamView_Contenidos.pbix en Power BI Desktop. Es el producto para la segunda audiencia. Los datos están incorporados.

## Páginas

1. Contenidos y Adquisición: dispersión, ranking con 1.000 votos, barras de popularidad y calificación por género y treemap.
2. Países y participantes: actores, directores, mapa de calificación por país con mínimo de 30 títulos con votos suficientes e idiomas.
3. Finanzas para adquisición: KPIs, presupuesto e ingresos, ROI, top por ingresos y títulos de presupuesto reducido.

Filtros: tipo, rango de años, género, país, idioma y rango de calificación. La clasificación etaria no existe en la fuente.

## Datos y edición

El PBIX incorpora la misma instantánea de 31.991 títulos que data/processed/catalogo_limpio.csv. Finanzas utiliza 3.523 películas con ambos montos >= USD 1.000. ROI agregado inicial: 191,68%.

El PBIP permite editar el informe y el modelo como texto. Sus consultas M incluyen esta instantánea. Al abrir el PBIP por primera vez, actualizar las consultas para cargar datos. Actualizar no obtiene registros futuros: para eso hay que cambiar el origen y guardar nuevamente el PBIX.

El mapa Azure requiere Internet y disponibilidad en Power BI. Verificar mapas e interacciones manualmente antes de exponer. La validación JSON y de medidas no sustituye esa prueba visual.
