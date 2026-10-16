# Validación de la entrega

Revisión del 16 de octubre de 2026.

## Comprobaciones realizadas

- Doce pruebas automáticas aprobadas con `python -m unittest discover -s tests -v`.
- Los CSV originales reproducen el catálogo entregado: 31.991 títulos únicos, después de nueve duplicados eliminados.
- El cuaderno completo ejecutó sus cinco celdas de código sin errores. Utiliza el mismo catálogo limpio y las mismas métricas del dashboard.
- Se ejecutaron preparación, resumen, narrativa y exportación de siete figuras estáticas.
- Python y D3 comprobados en navegador. D3 cambia entre cantidad y calificación y muestra valores al pasar el cursor. El mapa ejecutivo utiliza topología local.
- El PBIX se abrió en Power BI Desktop. Las 52 consultas del modelo abierto respondieron correctamente. Sus KPIs coinciden con Python: 31.991 títulos, 16.000 películas, 15.991 series, muestra financiera de 3.523, cobertura 22,01875% y ROI agregado aproximado 191,682234%.
- Las definiciones PBIR cumplen los esquemas JSON oficiales de Microsoft. Se comprobó la integridad del contenedor PBIX.
- Las ocho páginas del informe y doce diapositivas se renderizaron y revisaron visualmente. Los gráficos de la presentación permanecen editables.
- La pull request #1 está integrada en main mediante 5596b6d. La revisión final conserva una rama separada.

## Límites de la comprobación

La captura de pantalla de Power BI Desktop falló con `FrameArrived timed out`. La lectura de accesibilidad tampoco permitió inspeccionar sus visuales. Por ello sigue pendiente comprobar manualmente las tres páginas, los filtros, las interacciones y Azure Maps. Las consultas correctas y los esquemas válidos no sustituyen esa revisión visual.

Las capturas incluidas corresponden al navegador Python y a GitHub. Los gráficos analíticos del PDF y PowerPoint se reproducen con los datos y criterios del PBIX; no son capturas de Desktop.

No existe clasificación etaria utilizable en la fuente. El requisito correspondiente se documenta como limitación y debe validarse con la docente. Los datos financieros son parciales y el ROI no representa la rentabilidad de StreamView.
