# Gestión del repositorio con GitHub Flow

Repositorio: https://github.com/vicezepeda/STREAMVIEW-ANALYTICS

Se trabaja en una rama, se realizan commits de cambios concretos y se abre una pull request hacia main. La integración se mantiene como una decisión del propietario después de revisar el cambio.

| Corrección | Rama | Pull request | Estado verificado |
|---|---|---|---|
| Dos audiencias y herramientas | correccion/audiencias-semana9 | https://github.com/vicezepeda/STREAMVIEW-ANALYTICS/pull/1 | Integrada, 5596b6d |
| Ejecución reproducible y revisión anterior | correccion/revision-final-entrega | https://github.com/vicezepeda/STREAMVIEW-ANALYTICS/pull/2 | Integrada, 75d259a |
| KPIs, capturas reales y defensa | correccion/kpis-evidencias-defensa | https://github.com/vicezepeda/STREAMVIEW-ANALYTICS/pull/3 | Abierta al preparar esta entrega |

La tercera corrección parte de origin/main después de la integración de la PR #2. Se separan los commits de métricas y análisis, ajustes de legibilidad de Power BI, evidencias y documentos finales. Las fechas son reales y no se reconstruye un supuesto historial del semestre.

Las credenciales de GitHub no se incluyen en el proyecto. El bundle del paquete conserva el historial. Los archivos github_estado.json y github_pr_actual.json registran respuestas resumidas de la API. La captura github_pr3.png muestra la PR en el navegador.

La versión de la entrega está en la rama de la PR #3. Si la PR sigue abierta, entregar solo la URL de main omite esta corrección. Usar el enlace de la rama y de la PR o revisar e integrar la PR antes de compartir main.
