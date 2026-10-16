# Gestión con GitHub Flow

## Historial y primera corrección

La revisión original partió de b889ae3. Sus 38 commits alcanzables desde main no permitían acreditar por sí solos el trabajo continuo en ramas. No se afirma que nunca existieran otras ramas ni se reconstruye un historial anterior.

La corrección se desarrolló en correccion/audiencias-semana9 con cuatro commits reales: datos y KPIs, Python y D3, Power BI y documentación. Se publicó la rama y se abrió la pull request #1. GitHub confirma su integración en main mediante 5596b6d:

https://github.com/vicezepeda/STREAMVIEW-ANALYTICS/pull/1

## Revisión final de la entrega

La rama correccion/revision-final-entrega parte del main integrado. Corrige el cuaderno, los accesos Python y la documentación, actualiza las dependencias comprobadas y conserva evidencias de las pruebas. La publicación y revisión de esta rama se realizan sin forzar push ni reescribir commits anteriores.

Flujo utilizado: crear rama desde main, realizar cambios reales, probar, registrar commits, publicar, abrir una pull request, revisar e integrar. Cada commit conserva su fecha real. Los commits actuales no sustituyen avances que debieron registrarse durante el semestre.

## Recuperar el historial incluido

El ZIP de entrega conserva los archivos y StreamView_Historial.bundle conserva commits y ramas. Desde una terminal situada junto al bundle:

```bash
git clone StreamView_Historial.bundle STREAMVIEW-ANALYTICS
cd STREAMVIEW-ANALYTICS
git remote set-url origin https://github.com/vicezepeda/STREAMVIEW-ANALYTICS.git
git switch correccion/revision-final-entrega
git log --oneline --decorate -8
```

El bundle no incluye credenciales ni publica automáticamente. Antes de integrar, revisar los cambios y las observaciones de Power BI indicadas en VALIDACION.md.
