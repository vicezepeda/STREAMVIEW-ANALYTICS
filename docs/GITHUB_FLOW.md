# Gestión con GitHub Flow

## Historial original

Al revisar b889ae3 se encontraron 38 commits alcanzables desde main, una rama remota disponible y ningún commit de merge. Esa evidencia no permite acreditar por sí sola el trabajo continuo en ramas solicitado por la profesora. Las ramas anteriores pudieron eliminarse o integrarse de otra forma; no se afirma que nunca existieran.

## Corrección actual

1. Partir de main y crear correccion/audiencias-semana9.
2. Corregir preparación y métricas. Probar y registrar el cambio.
3. Implementar y comprobar Python ejecutivo y D3. Registrar el cambio.
4. Incorporar el PBIX analítico y su proyecto editable. Registrar el cambio.
5. Actualizar documentación, informe y presentación. Registrar el cambio.
6. Publicar la rama, abrir una pull request hacia main, revisar e integrar.

Los pasos de desarrollo local se realizan en esta revisión. La publicación y la integración remotas deben verificarse en GitHub. Describir el flujo o subir todos los archivos directamente a main no acredita su uso.

## Publicar desde el clon local

```bash
git status
git log --oneline --decorate main..correccion/audiencias-semana9
git push -u origin correccion/audiencias-semana9
```

En GitHub, crear una pull request con base main y comparación correccion/audiencias-semana9. Revisar cambios y pruebas, resolver observaciones e integrar conservando evidencia de la rama. No forzar el push ni reescribir el historial original.

## Recuperar el historial del bundle

El ZIP contiene archivos, y StreamView_Historial.bundle conserva referencias y commits locales.

```bash
git clone StreamView_Historial.bundle STREAMVIEW-ANALYTICS
cd STREAMVIEW-ANALYTICS
git remote set-url origin https://github.com/vicezepeda/STREAMVIEW-ANALYTICS.git
git switch correccion/audiencias-semana9
git push -u origin correccion/audiencias-semana9
```

Después abrir y revisar la pull request. Los commits de esta corrección tienen su fecha real. No sustituyen el historial de avances que debió generarse durante las semanas anteriores.
