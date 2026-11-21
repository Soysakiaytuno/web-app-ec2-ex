# Cambio 01: Refactorización del Backend a Arquitectura en Capas

## Problema / Objetivo
El backend estaba estructurado como MVC acoplado, donde los archivos en `controllers/` mezclaban el manejo de rutas HTTP, las validaciones de entrada y las consultas directas a SQLAlchemy (`db.session`, `.query`, `.commit()`). Esto dificultaba escalar e implementar las nuevas reglas de negocio descritas en `docs/REGLAS.md`.

## Decisiones de Diseño (definidas en `/grill-me` y `/plan`)
1. **Separación en 4 responsabilidades**:
   - `controllers/`: solo rutas Flask, lectura de `request` y serialización con `views/`.
   - `service/`: validaciones y lógica de negocio sin acoplamiento a Flask.
   - `repository/`: consultas y persistencia SQLAlchemy aisladas por entidad (`guest_repo.py`, `room_repo.py`, `reservation_repo.py`).
   - `service/exceptions.py`: jerarquía `ServiceError` (`ValidationError` 400, `NotFoundError` 404, `ConflictError` 409) capturada globalmente mediante `@app.errorhandler(ServiceError)` en `app/__init__.py`.
2. **Estilo funcional**: funciones a nivel de módulo en `repository/` y `service/`, manteniendo coherencia con `views/` y `controllers/`.
3. **Alcance**: modularización pura sin alterar consultas, mensajes de error ni contratos HTTP existentes.

## Archivos Modificados
- `backend/app/service/exceptions.py`
- `backend/app/__init__.py`
- `backend/app/repository/guest_repo.py`, `room_repo.py`, `reservation_repo.py`
- `backend/app/service/guest_service.py`, `room_service.py`, `reservation_service.py`
- `backend/app/controllers/guest_controller.py`, `room_controller.py`, `reservation_controller.py`

## Notas de Mejora para Futuros Cambios
- Al implementar las 11 reglas de negocio de `docs/REGLAS.md`, todas las validaciones nuevas irán en `service/` y las consultas de soporte (ej. solapamiento de fechas o conteo de reservas activas) en `repository/`.
- En `reservation_service.create_reservation`, `int(data["room_id"])` y `int(data["guest_id"])` podrían lanzar `ValueError`/`TypeError` si se envía un valor no numérico; conviene contemplarlo cuando se endurezcan validaciones.
