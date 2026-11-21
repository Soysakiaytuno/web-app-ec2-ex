import {
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
} from "./api.js";

const ROOM_TYPES = { single: "Simple", double: "Doble", family: "Familiar", suite: "Suite" };
const STATUS_LABELS = {
  available: "Disponible",
  maintenance: "Mantenimiento",
  confirmed: "Confirmada",
  checked_in: "Hospedado",
  checked_out: "Finalizada",
  cancelled: "Cancelada",
};

const RESERVATION_ACTIONS = {
  "check-in": checkInReservation,
  "check-out": checkOutReservation,
  cancel: cancelReservation,
};

// ---------- utilidades ----------
function esc(value) {
  return String(value ?? "").replace(
    /[&<>"']/g,
    (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]),
  );
}

function showMessage(text, isError = false) {
  const msg = document.getElementById("msg");
  msg.textContent = text;
  msg.className = isError ? "msg error" : "msg";
  msg.hidden = false;
  clearTimeout(showMessage.timer);
  showMessage.timer = setTimeout(() => {
    msg.hidden = true;
  }, 4000);
}

// ---------- pestañas ----------
document.querySelectorAll(".tabs button").forEach((button) => {
  button.addEventListener("click", () => {
    document.querySelectorAll(".tabs button").forEach((b) => b.classList.remove("active"));
    button.classList.add("active");
    document.querySelectorAll(".tab").forEach((tab) => {
      tab.hidden = true;
    });
    document.getElementById("tab-" + button.dataset.tab).hidden = false;
  });
});

// ---------- habitaciones ----------
async function loadRooms() {
  try {
    const rooms = await listRooms();
    const body = document.getElementById("rooms-body");
    if (rooms.length === 0) {
      body.innerHTML = '<tr><td colspan="6" class="empty">No hay habitaciones</td></tr>';
    } else {
      body.innerHTML = rooms
        .map(
          (r) => `
        <tr>
          <td>${esc(r.number)}</td>
          <td>${esc(ROOM_TYPES[r.type] || r.type)}</td>
          <td>Bs ${esc(r.price_per_night)}</td>
          <td>${esc(r.capacity)}</td>
          <td><span class="badge ${esc(r.status)}">${esc(STATUS_LABELS[r.status])}</span></td>
          <td>
            <button class="btn btn-small btn-gray" data-action="toggle-maintenance" data-id="${r.id}" data-status="${esc(r.status)}">
              ${r.status === "maintenance" ? "Habilitar" : "Mantenimiento"}
            </button>
            <button class="btn btn-small btn-red" data-action="delete-room" data-id="${r.id}">Eliminar</button>
          </td>
        </tr>`,
        )
        .join("");
    }
    // también llena el select del formulario de reservas
    document.getElementById("reservation-room").innerHTML = rooms
      .map(
        (r) =>
          `<option value="${r.id}">${esc(r.number)} · ${esc(ROOM_TYPES[r.type])} · Bs ${esc(r.price_per_night)}</option>`,
      )
      .join("");
  } catch (error) {
    showMessage(error.message || "No se pudo conectar con el servidor", true);
  }
}

document.getElementById("room-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const form = event.target;
  const data = Object.fromEntries(new FormData(form));
  data.price_per_night = Number(data.price_per_night);
  data.capacity = Number(data.capacity);

  try {
    const body = await createRoom(data);
    form.reset();
    showMessage("Habitación " + body.number + " creada");
    await loadRooms();
  } catch (error) {
    showMessage(error.message, true);
  }
});

async function handleToggleMaintenance(id, status) {
  const nextStatus = status === "maintenance" ? "available" : "maintenance";
  try {
    await updateRoomStatus(id, nextStatus);
    await loadRooms();
  } catch (error) {
    showMessage(error.message, true);
  }
}

async function handleDeleteRoom(id) {
  if (!confirm("¿Eliminar la habitación?")) return;
  try {
    await deleteRoom(id);
    showMessage("Habitación eliminada");
    await loadRooms();
  } catch (error) {
    showMessage(error.message, true);
  }
}

document.getElementById("rooms-body").addEventListener("click", (event) => {
  const button = event.target.closest("button[data-action]");
  if (!button) return;

  const id = Number(button.dataset.id);
  if (button.dataset.action === "toggle-maintenance") {
    handleToggleMaintenance(id, button.dataset.status);
  } else if (button.dataset.action === "delete-room") {
    handleDeleteRoom(id);
  }
});

// ---------- huéspedes ----------
async function loadGuests() {
  try {
    const guests = await listGuests();
    const body = document.getElementById("guests-body");
    if (guests.length === 0) {
      body.innerHTML = '<tr><td colspan="4" class="empty">No hay huéspedes</td></tr>';
    } else {
      body.innerHTML = guests
        .map(
          (g) => `
        <tr>
          <td>${esc(g.full_name)}</td>
          <td>${esc(g.email)}</td>
          <td>${esc(g.document)}</td>
          <td><button class="btn btn-small btn-red" data-action="delete-guest" data-id="${g.id}">Eliminar</button></td>
        </tr>`,
        )
        .join("");
    }
    document.getElementById("reservation-guest").innerHTML = guests
      .map((g) => `<option value="${g.id}">${esc(g.full_name)}</option>`)
      .join("");
  } catch (error) {
    showMessage(error.message || "No se pudo conectar con el servidor", true);
  }
}

document.getElementById("guest-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const form = event.target;
  const data = Object.fromEntries(new FormData(form));

  try {
    const body = await createGuest(data);
    form.reset();
    showMessage("Huésped " + body.full_name + " registrado");
    await loadGuests();
  } catch (error) {
    showMessage(error.message, true);
  }
});

async function handleDeleteGuest(id) {
  if (!confirm("¿Eliminar el huésped?")) return;
  try {
    await deleteGuest(id);
    showMessage("Huésped eliminado");
    await loadGuests();
  } catch (error) {
    showMessage(error.message, true);
  }
}

document.getElementById("guests-body").addEventListener("click", (event) => {
  const button = event.target.closest("button[data-action]");
  if (!button) return;

  if (button.dataset.action === "delete-guest") {
    handleDeleteGuest(Number(button.dataset.id));
  }
});

// ---------- reservas ----------
async function loadReservations() {
  try {
    const status = document.getElementById("reservation-filter").value;
    const reservations = await listReservations(status);
    const body = document.getElementById("reservations-body");
    if (reservations.length === 0) {
      body.innerHTML = '<tr><td colspan="10" class="empty">No hay reservas</td></tr>';
      return;
    }
    body.innerHTML = reservations
      .map(
        (r) => `
      <tr>
        <td>${r.id}</td>
        <td>${esc(r.room_number)}</td>
        <td>${esc(r.guest_name)}</td>
        <td>${esc(r.check_in)}</td>
        <td>${esc(r.check_out)}</td>
        <td>${esc(r.nights)}</td>
        <td>${esc(r.guests_count)}</td>
        <td>${esc(r.total_price)}</td>
        <td><span class="badge ${esc(r.status)}">${esc(STATUS_LABELS[r.status])}</span></td>
        <td>
          <button class="btn btn-small btn-green" data-action="check-in" data-id="${r.id}">Check-in</button>
          <button class="btn btn-small" data-action="check-out" data-id="${r.id}">Check-out</button>
          <button class="btn btn-small btn-red" data-action="cancel" data-id="${r.id}">Cancelar</button>
        </td>
      </tr>`,
      )
      .join("");
  } catch (error) {
    showMessage(error.message || "No se pudo conectar con el servidor", true);
  }
}

document.getElementById("reservation-filter").addEventListener("change", loadReservations);

document.getElementById("reservation-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const form = event.target;
  const data = Object.fromEntries(new FormData(form));
  data.room_id = Number(data.room_id);
  data.guest_id = Number(data.guest_id);
  data.guests_count = Number(data.guests_count);

  try {
    const body = await createReservation(data);
    form.reset();
    showMessage("Reserva #" + body.id + " creada · total Bs " + body.total_price);
    await loadReservations();
  } catch (error) {
    showMessage(error.message, true);
  }
});

async function handleChangeReservation(id, action) {
  const actionFn = RESERVATION_ACTIONS[action];
  if (!actionFn) return;

  try {
    const body = await actionFn(id);
    showMessage("Reserva #" + id + ": " + STATUS_LABELS[body.status]);
    await loadReservations();
  } catch (error) {
    showMessage(error.message, true);
  }
}

document.getElementById("reservations-body").addEventListener("click", (event) => {
  const button = event.target.closest("button[data-action]");
  if (!button) return;

  handleChangeReservation(Number(button.dataset.id), button.dataset.action);
});

// ---------- inicio ----------
loadRooms();
loadGuests();
loadReservations();
