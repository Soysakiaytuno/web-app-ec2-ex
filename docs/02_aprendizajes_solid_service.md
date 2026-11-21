# Aprendizajes para Refactorización SOLID (Backend y Frontend)

## Puntos a aplicar en próximas refactorizaciones
1. **Separación de responsabilidades (SRP)**:
   - Funciones como `create_reservation` actualmente combinan validación de entrada/reglas y creación de entidad.
   - Se debe separar la responsabilidad de validación de la de creación, pudiendo crear su propio archivo y su propia clase para centrarlo en esa operación.
2. **Errores `422` para reglas de negocio**:
   - Todas las reglas de negocio que se implementen en adelante deben usar `BusinessRuleError` (HTTP `422`).
3. **Buenas prácticas y criterio técnico**:
   - Mantener buenas prácticas de programación (código limpio, legible y patrones adecuados cuando corresponda), refutando y proponiendo alternativas cuando una indicación no vaya por ese camino.
4. **Reglas generales en raíz y `docs/`**:
   - El flujo de trabajo y los principios SOLID aplican tanto a backend como a frontend, por lo que quedan documentados en `AGENTS.md` (raíz) y en `docs/`.
