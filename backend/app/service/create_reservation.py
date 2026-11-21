from ..models import Reservation
from ..repository import reservation_repo
from .reservation_validators import validate_create_reservation


def calculate_total_price(check_in, check_out, price_per_night):
    """Calcula el precio total de la estadía."""
    nights = (check_out - check_in).days
    return nights * price_per_night


class CreateReservationUseCase:
    """Caso de uso dedicado a calcular el total y persistir una reserva ya validada."""

    def execute(self, data):
        room, guest, check_in, check_out, guests_count = validate_create_reservation(data)
        total_price = calculate_total_price(check_in, check_out, room.price_per_night)

        reservation = Reservation(
            room=room,
            guest=guest,
            check_in=check_in,
            check_out=check_out,
            guests_count=guests_count,
            status="confirmed",
            total_price=total_price,
        )
        return reservation_repo.save(reservation)
