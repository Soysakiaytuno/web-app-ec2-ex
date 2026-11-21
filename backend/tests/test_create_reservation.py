from datetime import date, timedelta
from types import SimpleNamespace

import pytest

from app.service.exceptions import BusinessRuleError, ValidationError
from app.service.reservation_validators import (
    validate_check_in_not_in_past,
    validate_date_range,
    validate_guests_count,
    validate_room_capacity,
)


def test_business_rule_error_default_message_and_status():
    err = BusinessRuleError()
    assert err.status_code == 422
    assert err.message == "La operación incumple una regla de negocio"


def test_validate_date_range_rejects_checkout_before_checkin():
    today = date.today()
    with pytest.raises(BusinessRuleError) as exc:
        validate_date_range(today + timedelta(days=5), today + timedelta(days=2))
    assert exc.value.status_code == 422


def test_validate_date_range_rejects_same_day_checkout():
    today = date.today()
    with pytest.raises(BusinessRuleError) as exc:
        validate_date_range(today + timedelta(days=3), today + timedelta(days=3))
    assert exc.value.status_code == 422


def test_validate_date_range_accepts_valid_range():
    today = date.today()
    validate_date_range(today + timedelta(days=1), today + timedelta(days=2))


def test_api_create_reservation_rejects_checkout_before_checkin(client, room, guest):
    start = date.today() + timedelta(days=5)
    res = client.post("/api/reservations", json={
        "room_id": room["id"],
        "guest_id": guest["id"],
        "check_in": start.isoformat(),
        "check_out": (start - timedelta(days=1)).isoformat(),
        "guests_count": 2,
    })
    assert res.status_code == 422
    assert "error" in res.get_json()


def test_api_create_reservation_rejects_same_day_checkout(client, room, guest):
    start = date.today() + timedelta(days=5)
    res = client.post("/api/reservations", json={
        "room_id": room["id"],
        "guest_id": guest["id"],
        "check_in": start.isoformat(),
        "check_out": start.isoformat(),
        "guests_count": 2,
    })
    assert res.status_code == 422
    assert "error" in res.get_json()


def test_validate_check_in_rejects_past_date():
    with pytest.raises(BusinessRuleError) as exc:
        validate_check_in_not_in_past(date.today() - timedelta(days=1))
    assert exc.value.status_code == 422


def test_validate_check_in_accepts_today():
    validate_check_in_not_in_past(date.today())


def test_api_create_reservation_rejects_past_check_in(client, room, guest):
    past = date.today() - timedelta(days=1)
    res = client.post("/api/reservations", json={
        "room_id": room["id"],
        "guest_id": guest["id"],
        "check_in": past.isoformat(),
        "check_out": (past + timedelta(days=2)).isoformat(),
        "guests_count": 2,
    })
    assert res.status_code == 422
    assert "error" in res.get_json()


def test_validate_guests_count_rejects_zero_and_negative():
    for invalid in (0, -1):
        with pytest.raises(ValidationError) as exc:
            validate_guests_count(invalid)
        assert exc.value.status_code == 400


def test_validate_room_capacity_rejects_exceeding_capacity():
    room = SimpleNamespace(capacity=2)
    with pytest.raises(BusinessRuleError) as exc:
        validate_room_capacity(3, room)
    assert exc.value.status_code == 422


def test_validate_room_capacity_accepts_within_capacity():
    room = SimpleNamespace(capacity=2)
    validate_room_capacity(1, room)
    validate_room_capacity(2, room)


def test_api_create_reservation_rejects_exceeding_capacity(client, room, guest):
    start = date.today() + timedelta(days=2)
    res = client.post("/api/reservations", json={
        "room_id": room["id"],
        "guest_id": guest["id"],
        "check_in": start.isoformat(),
        "check_out": (start + timedelta(days=2)).isoformat(),
        "guests_count": 3,
    })
    assert res.status_code == 422
    assert "error" in res.get_json()


def test_api_create_reservation_rejects_zero_guests(client, room, guest):
    start = date.today() + timedelta(days=2)
    res = client.post("/api/reservations", json={
        "room_id": room["id"],
        "guest_id": guest["id"],
        "check_in": start.isoformat(),
        "check_out": (start + timedelta(days=2)).isoformat(),
        "guests_count": 0,
    })
    assert res.status_code == 400
    assert "error" in res.get_json()
