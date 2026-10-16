# Validación de la corrección

Se ejecutaron 11 pruebas automáticas mediante `python -m unittest discover -s tests -v`: todas aprobaron. Comprueban catálogo, filtros, muestra financiera, aplicación ejecutiva y estructura del PBIX. Las definiciones JSON del informe Power BI también se validaron contra sus esquemas.

En navegador se comprobó la carga de Streamlit, el filtro de películas (16.000), el reinicio (31.991), el mapa y el selector de medida del componente D3. Las capturas de `docs/evidencias/` corresponden a esa aplicación real.

El informe PDF de ocho páginas y las diez diapositivas se renderizaron y revisaron visualmente. Los gráficos analíticos de los documentos se reproducen con los datos y criterios del PBIX; no son capturas de Power BI Desktop.

Pendiente: abrir el PBIX en Power BI Desktop y comprobar visualmente sus páginas, filtros, interacciones y mapa Azure. La validación estructural no sustituye esa prueba. También quedan pendientes la publicación de la rama, la pull request y su integración remota.

Las advertencias de Streamlit sobre el componente HTML no impidieron las pruebas ni la interacción D3. Debe revisarse su compatibilidad al actualizar Streamlit.
