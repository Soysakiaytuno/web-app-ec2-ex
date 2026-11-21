# Cambio 05: Regla de Negocio #4 — Capacidad de la Habitación y Separación Validador/Creador

## Problema / Objetivo
Implementar la **Regla #4** de `docs/REGLAS.md`: no permitir reservar si `guests_count > room.capacity`, además de validar `guests_count > 0`.
Al mismo tiempo, reforzar el principio SRP separando completamente las validaciones (y obtención de entidades para validar) en `reservation_validators.py`, dejando a `CreateReservationUseCase` exclusivamente el cálculo del total y la creación/persistencia.

## Decisiones de Diseño
1. **Separación en `reservation_validators.py`**:
   - `validate_create_reservation(data)` ejecuta las validaciones de entrada, obtiene `room` y `guest` vía repositorios y valida reglas de negocio sobre la habitación.
   - `validate_guests_count(guests_count)`: lanza `ValidationError` (`400`) si `guests_count <= 0`.
   - `validate_room_capacity(guests_count, room)`: lanza `BusinessRuleError` (`422`) si `guests_count > room.capacity`.
2. **Responsabilidad de `CreateReservationUseCase` (`create_reservation.py`)**:
   - Solo invoca `validate_create_reservation(data)`, calcula `total_price` mediante `calculate_total_price(...)` y guarda la entidad `Reservation`.

## Archivos Creados / Modificados
- `backend/app/service/reservation_validators.py` (nuevo)
- `backend/app/service/create_reservation.py`
- `backend/tests/test_create_reservation.py`
- `docs/05_regla4_capacidad_habitacion.md` (nuevo)

## Verificación
- Se ejecutó `.\.venv\Scripts\pytest.exe -v` en `backend/` cubriendo los 9 tests de `test_api.py` y los tests unitarios y de endpoint de `test_create_reservation.py`.
