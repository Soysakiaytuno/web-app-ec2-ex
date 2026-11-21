# 07 · Modularización del Frontend JS (API y Lógica)

## Problema Inicial
`frontend/app.js` concentraba en un solo archivo:
- URLs del backend y verbos HTTP (`GET`, `POST`, `PUT`, `PATCH`, `DELETE`).
- Llamadas directas a `fetch` con manejo de errores inconsistente (sin `try/catch` en mutaciones y sin validar `res.ok` en lecturas).
- Funciones globales en `window` invocadas mediante `onclick="..."` inline desde el HTML generado.

## Diseño Implementado
Se aplicó una separación minimalista en 2 capas usando **ES Modules nativos** (`<script type="module" src="js/app.js">`), sin introducir bundlers ni dependencias externas:

1. **`frontend/js/api.js` (Capa HTTP)**
   - Única capa que conoce `API_BASE_URL`, rutas (`/rooms`, `/guests`, `/reservations`), query strings y métodos HTTP.
   - Define `ApiError` (`status`, `message`, `data`) y un helper central `request()` que:
     - Agrega `Content-Type: application/json` cuando existe `body`.
     - Parsea respuestas de forma segura (soporta `204 No Content` y respuestas no-JSON).
     - Normaliza errores de red y respuestas `!res.ok` en `ApiError`.
   - Expone métodos semánticos explícitos (`listRooms`, `createRoom`, `updateRoomStatus`, `deleteRoom`, `listGuests`, `createGuest`, `deleteGuest`, `listReservations`, `createReservation`, `checkInReservation`, `checkOutReservation`, `cancelReservation`).

2. **`frontend/js/app.js` (Capa Lógica y DOM)**
   - No conoce URLs, `fetch` ni métodos HTTP.
   - Maneja errores de forma uniforme con `try/catch` y `showMessage(error.message, true)`.
   - Reemplaza los `onclick="..."` inline por **delegación de eventos** (`data-action`, `data-id`) en los `<tbody>` de cada tabla, evitando contaminar `window`.

## Pruebas Unitarias y Verificación
- Se creó `frontend/tests/api.test.mjs` usando `node:test` nativo (Node 22) mockeando `globalThis.fetch`.
- Comando de ejecución:
  ```powershell
  node --test frontend/tests/api.test.mjs
  ```
