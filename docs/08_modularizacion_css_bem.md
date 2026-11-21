# 08 · Modularización CSS y Metodología BEM

## Objetivo
Separar el CSS monolítico (`frontend/style.css`) en módulos independientes por bloque siguiendo la metodología **BEM** en español, dejando `style.css` únicamente como archivo de referencias `@import`.

## Bloques Implementados
- **`base` y `contenedor`** (`frontend/css/base.css`): reset global, variables `:root` de diseño, tipografía base y contenedor principal. *(Bloque adicional justificado para aislar estilos globales y layout).*
- **`titulo`** (`frontend/css/titulo.css`): cabecera superior (`.titulo`, `.titulo__principal`, `.titulo__subtitulo`).
- **`nav`** (`frontend/css/nav.css`): pestañas de navegación (`.nav`, `.nav__ruta`, `.nav__ruta--activo`, `.nav__ruta--inactivo`).
- **`tarjeta`** (`frontend/css/tarjeta.css`): contenedor visual reutilizable para formularios y tablas (`.tarjeta`, `.tarjeta__cabecera`, `.tarjeta__titulo`). *(Bloque adicional justificado).*
- **`formulario`** (`frontend/css/formulario.css`): formulario y controles diferenciados por tipo (`.formulario`, `.formulario__campo`, `.formulario__entrada`, `.formulario__selector`).
- **`data`** (`frontend/css/data.css`) y **`fila`** (`frontend/css/fila.css`): tabla de datos (`.data`, `.data__cabecera`, `.data__encabezado`, `.data__cuerpo`, `.data__vacio`) y filas con celdas de datos/acciones (`.fila`, `.fila__dato`, `.fila__acciones`).
- **`boton`** (`frontend/css/boton.css`): botones reutilizables con modificadores de tamaño y color (`.boton`, `.boton--pequeno`, `.boton--peligro`, `.boton--exito`, `.boton--neutro`). *(Bloque adicional justificado).*
- **`estado`** (`frontend/css/estado.css`): insignias de estado de habitaciones y reservas (`.estado`, `.estado--<status>`). *(Bloque adicional justificado).*
- **`alerta`** (`frontend/css/alerta.css`): mensajes de retroalimentación (`.alerta`, `.alerta--error`). *(Bloque adicional justificado).*

## Verificación
- `node --check frontend/js/app.js`
- `node --test frontend/tests/api.test.mjs`
