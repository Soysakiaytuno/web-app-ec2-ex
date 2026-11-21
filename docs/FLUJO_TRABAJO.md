# Flujo de Trabajo y Reglas Obligatorias (Ciclo de Vida con IA)

Este documento define el flujo de trabajo obligatorio para las refactorizaciones y cambios del proyecto.

## Principios Generales
- **Notas y registro en `docs/`**: Durante cada cambio e implementación se debe escribir un archivo Markdown (`.md`) dentro de `docs/` tomando notas de mejoras, decisiones y verificación para asegurar que estamos alineados.
- **Ciclo de vida de software con IA**: Se plantean primero los problemas y las soluciones, para después implementarlos y verificarlos.

## Reglas Obligatorias del Flujo

1. **Planificación y diseño inicial**: Al inicio de cada cambio se hace una planificación y un diseño con base en lo solicitado.
2. **Análisis y debate sin ambigüedades (`/plan` y `/grill-me`)**: Los cambios solicitados se deben analizar y debatir para llegar a una definición clara. Para este punto y el anterior, ejecutar siempre `/plan` y `/grill-me` para definir y eliminar ambigüedades de prompts que puedan ser simples.
3. **Revisión mutua**: En cada cambio solicitado debemos revisarlo mutuamente para verificar que se cumplió con los requisitos planteados en los puntos anteriores.
4. **Respaldo con pruebas unitarias**: Cada cambio debe estar respaldado por pruebas unitarias. Si no existen, se deben crear; si ya existen, el cambio debe cumplirlas.
5. **Control de versiones y PR**: Con cada cambio aprobado se debe hacer `commit` en el repositorio local y `push` al repositorio remoto para mantener el registro en el Pull Request actualmente abierto.
6. **Aprendizaje continuo (`/learn`)**: Al aprobar cada cambio se debe ejecutar `/learn` para aprender de las fallas y evitar repetirlas en futuras planificaciones (registrando los `.md` en la carpeta `docs/`).
7. **Extensión de definición**: Los puntos 1 y 2 se pueden extender lo necesario hasta definir correctamente cómo se plantea el problema.
8. **Verificación integral tras cada cambio**: Después de cada cambio hay que asegurarse de que la aplicación funciona y no se rompió nada. Si algo se rompe, se repite el ciclo de vida planificando cómo resolverlo.
9. **Cambios grandes (`/teamwork`)**: Si los cambios solicitados son grandes, se debe usar `/teamwork` para agilizar y optimizar costos al implementar.
