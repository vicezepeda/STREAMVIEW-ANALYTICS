# Corrección del feedback de semana 9

## Diagnóstico de la versión remota revisada

Base: commit b889ae3. El repositorio contiene un dashboard Streamlit denominado ejecutivo y ningún PBIX. El dashboard intenta leer `year`, aunque los CSV usan `release_year`. El historial disponible tiene 38 commits, una rama remota main y ningún merge. No demuestra por sí solo un flujo de trabajo en ramas.

## Asignación de audiencias

| Audiencia | Herramienta | Producto |
|---|---|---|
| Directorio y Gerencia General | Python con Streamlit y Plotly | dashboard/dashboard.py |
| Gerencia de Contenidos y Adquisición | Power BI Desktop | powerbi/StreamView_Contenidos.pbix |

D3 se integra como una vista complementaria de géneros dentro del dashboard Python. Comparte el catálogo filtrado. Finanzas pertenece a la audiencia de Contenidos y Adquisición en Power BI.

## Gestión de cambios

Las correcciones se desarrollan en la rama `correccion/audiencias-semana9` mediante commits correspondientes a cambios reales. Se conserva el historial original. Estos commits actuales no sustituyen la evidencia histórica de trabajo continuo que pidió la profesora. La rama se publicó y la pull request #1 se integró en main (5596b6d). La revisión final utiliza la rama correccion/revision-final-entrega.
