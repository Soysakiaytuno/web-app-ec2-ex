from ..models import Guest, db


def list_all():
    return Guest.query.order_by(Guest.full_name).all()


def get_by_id(guest_id):
    return db.session.get(Guest, guest_id)


def get_by_email(email):
    return Guest.query.filter_by(email=email).first()


def save(guest):
    db.session.add(guest)
    db.session.commit()
    return guest


def delete(guest):
    db.session.delete(guest)
    db.session.commit()
