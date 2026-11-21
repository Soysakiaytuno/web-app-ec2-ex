from .exceptions import BusinessRuleError


class ReservationState:
    """Estado base del patrón State para transiciones de una reserva."""

    status_name = ""

    def check_in(self, reservation):
        raise BusinessRuleError(f"No se puede hacer check-in desde el estado '{self.status_name}'")

    def check_out(self, reservation):
        raise BusinessRuleError(f"No se puede hacer check-out desde el estado '{self.status_name}'")

    def cancel(self, reservation):
        raise BusinessRuleError(f"No se puede cancelar una reserva en estado '{self.status_name}'")


class ConfirmedState(ReservationState):
    status_name = "confirmed"

    def check_in(self, reservation):
        reservation.status = "checked_in"

    def check_out(self, reservation):
        raise BusinessRuleError("No se puede hacer check-out sin haber hecho check-in")

    def cancel(self, reservation):
        reservation.status = "cancelled"


class CheckedInState(ReservationState):
    status_name = "checked_in"

    def check_out(self, reservation):
        reservation.status = "checked_out"


class CheckedOutState(ReservationState):
    status_name = "checked_out"


class CancelledState(ReservationState):
    status_name = "cancelled"


STATE_REGISTRY = {
    "confirmed": ConfirmedState(),
    "checked_in": CheckedInState(),
    "checked_out": CheckedOutState(),
    "cancelled": CancelledState(),
}


def get_reservation_state(reservation) -> ReservationState:
    """Obtiene el objeto State correspondiente al estado actual de la reserva."""
    state = STATE_REGISTRY.get(reservation.status)
    if state is None:
        raise BusinessRuleError(f"Estado de reserva desconocido: '{reservation.status}'")
    return state
