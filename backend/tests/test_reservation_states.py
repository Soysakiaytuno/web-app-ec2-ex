from datetime import date, timedelta
from types import SimpleNamespace

import pytest

from app.service.exceptions import BusinessRuleError
from app.service.reservation_states import get_reservation_state


def test_confirmed_allows_check_in_and_cancel_but_blocks_check_out():
    res_in = SimpleNamespace(status="confirmed")
    get_reservation_state(res_in).check_in(res_in)
    assert res_in.status == "checked_in"

    res_cancel = SimpleNamespace(status="confirmed")
    get_reservation_state(res_cancel).cancel(res_cancel)
    assert res_cancel.status == "cancelled"

    res_out = SimpleNamespace(status="confirmed")
    with pytest.raises(BusinessRuleError) as exc:
        get_reservation_state(res_out).check_out(res_out)
    assert exc.value.status_code == 422


def test_checked_in_allows_check_out_and_blocks_check_in_and_cancel():
    res = SimpleNamespace(status="checked_in")
    with pytest.raises(BusinessRuleError) as exc_in:
        get_reservation_state(res).check_in(res)
    assert exc_in.value.status_code == 422

    with pytest.raises(BusinessRuleError) as exc_cancel:
        get_reservation_state(res).cancel(res)
    assert exc_cancel.value.status_code == 422

    get_reservation_state(res).check_out(res)
    assert res.status == "checked_out"


@pytest.mark.parametrize("terminal_status", ["checked_out", "cancelled"])
def test_terminal_states_block_all_transitions(terminal_status):
    res = SimpleNamespace(status=terminal_status)
    state = get_reservation_state(res)

    for action in (state.check_in, state.check_out, state.cancel):
        with pytest.raises(BusinessRuleError) as exc:
            action(res)
        assert exc.value.status_code == 422


def test_api_check_out_without_check_in_returns_422(client, room, guest):
    start = date.today()
    created = client.post("/api/reservations", json={
        "room_id": room["id"],
        "guest_id": guest["id"],
        "check_in": start.isoformat(),
        "check_out": (start + timedelta(days=2)).isoformat(),
        "guests_count": 1,
    }).get_json()

    res = client.patch(f"/api/reservations/{created['id']}/check-out")
    assert res.status_code == 422
    assert "error" in res.get_json()


def test_api_check_in_on_cancelled_reservation_returns_422(client, room, guest):
    start = date.today()
    created = client.post("/api/reservations", json={
        "room_id": room["id"],
        "guest_id": guest["id"],
        "check_in": start.isoformat(),
        "check_out": (start + timedelta(days=2)).isoformat(),
        "guests_count": 1,
    }).get_json()

    rid = created["id"]
    assert client.patch(f"/api/reservations/{rid}/cancel").status_code == 200

    res = client.patch(f"/api/reservations/{rid}/check-in")
    assert res.status_code == 422
    assert "error" in res.get_json()
