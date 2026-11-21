import { afterEach, beforeEach, describe, it } from "node:test";
import assert from "node:assert/strict";
import {
  ApiError,
  cancelReservation,
  checkInReservation,
  checkOutReservation,
  createGuest,
  createReservation,
  createRoom,
  deleteGuest,
  deleteRoom,
  listGuests,
  listReservations,
  listRooms,
  updateRoomStatus,
} from "../js/api.js";

const originalFetch = globalThis.fetch;

function mockFetchResponse({ ok = true, status = 200, body = null } = {}) {
  const calls = [];
  globalThis.fetch = async (url, init) => {
    calls.push({ url, init });
    return {
      ok,
      status,
      async text() {
        if (body === null || body === undefined) return "";
        return typeof body === "string" ? body : JSON.stringify(body);
      },
    };
  };
  return calls;
}

describe("frontend/js/api.js", () => {
  beforeEach(() => {
    globalThis.fetch = originalFetch;
  });

  afterEach(() => {
    globalThis.fetch = originalFetch;
  });

  it("listRooms realiza GET /rooms y retorna el JSON parseado", async () => {
    const expected = [{ id: 1, number: "101" }];
    const calls = mockFetchResponse({ body: expected });

    const result = await listRooms();

    assert.deepEqual(result, expected);
    assert.equal(calls.length, 1);
    assert.equal(calls[0].url, "http://localhost:8000/api/rooms");
    assert.equal(calls[0].init.method, "GET");
    assert.equal(calls[0].init.body, undefined);
  });

  it("createRoom realiza POST /rooms con Content-Type JSON", async () => {
    const payload = { number: "102", type: "single", price_per_night: 150, capacity: 1 };
    const calls = mockFetchResponse({ status: 201, body: { id: 2, ...payload } });

    const result = await createRoom(payload);

    assert.equal(result.id, 2);
    assert.equal(calls[0].url, "http://localhost:8000/api/rooms");
    assert.equal(calls[0].init.method, "POST");
    assert.equal(calls[0].init.headers["Content-Type"], "application/json");
    assert.equal(calls[0].init.body, JSON.stringify(payload));
  });

  it("updateRoomStatus realiza PUT /rooms/:id con el nuevo estado", async () => {
    const calls = mockFetchResponse({ body: { id: 5, status: "maintenance" } });

    const result = await updateRoomStatus(5, "maintenance");

    assert.equal(result.status, "maintenance");
    assert.equal(calls[0].url, "http://localhost:8000/api/rooms/5");
    assert.equal(calls[0].init.method, "PUT");
    assert.equal(calls[0].init.body, JSON.stringify({ status: "maintenance" }));
  });

  it("deleteRoom realiza DELETE /rooms/:id y soporta respuesta 204 vacía", async () => {
    const calls = mockFetchResponse({ status: 204, body: null });

    const result = await deleteRoom(7);

    assert.equal(result, null);
    assert.equal(calls[0].url, "http://localhost:8000/api/rooms/7");
    assert.equal(calls[0].init.method, "DELETE");
  });

  it("listGuests, createGuest y deleteGuest usan las rutas y métodos correctos", async () => {
    let calls = mockFetchResponse({ body: [] });
    await listGuests();
    assert.equal(calls[0].url, "http://localhost:8000/api/guests");
    assert.equal(calls[0].init.method, "GET");

    calls = mockFetchResponse({ status: 201, body: { id: 3, full_name: "Ana" } });
    await createGuest({ full_name: "Ana", email: "ana@test.com", document: "123" });
    assert.equal(calls[0].url, "http://localhost:8000/api/guests");
    assert.equal(calls[0].init.method, "POST");

    calls = mockFetchResponse({ status: 204, body: null });
    await deleteGuest(3);
    assert.equal(calls[0].url, "http://localhost:8000/api/guests/3");
    assert.equal(calls[0].init.method, "DELETE");
  });

  it("listReservations envía query param ?status=... solo cuando hay filtro", async () => {
    let calls = mockFetchResponse({ body: [] });
    await listReservations();
    assert.equal(calls[0].url, "http://localhost:8000/api/reservations");

    calls = mockFetchResponse({ body: [] });
    await listReservations("confirmed");
    assert.equal(calls[0].url, "http://localhost:8000/api/reservations?status=confirmed");
  });

  it("createReservation y transiciones de reserva usan sus endpoints semánticos", async () => {
    let calls = mockFetchResponse({ status: 201, body: { id: 10, total_price: 300 } });
    await createReservation({ room_id: 1, guest_id: 2 });
    assert.equal(calls[0].url, "http://localhost:8000/api/reservations");
    assert.equal(calls[0].init.method, "POST");

    calls = mockFetchResponse({ body: { id: 10, status: "checked_in" } });
    await checkInReservation(10);
    assert.equal(calls[0].url, "http://localhost:8000/api/reservations/10/check-in");
    assert.equal(calls[0].init.method, "PATCH");

    calls = mockFetchResponse({ body: { id: 10, status: "checked_out" } });
    await checkOutReservation(10);
    assert.equal(calls[0].url, "http://localhost:8000/api/reservations/10/check-out");
    assert.equal(calls[0].init.method, "PATCH");

    calls = mockFetchResponse({ body: { id: 10, status: "cancelled" } });
    await cancelReservation(10);
    assert.equal(calls[0].url, "http://localhost:8000/api/reservations/10/cancel");
    assert.equal(calls[0].init.method, "PATCH");
  });

  it("lanza ApiError con el mensaje del backend cuando !response.ok", async () => {
    mockFetchResponse({
      ok: false,
      status: 422,
      body: { error: "Capacidad excedida" },
    });

    await assert.rejects(
      () => createReservation({ room_id: 1 }),
      (error) => {
        assert.ok(error instanceof ApiError);
        assert.equal(error.status, 422);
        assert.equal(error.message, "Capacidad excedida");
        return true;
      },
    );
  });

  it("lanza ApiError con mensaje HTTP genérico si la respuesta de error no es JSON", async () => {
    mockFetchResponse({
      ok: false,
      status: 500,
      body: "Internal Server Error",
    });

    await assert.rejects(
      () => listRooms(),
      (error) => {
        assert.ok(error instanceof ApiError);
        assert.equal(error.status, 500);
        assert.equal(error.message, "Error HTTP 500");
        return true;
      },
    );
  });

  it("lanza ApiError legible cuando fetch falla por error de red", async () => {
    globalThis.fetch = async () => {
      throw new TypeError("Failed to fetch");
    };

    await assert.rejects(
      () => listRooms(),
      (error) => {
        assert.ok(error instanceof ApiError);
        assert.equal(error.status, 0);
        assert.equal(error.message, "No se pudo conectar con el servidor");
        return true;
      },
    );
  });
});
