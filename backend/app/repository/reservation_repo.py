from ..models import Reservation, db


def list_all(status=None, guest_id=None):
    query = Reservation.query
    if status:
        query = query.filter_by(status=status)
    if guest_id:
        query = query.filter_by(guest_id=guest_id)
    return query.order_by(Reservation.check_in).all()


def get_by_id(reservation_id):
    return db.session.get(Reservation, reservation_id)


def save(reservation):
    db.session.add(reservation)
    db.session.commit()
    return reservation


def commit():
    db.session.commit()
