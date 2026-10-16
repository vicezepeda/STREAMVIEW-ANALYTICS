# StreamView Analytics

Proyecto individual de Visualización de Datos ADY1104. Esta revisión separa las dos audiencias de la pauta de semana 9.

| Audiencia | Implementación | Archivo para demostrar |
|---|---|---|
| Directorio y Gerencia General | Python, Streamlit y Plotly | dashboard/dashboard.py |
| Gerencia de Contenidos y Adquisición | Power BI Desktop | powerbi/StreamView_Contenidos.pbix |

D3 es una visualización complementaria de géneros dentro del dashboard Python. Recibe los datos filtrados y permite cambiar la medida y consultar valores al pasar el cursor.

## Ejecutar Python

Desde la raíz del proyecto, con Python 3.11 o superior:

```bash
python -m venv .venv
```

Activar el entorno en Windows con `.venv\Scripts\activate`, o en macOS/Linux con `source .venv/bin/activate`.

```bash
python -m pip install -r requirements.txt
python src/etl.py
python -m streamlit run dashboard/dashboard.py
```

La preparación lee los CSV originales si están disponibles o data/raw/Data_Movies.zip. El catálogo limpio se incluye para facilitar la ejecución.

Python muestra los KPIs ejecutivos, estrenos e incorporaciones por año, países, géneros, distribución de tipos, mapa coroplético e idiomas. Tipo, años y género afectan todas sus vistas. El mapa y D3 utilizan archivos locales.

## Abrir Power BI

Abrir powerbi/StreamView_Contenidos.pbix. Las páginas Contenidos y Adquisición, Países y participantes y Finanzas para adquisición pertenecen a la misma audiencia analítica. El PBIX incluye datos y medidas.

El PBIP y las carpetas de modelo e informe permiten revisar cambios de texto en Git. Ver powerbi/LEEME.md. El mapa Azure requiere Internet y disponibilidad en Power BI. Comprobar visuales e interacciones en Desktop antes de exponer.

## Datos comunes

- 32.000 filas originales y 31.991 títulos únicos después de eliminar nueve duplicados dentro del mismo tipo.
- 16.000 películas y 15.991 series. Clave: tipo más show_id.
- Cada título se cuenta una vez por categoría de género, país o participante.
- Finanzas: películas con presupuesto e ingresos >= USD 1.000, sobre la misma muestra pareada.
- Muestra financiera: 3.523 películas, cobertura inicial 22,02%, ROI agregado aproximado 191,68%.
- La distribución por año de estreno es casi uniforme. No demuestra crecimiento real del catálogo.
- Sin datos de usuarios no se calculan retención ni churn. La clasificación etaria no existe en la fuente.

## Verificación

```bash
python -m unittest discover -s tests -v
```

Las pruebas cubren claves, finanzas, filtros, categorías, Streamlit y estructura del PBIX. Las evidencias de navegador están en docs/evidencias/. La validación de medidas y JSON no sustituye la revisión visual de Power BI.

## GitHub Flow

La corrección se desarrolla en correccion/audiencias-semana9 mediante commits de cambios reales. El historial original se conserva. No se reconstruyen fechas ni avances pasados. Ver docs/GITHUB_FLOW.md para publicar la rama, abrir una pull request y dirigir los cambios a main.

## Organización

```text
data/        Datos originales y catálogo común
src/         Preparación, métricas y filtros
dashboard/   Dashboard ejecutivo Python y componente D3
powerbi/     Dashboard analítico PBIX, proyecto PBIP y medidas
tests/       Comprobaciones de datos y entregables
docs/        Arquitectura, requisitos y evidencias
```

Los documentos anteriores que permanecen en docs son antecedentes. La entrega corregida se identifica por el sufijo Semana9.
