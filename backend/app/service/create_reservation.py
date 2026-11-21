from datetime import date

from ..models import Reservation
from ..repository import guest_repo, reservation_repo, room_repo
from .exceptions import BusinessRuleError, NotFoundError, ValidationError

REQUIRED_FIELDS = ("room_id", "guest_id", "check_in", "check_out", "guests_count")


def validate_required_fields(data):
    """Verifica que todos los campos obligatorios estén presentes."""
    missing = [f for f in REQUIRED_FIELDS if data.get(f) in (None, "")]
    if missing:
        raise ValidationError(f"Faltan campos: {', '.join(missing)}")


def parse_reservation_inputs(data):
    """Convierte y valida los tipos básicos de entrada para una reserva."""
    try:
        room_id = int(data["room_id"])
        guest_id = int(data["guest_id"])
        check_in = date.fromisoformat(data["check_in"])
        check_out = date.fromisoformat(data["check_out"])
        guests_count = int(data["guests_count"])
    except (TypeError, ValueError):
        raise ValidationError("Fechas en formato AAAA-MM-DD y room_id, guest_id, guests_count numéricos")
    return room_id, guest_id, check_in, check_out, guests_count


def validate_check_in_not_in_past(check_in):
    """Regla #3: la fecha de llegada no puede ser anterior a la fecha actual."""
    if check_in < date.today():
        raise BusinessRuleError("La fecha de reserva no puede ser anterior a la actual")


def validate_date_range(check_in, check_out):
    """Regla #2: la fecha de salida debe ser estrictamente posterior a la de llegada."""
    if check_out <= check_in:
        raise BusinessRuleError("La fecha de salida debe ser posterior a la fecha de llegada")


class CreateReservationUseCase:
    """Caso de uso dedicado para validar y crear una reserva."""

    def execute(self, data):
        validate_required_fields(data)
        room_id, guest_id, check_in, check_out, guests_count = parse_reservation_inputs(data)
        validate_check_in_not_in_past(check_in)
        validate_date_range(check_in, check_out)

        room = room_repo.get_by_id(room_id)
        if room is None:
            raise NotFoundError("Habitación no encontrada")

        guest = guest_repo.get_by_id(guest_id)
        if guest is None:
            raise NotFoundError("Huésped no encontrado")

        nights = (check_out - check_in).days
        total_price = nights * room.price_per_night

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
