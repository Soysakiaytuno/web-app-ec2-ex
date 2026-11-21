from datetime import date

from ..repository import guest_repo, room_repo
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


def validate_guests_count(guests_count):
    """Verifica que la cantidad de huéspedes sea positiva."""
    if guests_count <= 0:
        raise ValidationError("La cantidad de huéspedes debe ser mayor a 0")


def validate_check_in_not_in_past(check_in):
    """Regla #3: la fecha de llegada no puede ser anterior a la fecha actual."""
    if check_in < date.today():
        raise BusinessRuleError("La fecha de reserva no puede ser anterior a la actual")


def validate_date_range(check_in, check_out):
    """Regla #2: la fecha de salida debe ser estrictamente posterior a la de llegada."""
    if check_out <= check_in:
        raise BusinessRuleError("La fecha de salida debe ser posterior a la fecha de llegada")


def validate_room_capacity(guests_count, room):
    """Regla #4: la cantidad de huéspedes no puede superar la capacidad de la habitación."""
    if guests_count > room.capacity:
        raise BusinessRuleError("La cantidad de huéspedes supera la capacidad de la habitación")


def validate_create_reservation(data):
    """Orquesta todas las validaciones y resuelve las entidades requeridas para crear una reserva."""
    validate_required_fields(data)
    room_id, guest_id, check_in, check_out, guests_count = parse_reservation_inputs(data)
    validate_guests_count(guests_count)
    validate_check_in_not_in_past(check_in)
    validate_date_range(check_in, check_out)

    room = room_repo.get_by_id(room_id)
    if room is None:
        raise NotFoundError("Habitación no encontrada")
    validate_room_capacity(guests_count, room)

    guest = guest_repo.get_by_id(guest_id)
    if guest is None:
        raise NotFoundError("Huésped no encontrado")

    return room, guest, check_in, check_out, guests_count
