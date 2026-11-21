from ..models import Room, db


def list_all(status=None):
    query = Room.query
    if status:
        query = query.filter_by(status=status)
    return query.order_by(Room.number).all()


def get_by_id(room_id):
    return db.session.get(Room, room_id)


def get_by_number(number):
    return Room.query.filter_by(number=number).first()


def save(room):
    db.session.add(room)
    db.session.commit()
    return room


def commit():
    db.session.commit()


def delete(room):
    db.session.delete(room)
    db.session.commit()
