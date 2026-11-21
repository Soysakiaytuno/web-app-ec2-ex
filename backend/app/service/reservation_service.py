from ..repository import reservation_repo
from .create_reservation import CreateReservationUseCase
from .exceptions import NotFoundError


def list_reservations(status=None, guest_id=None):
    return reservation_repo.list_all(status=status, guest_id=guest_id)


def get_reservation(reservation_id):
    reservation = reservation_repo.get_by_id(reservation_id)
    if reservation is None:
        raise NotFoundError("Reserva no encontrada")
    return reservation


def create_reservation(data):
    return CreateReservationUseCase().execute(data)


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
