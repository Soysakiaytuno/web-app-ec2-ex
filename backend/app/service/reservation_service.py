from datetime import date

from ..models import Reservation
from ..repository import guest_repo, reservation_repo, room_repo
from .exceptions import NotFoundError, ValidationError


def list_reservations(status=None, guest_id=None):
    return reservation_repo.list_all(status=status, guest_id=guest_id)


def get_reservation(reservation_id):
    reservation = reservation_repo.get_by_id(reservation_id)
    if reservation is None:
        raise NotFoundError("Reserva no encontrada")
    return reservation


def create_reservation(data):
    missing = [f for f in ("room_id", "guest_id", "check_in", "check_out", "guests_count") if data.get(f) in (None, "")]
    if missing:
        raise ValidationError(f"Faltan campos: {', '.join(missing)}")

    room = room_repo.get_by_id(int(data["room_id"]))
    if room is None:
        raise NotFoundError("Habitación no encontrada")
    guest = guest_repo.get_by_id(int(data["guest_id"]))
    if guest is None:
        raise NotFoundError("Huésped no encontrado")

    try:
        check_in = date.fromisoformat(data["check_in"])
        check_out = date.fromisoformat(data["check_out"])
        guests_count = int(data["guests_count"])
    except (TypeError, ValueError):
        raise ValidationError("Fechas en formato AAAA-MM-DD y guests_count numérico")

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


def cancel_reservation(reservation_id):
    reservation = get_reservation(reservation_id)
    reservation.status = "cancelled"
    reservation_repo.commit()
    return reservation


def check_in_reservation(reservation_id):
    reservation = get_reservation(reservation_id)
    reservation.status = "checked_in"
    reservation_repo.commit()
    return reservation


def check_out_reservation(reservation_id):
    reservation = get_reservation(reservation_id)
    reservation.status = "checked_out"
    reservation_repo.commit()
    return reservation
