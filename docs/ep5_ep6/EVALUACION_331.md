# Evaluación crítica aplicada al proyecto

Base: 3.3.1 PPT Evaluación Crítica de las Visualizaciones, páginas 5, 10-11 y 13-18. Se adapta el framework al catálogo StreamView.

| Paso | Hallazgo | Consecuencia o mejora |
|---|---|---|
| 1. Objetivo | Dirección necesita comprender la oferta. Contenidos necesita comparar candidatos para revisión editorial. El catálogo no permite medir retención ni engagement. | Acotar los KPIs al catálogo y distinguir hipótesis de inversión de decisiones de compra. |
| 2. Datos | Se integran dos CSV, se eliminan nueve duplicados por tipo + show_id y se excluyen valoraciones no utilizables. La instantánea llega hasta 2025 y no incluye consumo ni licencias. | Mostrar denominadores, corte y cobertura. Revisar la fuente de montos extremos. |
| 3. Representación | Barras desde cero, calificaciones sobre 10, líneas con símbolos y trazos distintos, tablas de datos y colores de mayor contraste. El treemap aporta exploración de volumen. | Usar barras para comparar con precisión y el mapa para localizar, con una alternativa tabular. |
| 4. Interpretación | Más títulos no significa mayor demanda. Un ROI de producción no equivale a beneficio de la plataforma. La asociación observada no demuestra causalidad. | Acompañar cada hallazgo con población, limitación y decisión permitida por la evidencia. |
| 5. Mejora | Se reorganizaron KPIs, se añadió Géneros por tipo, un mínimo de muestra ajustable, exportación y datos alternativos a D3. | Verificar los cambios en ejecución y priorizar consumo, licencias y pruebas con usuarios reales. |

## Errores analíticos, comunicación y sesgos

| Tema del documento | Riesgo del proyecto | Mitigación |
|---|---|---|
| KPI o pregunta poco pertinente | Usar total de títulos como evidencia de retención o elegir adquisiciones solo por volumen. | El total describe oferta. Se requiere consumo por usuario para evaluar retención. |
| Exceso de información y contexto insuficiente | Muchos KPIs compiten por atención y un promedio sin n puede parecer más sólido de lo que es. | Seis KPIs principales, indicadores secundarios desplegables, filtros activos y tamaños de muestra. |
| Escalas y color | Un eje truncado o un color poco visible exagera o esconde diferencias. | Barras desde cero, nota 0 a 10, color más oscuro y etiquetas. Contraste medido; sin certificación integral de accesibilidad. |
| Comparaciones injustas | Películas y series tienen distintas valoraciones, taxonomías y condiciones de licencia. | Separar tipos y conservar las categorías de origen. Mínimos 50 y 30 votos y n visible. |
| Cherry picking y selección | Los ejemplos rentables y los rankings pueden ocultar pérdidas. La muestra financiera representa solo 22,02% de las películas. | Conservar el catálogo completo, mostrar cobertura y permitir exportar. Los ejemplos no estiman el éxito futuro. |
| Sobreinterpretación y datos incompletos | Confundir correlación con causa o ROI aproximado con beneficio. Los votos favorecen títulos ya conocidos. | Separar tipos, informar Pearson y Spearman y contrastar con costos y consumo antes de decidir. |

## Mejoras implementadas

| Antes | Después | Evidencia |
|---|---|---|
| Géneros combinados para recomendar | Comparación y tabla por tipo, con n y mínimo ajustable. | Animation: películas 7,00 (1.226), series 7,65 (1.022). |
| Nueve KPIs visibles al mismo nivel | Seis principales y cuatro secundarios en un desplegable. | Total, tipos, nota, mediana y valoraciones válidas se distinguen del contexto. |
| Naranja claro sobre blanco | Naranja #A34B00 y azul #1F4E79. | Contraste naranja/blanco: 2,42:1 antes y 5,89:1 después. |
| Distinguir series solo por color | Símbolos y trazos distintos en líneas, patrones en barras por tipo. | La leyenda y el tipo siguen identificables sin depender solo del color. |
| Lectura dependiente del cursor | Tabla de géneros, descarga CSV y datos alternativos de D3. | Se puede consultar el valor exacto y revisar los datos fuera del gráfico. |

## Mejoras priorizadas

| Prioridad | Mejora | Justificación |
|---|---|---|
| P1: validar candidatos | Consumo y costos de licencia por título y territorio. | Esfuerzo alto. Resuelve la principal falta de evidencia para comprar. |
| P2: datos y clasificación | Auditar ROI extremos, actualizar la instantánea y añadir clasificación etaria válida. | Esfuerzo medio. Mejora cobertura y permite segmentar sin inventar datos. |
| P2: prueba con usuarios | Observar a cinco usuarios en tareas de filtro, comparación y exportación. | Esfuerzo bajo. Medir éxito, errores y tiempo antes y después. |
| P3: accesibilidad completa | Revisar teclado, lector de pantalla, zoom y daltonismo en ambos productos. | Esfuerzo medio. La revisión de color no cubre todas las necesidades. |

## Impacto esperado y cómo medirlo

Se espera que mostrar tipos, n y cobertura reduzca comparaciones equivocadas y favorezca listas de candidatos trazables. Es una hipótesis de utilidad, no un aumento demostrado de ingresos o retención. La prueba propuesta con cinco usuarios registrará éxito sin ayuda en filtrar películas, comparar Animation y Documentary y exportar datos, tiempo por tarea y errores de interpretación. Se propone como meta inicial que al menos cuatro de cinco usuarios completen cada tarea sin ayuda; no se presenta esta meta como resultado obtenido. No se han realizado entrevistas ni pruebas con usuarios externos.

## Accesibilidad: alcance real

Se calcularon contrastes de colores definidos contra blanco y se añadieron texto, símbolos, patrones y tablas. El naranja nuevo alcanza 5,89:1 y el azul 8,66:1. Estas medidas no certifican conformidad completa de la interfaz con WCAG. Queda pendiente una auditoría integral con lector de pantalla y usuarios con necesidades diversas.

Referencias técnicas: https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html y https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html
