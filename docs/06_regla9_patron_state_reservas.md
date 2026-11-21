# Cambio 06: Regla de Negocio #9 y Patrón State para Reservas

## Problema / Objetivo
Implementar la **Regla #9** de `docs/REGLAS.md`: *"no se puede hacer check out sin hacer check in"*, ordenando el ciclo de vida de estados de una reserva mediante el **Patrón de Diseño State** para facilitar futuras reglas (como la Regla #8 de fecha en check-in y la Regla #10 de bloqueo sobre reservas canceladas).

## Decisiones de Diseño (definidas en `/grill-me` y `/plan`)
1. **Estados reales de `Reservation`**:
   - Se utilizan únicamente los 4 estados reales del modelo (`confirmed`, `checked_in`, `checked_out`, `cancelled`), descartando `"libre"` por corresponder a disponibilidad de `Room` y no a una reserva existente.
2. **Patrón State (`reservation_states.py`)**:
   - `ConfirmedState`: permite `check_in` -> `checked_in` y `cancel` -> `cancelled`; bloquea `check_out` con `BusinessRuleError` (`422`).
   - `CheckedInState`: permite `check_out` -> `checked_out`; bloquea `check_in` y `cancel` con `422`.
   - `CheckedOutState` y `CancelledState`: estados terminales que bloquean todas las transiciones con `422`.
   - `STATE_REGISTRY` permite resolver el estado por diccionario sin `if` anidados.

## Archivos Creados / Modificados
- `backend/app/service/reservation_states.py` (nuevo)
- `backend/app/service/reservation_service.py`
- `backend/tests/test_reservation_states.py` (nuevo)
- `docs/06_regla9_patron_state_reservas.md` (nuevo)

## Verificación
- Se ejecutó `.\.venv\Scripts\pytest.exe -v` en `backend/` validando toda la suite existente más las nuevas pruebas del patrón State y endpoints.
