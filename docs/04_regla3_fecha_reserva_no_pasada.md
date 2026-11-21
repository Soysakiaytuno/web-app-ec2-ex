# Cambio 04: Regla de Negocio #3 — Fecha de Reserva no Anterior a la Actual

## Problema / Objetivo
Implementar la **Regla #3** de `docs/REGLAS.md`: *"le fecha de reserva no puede ser anterior a la actual"*, evitando crear reservas con `check_in` en el pasado.

## Decisiones de Diseño (definidas en `/grill-me` y `/plan`)
1. **Criterio de fecha actual**:
   - Se rechaza únicamente `check_in < date.today()`, permitiendo reservas para el mismo día (`check_in == date.today()`), lo cual además mantiene compatibilidad con `test_reservation_status_changes` en `test_api.py`.
2. **Error HTTP `422`**:
   - Se lanza `BusinessRuleError("La fecha de reserva no puede ser anterior a la actual")` (HTTP `422`), siguiendo la convención de `AGENTS.md`.
3. **Ubicación SRP**:
   - Se agregó la función independiente `validate_check_in_not_in_past(check_in)` en `backend/app/service/create_reservation.py` e invocada en `CreateReservationUseCase.execute`.

## Archivos Creados / Modificados
- `backend/app/service/create_reservation.py`
- `backend/tests/test_create_reservation.py`
- `docs/04_regla3_fecha_reserva_no_pasada.md`

## Verificación
- Se ejecutó `.\.venv\Scripts\pytest.exe -v` en `backend/` validando los 9 tests existentes de `test_api.py` y las nuevas pruebas unitarias y de endpoint para Regla #3.
