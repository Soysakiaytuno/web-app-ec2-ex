from ..models import Room
from ..repository import room_repo
from .exceptions import ConflictError, NotFoundError, ValidationError

ROOM_TYPES = ("single", "double", "family", "suite")
ROOM_STATUSES = ("available", "maintenance")


def list_rooms(status=None):
    return room_repo.list_all(status=status)


def get_room(room_id):
    room = room_repo.get_by_id(room_id)
    if room is None:
        raise NotFoundError("Habitación no encontrada")
    return room


def create_room(data):
    missing = [f for f in ("number", "type", "price_per_night", "capacity") if data.get(f) in (None, "")]
    if missing:
        raise ValidationError(f"Faltan campos: {', '.join(missing)}")
    if data["type"] not in ROOM_TYPES:
        raise ValidationError(f"Tipo inválido. Usa: {', '.join(ROOM_TYPES)}")

    try:
        price = float(data["price_per_night"])
        capacity = int(data["capacity"])
    except (TypeError, ValueError):
        raise ValidationError("price_per_night y capacity deben ser números")

    number = str(data["number"]).strip()
    if room_repo.get_by_number(number):
        raise ConflictError("Ya existe una habitación con ese número")

    room = Room(
        number=number,
        type=data["type"],
        price_per_night=price,
        capacity=capacity,
        status=data.get("status", "available"),
    )
    return room_repo.save(room)


def update_room(room_id, data):
    room = get_room(room_id)

    if "type" in data:
        if data["type"] not in ROOM_TYPES:
            raise ValidationError(f"Tipo inválido. Usa: {', '.join(ROOM_TYPES)}")
        room.type = data["type"]
    if "status" in data:
        if data["status"] not in ROOM_STATUSES:
            raise ValidationError(f"Estado inválido. Usa: {', '.join(ROOM_STATUSES)}")
        room.status = data["status"]
    try:
        if "price_per_night" in data:
            room.price_per_night = float(data["price_per_night"])
        if "capacity" in data:
            room.capacity = int(data["capacity"])
    except (TypeError, ValueError):
        raise ValidationError("price_per_night y capacity deben ser números")

    room_repo.commit()
    return room


def delete_room(room_id):
    room = get_room(room_id)
    if room.reservations:
        raise ConflictError("La habitación tiene reservas registradas")
    room_repo.delete(room)
