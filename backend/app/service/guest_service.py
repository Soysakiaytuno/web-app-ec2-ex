from ..models import Guest
from ..repository import guest_repo
from .exceptions import ConflictError, NotFoundError, ValidationError


def list_guests():
    return guest_repo.list_all()


def get_guest(guest_id):
    guest = guest_repo.get_by_id(guest_id)
    if guest is None:
        raise NotFoundError("Huésped no encontrado")
    return guest


def create_guest(data):
    missing = [f for f in ("full_name", "email", "document") if not str(data.get(f, "")).strip()]
    if missing:
        raise ValidationError(f"Faltan campos: {', '.join(missing)}")

    email = data["email"].strip().lower()
    if "@" not in email:
        raise ValidationError("Email inválido")
    if guest_repo.get_by_email(email):
        raise ConflictError("Ya existe un huésped con ese email")

    guest = Guest(
        full_name=data["full_name"].strip(),
        email=email,
        document=str(data["document"]).strip(),
    )
    return guest_repo.save(guest)


def delete_guest(guest_id):
    guest = get_guest(guest_id)
    if guest.reservations:
        raise ConflictError("El huésped tiene reservas registradas")
    guest_repo.delete(guest)
