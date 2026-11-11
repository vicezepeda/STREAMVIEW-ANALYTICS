# Comprobaciones de Python en ejecución

Revisión y capturas del 9 de noviembre de 2026. Empaquetado final: 11 de noviembre. Aplicación del repositorio, servida localmente en el puerto 8503 durante la revisión.

- Inicio: 31.991 títulos; 16.000 películas; 15.991 series; nota 6,63; mediana 22,07; 27.414 valoraciones utilizables. Seis indicadores principales y cuatro secundarios desplegables.
- Géneros por tipo: mínimo 100, gráficas separadas con escala 0 a 10. Animation: películas 7,00 (1.226), series 7,65 (1.022). Documentary: películas 7,20 (542), series 7,50 (129). Captura dashboard_ep5_generos.png.
- Mínimo 2.000: se excluyen géneros con muestras menores. Quedan Drama en series y los géneros de películas que superan el umbral. Captura dashboard_ep5_minimo.png.
- Limpiar filtros devuelve el mínimo a 100. El navegador confirmó el valor después de terminar la actualización. Las pruebas comprueban también el reinicio del tipo y el total a 31.991.
- D3: cambio de Cantidad de títulos a Calificación promedio, con eje 0 a 10, y apertura de Ver los datos del gráfico D3.
- Descarga real de la comparación CSV. comparacion_descargada.csv coincide con generos_por_tipo.csv (comparación de columnas, filas y valores; tolerancia numérica estándar de pandas).
- Distribución a 768 x 900: KPIs en dos filas; pestañas y control de mínimo visibles; ancho del contenido 758 y ancho desplazable 758, sin desbordamiento horizontal del contenedor principal. Captura dashboard_ep5_768.png. Se retiró el tamaño temporal al terminar.
- El mensaje de muestra insuficiente para Serie / Documentary / mínimo 2.000 se comprueba en test_genre_sample_threshold_handles_empty_results. No se presenta como una captura manual de ese estado.

Estas comprobaciones cubren los estados descritos. No equivalen a una auditoría completa de accesibilidad o a una prueba con usuarios externos. Las consultas DAX y las capturas de Power BI se conservan como evidencia de octubre; no se afirma una nueva revisión de Desktop en noviembre.
