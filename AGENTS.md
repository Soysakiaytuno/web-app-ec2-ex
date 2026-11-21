# Reglas Obligatorias del Proyecto

## 1. Flujo de Trabajo (Backend y Frontend)
1. **Planificación y análisis sin ambigüedades**: Al inicio de cada cambio, planificar y debatir ejecutando `/plan` y `/grill-me` (extensible hasta definir bien el problema).
2. **Notas en `docs/`**: En cada cambio e implementación, crear o actualizar un `.md` en `docs/` con notas de mejora y verificación.
3. **Revisión mutua**: Revisar juntos cada cambio antes de darlo por aprobado.
4. **Pruebas unitarias**: Todo cambio debe estar respaldado por pruebas unitarias (crearlas si no existen; cumplirlas si ya existen).
5. **Commit y Push**: Con cada cambio aprobado, hacer `commit` local y `push` al remoto para mantener el registro en el PR abierto.
6. **Aprendizaje continuo (`/learn`)**: Al aprobar cada cambio, ejecutar `/learn` registrando aprendizajes en `docs/` y en las reglas del proyecto.
7. **Verificación integral**: Asegurar tras cada cambio que la aplicación funciona y nada se rompió.
8. **Cambios grandes (`/teamwork`)**: Usar `/teamwork` para agilizar y optimizar costos en cambios grandes.

## 2. Diseño SOLID y Código Limpio (ej. `service/` y lógica de negocio)
1. **Responsabilidad Única (SRP) en operaciones complejas**: No mezclar validaciones extensas y creación/orquestación dentro de una sola función (ej. `create_reservation`). Extraerlas a su propio archivo y clase dedicada (separando validador y creador/caso de uso).
2. **Errores de reglas de negocio (`422`)**: Toda regla de negocio que se implemente debe lanzar `BusinessRuleError` (HTTP `422`).
3. **Buenas prácticas y criterio técnico**: Mantener buenas prácticas de programación (código limpio, legible, mantenible y patrones adecuados cuando corresponda). Si una indicación del usuario va en contra de las buenas prácticas, se debe **refutar y proponer la alternativa correcta** antes de implementarla.
