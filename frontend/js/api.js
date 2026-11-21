function getDefaultBaseUrl() {
  if (typeof location !== "undefined") {
    return `${location.protocol}//${location.hostname}:8000/api`;
  }
  return "http://localhost:8000/api";
}

const API_BASE_URL = getDefaultBaseUrl();

export class ApiError extends Error {
  constructor(message, status = 0, data = null) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.data = data;
  }
}

async function parseResponseBody(response) {
  const text = await response.text();
  if (!text) return null;

  try {
    return JSON.parse(text);
  } catch {
    return text;
  }
}

async function request(path, { method = "GET", body, headers = {} } = {}) {
  const requestHeaders = { ...headers };
  const init = { method, headers: requestHeaders };

  if (body !== undefined) {
    requestHeaders["Content-Type"] = "application/json";
    init.body = JSON.stringify(body);
  }

  let response;
  try {
    response = await fetch(`${API_BASE_URL}${path}`, init);
  } catch (error) {
    throw new ApiError("No se pudo conectar con el servidor", 0, error);
  }

  const data = await parseResponseBody(response);

  if (!response.ok) {
    const message =
      (data && typeof data === "object" && data.error) ||
      `Error HTTP ${response.status}`;
    throw new ApiError(message, response.status, data);
  }

  return data;
}

// ---------- Habitaciones ----------
export function listRooms() {
  return request("/rooms");
}

export function createRoom(roomData) {
  return request("/rooms", { method: "POST", body: roomData });
}

export function updateRoomStatus(id, status) {
  return request(`/rooms/${id}`, { method: "PUT", body: { status } });
}

export function deleteRoom(id) {
  return request(`/rooms/${id}`, { method: "DELETE" });
}

// ---------- Huéspedes ----------
export function listGuests() {
  return request("/guests");
}

export function createGuest(guestData) {
  return request("/guests", { method: "POST", body: guestData });
}

export function deleteGuest(id) {
  return request(`/guests/${id}`, { method: "DELETE" });
}

// ---------- Reservas ----------
export function listReservations(status = "") {
  const query = status ? `?${new URLSearchParams({ status }).toString()}` : "";
  return request(`/reservations${query}`);
}

export function createReservation(reservationData) {
  return request("/reservations", { method: "POST", body: reservationData });
}

export function checkInReservation(id) {
  return request(`/reservations/${id}/check-in`, { method: "PATCH" });
}

export function checkOutReservation(id) {
  return request(`/reservations/${id}/check-out`, { method: "PATCH" });
}

export function cancelReservation(id) {
  return request(`/reservations/${id}/cancel`, { method: "PATCH" });
}
