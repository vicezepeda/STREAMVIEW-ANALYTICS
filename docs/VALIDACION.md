# Validación y alcance de la entrega

Revisión del 16 de octubre de 2026.

## Evidencia verificable

- 14 pruebas automáticas aprobadas. Comando y salida completa en evidencias/pruebas_automaticas.txt.
- Catálogo: 31.991 títulos únicos, 16.000 películas y 15.991 series. Se eliminaron nueve duplicados por tipo + show_id.
- Notebook completo ejecutado: cinco celdas de código, sin errores.
- Ocho figuras exportadas con Matplotlib. La octava utiliza Seaborn para comparar la relación popularidad-calificación por tipo.
- Modelo nativo de Power BI: 52 consultas DAX correctas. Resultado completo en evidencias/consultas_powerbi.json. Las consultas acreditan el modelo, no las interacciones de la interfaz.
- Coincidencia de 11 indicadores entre Python y Power BI: evidencias/coincidencia_python_powerbi.csv. Incluye la nota 6,634187, mediana 22,071, ROI 191,682234% y Drama 14.769.
- Power BI Desktop: tres páginas renderizadas, mapa Azure visible, selección de Drama y filtro de tipo comprobados. Las capturas pbi_final_*.png son reales, sin redibujar visuales.
- La interacción de Drama actualiza los KPIs y resalta otras barras. El resaltado mantiene valores de contexto en algunos visuales. No se interpreta como que todas las barras cambien a un subconjunto.
- Python y D3 ejecutados en navegador con los KPIs corregidos. D3 cambia de cantidad a calificación promedio.
- PDF y presentación final renderizados e inspeccionados antes de empaquetar.

## Límites

Se comprobaron ejemplos de filtros e interacción, no todas sus combinaciones posibles. Azure Maps necesita conexión y disponibilidad del servicio. El PBIX incorpora una instantánea, no una actualización automática de nuevos registros.

Falta clasificación etaria utilizable en la fuente. No se puede afirmar cumplimiento total de ese filtro. No hay datos de consumo, usuarios, licencias o costos completos para inferir demanda, retención o beneficio de la plataforma. La cobertura financiera es 22,02% de las películas.

La calificación exige votos > 0 y nota > 0 y <= 10. Los umbrales de 50 votos en películas y 30 en series se aplican a la exploración de relaciones y comparaciones específicas. El ranking de mejor evaluados exige 1.000 votos.

La pauta menciona Streamlit, Dash, Matplotlib y Seaborn. Se usan Streamlit, Matplotlib y Seaborn, además de Plotly y D3. Dash se justifica como alternativa no implementada. La interpretación final de esa exigencia corresponde a la docente.
