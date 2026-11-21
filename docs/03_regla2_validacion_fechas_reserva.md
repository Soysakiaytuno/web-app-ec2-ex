# Cambio 03: Regla de Negocio #2 — Validación de Fechas en Creación de Reservas

## Problema / Objetivo
Implementar la **Regla #2** de `docs/REGLAS.md`: *"la fecha de salida no puede ser antes a la de la llegada"*, asegurando que `check_out > check_in` (mínimo 1 noche) al crear reservas, y aplicando principios SOLID (SRP y cero `if` anidados) en `service/`.

## Decisiones de Diseño (definidas en `/grill-me` y `/plan`)
1. **Excepción `BusinessRuleError` (HTTP 422)**:
   - Se agregó `BusinessRuleError` en `backend/app/service/exceptions.py` con `status_code=422` y un mensaje predeterminado (`"La operación incumple una regla de negocio"`).
2. **Separación de responsabilidades (SRP) en `create_reservation.py`**:
   - Se creó `backend/app/service/create_reservation.py` con la clase `CreateReservationUseCase` y funciones de validación planas independientes (`validate_required_fields`, `parse_reservation_inputs`, `validate_date_range`), evitando `if` anidados.
   - `reservation_service.create_reservation(data)` delega directamente en `CreateReservationUseCase().execute(data)`.
3. **Criterio de fechas**:
   - Se exige `check_out > check_in` (rechaza tanto `check_out < check_in` como `check_out == check_in`, devolviendo `422`).

## Archivos Creados / Modificados
- `backend/app/service/exceptions.py`
- `backend/app/service/create_reservation.py`
- `backend/app/service/reservation_service.py`
- `backend/tests/test_create_reservation.py`

## Verificación
- Se ejecutó `.\.venv\Scripts\pytest.exe -v` en `backend/` cubriendo tanto los tests existentes (`test_api.py`) como los nuevos tests unitarios y de endpoint (`test_create_reservation.py`).
