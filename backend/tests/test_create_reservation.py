from datetime import date, timedelta

import pytest

from app.service.create_reservation import validate_date_range
from app.service.exceptions import BusinessRuleError


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
