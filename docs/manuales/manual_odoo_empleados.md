# Manual de Usuario — Aplicación Empleados Renaix (Odoo Web)

**Proyecto:** Renaix — Marketplace de Segunda Mano
**Versión:** 1.0.0
**Fecha:** Marzo 2026
**Autores:** Javier Herraiz Calatayud & Alejandro Sánchez Serrano
**Roles:** Desarrolladores Full-Stack — 2º DAM 2025-2026

---

## Índice

1. [Requisitos del sistema](#1-requisitos-del-sistema)
2. [Acceso a la aplicación](#2-acceso-a-la-aplicación)
3. [Navegación principal](#3-navegación-principal)
4. [Gestión de productos](#4-gestión-de-productos)
5. [Subida y gestión de imágenes](#5-subida-y-gestión-de-imágenes)
6. [Gestión de etiquetas](#6-gestión-de-etiquetas)
7. [Denuncias e incidencias](#7-denuncias-e-incidencias)
8. [Estadísticas y dashboard](#8-estadísticas-y-dashboard)
9. [Gestión de usuarios](#9-gestión-de-usuarios)
10. [Errores habituales y soluciones (FAQ)](#10-errores-habituales-y-soluciones-faq)
11. [Glosario](#11-glosario)

---

## 1. Requisitos del sistema

| Requisito | Detalle |
|-----------|---------|
| **Navegador** | Google Chrome 110+, Firefox 110+, Edge 110+ |
| **Conexión** | Red local o acceso a servidor donde corre Docker |
| **Resolución** | Mínimo 1280×768 px recomendado |
| **URL de acceso** | `http://localhost:8069` (entorno local con Docker) |

### Credenciales de prueba

> ⚠️ Estos datos son ficticios y solo válidos en el entorno de demostración.

| Rol | Usuario | Contraseña |
|-----|---------|------------|
| Administrador | `admin` | `admin` |
| Moderador | `moderador@renaix.com` | `renaix2026` |

---

## 2. Acceso a la aplicación

### 2.1 Iniciar sesión

1. Abre tu navegador web y ve a `http://localhost:8069`.
2. Aparece la pantalla de inicio de sesión de Odoo.
3. Introduce el **usuario** (email o `admin`) y la **contraseña**.
4. Haz clic en **Iniciar sesión**.
5. Si las credenciales son correctas, accederás al menú principal de Renaix.

> **Nota:** Si aparece la pantalla de selección de base de datos, selecciona `renaix_db` (o la base de datos configurada).

### 2.2 Acceder al módulo Renaix

Una vez dentro de Odoo:

1. Haz clic en el icono de cuadrícula (☰ menú de apps) en la esquina superior izquierda.
2. Busca la aplicación **"Renaix"** o **"Marketplace Segunda Mano"**.
3. Haz clic sobre ella para acceder al panel principal.

### 2.3 Cerrar sesión

1. Haz clic sobre tu nombre de usuario en la esquina superior derecha.
2. Selecciona **"Cerrar sesión"** en el menú desplegable.
3. Serás redirigido a la pantalla de inicio de sesión.

---

## 3. Navegación principal

El módulo Renaix está organizado en los siguientes menús principales:

```
Renaix
├── Productos
│   ├── Todos los Productos
│   └── Imágenes de Productos
├── Usuarios
│   └── Usuarios App
├── Transacciones
│   ├── Compras
│   └── Valoraciones
├── Comunicación
│   ├── Comentarios
│   └── Mensajes
├── Moderación
│   └── Denuncias
├── Estadísticas
│   ├── Resumen General
│   └── Dashboard
└── Configuración
    ├── Categorías
    └── Etiquetas
```

### Barra superior

- **Icono ☰**: Vuelve al menú de apps de Odoo.
- **Búsqueda global**: Busca en cualquier campo del módulo activo.
- **Icono de usuario**: Configuración de perfil y cierre de sesión.
- **Icono de campana**: Notificaciones del sistema.

---

## 4. Gestión de productos

### 4.1 Ver listado de productos

1. En el menú lateral, ve a **Productos → Todos los Productos**.
2. Verás el listado de productos en vista **lista** o **kanban**.
   - Para cambiar de vista, usa los iconos en la esquina superior derecha ( ☰ lista / ⊞ kanban).
3. Puedes **filtrar** por estado de venta, categoría o etiqueta usando la barra de búsqueda superior.
4. Puedes **ordenar** haciendo clic en las cabeceras de columna.

**Filtros rápidos disponibles:**
- `Disponibles`: productos actualmente en venta.
- `Vendidos`: productos ya transaccionados.
- `Borradores`: productos pendientes de publicar.

### 4.2 Ver detalle de un producto

1. En el listado, haz clic sobre el nombre de cualquier producto.
2. Se abre el formulario de detalle con todos los campos:
   - Nombre, descripción, precio, antigüedad
   - Estado del producto (Nuevo, Como Nuevo, Buen Estado…)
   - Estado de venta (Borrador, Disponible, Reservado, Vendido)
   - Propietario (usuario de la app)
   - Categoría y etiquetas
   - Imágenes asociadas
   - Comentarios recibidos
3. En la parte inferior verás el **chatter** (historial de cambios y mensajes internos).

### 4.3 Crear un nuevo producto

1. En **Productos → Todos los Productos**, haz clic en **"Nuevo"** (botón azul).
2. Rellena los campos obligatorios (marcados con *):
   - **Nombre del Producto** *
   - **Precio** *
   - **Estado del Producto** * (condición física)
   - **Estado de Venta** * (por defecto: Borrador)
   - **Propietario** * (usuario app)
3. Opcionalmente rellena: Descripción, Antigüedad, Ubicación, Categoría, Etiquetas.
4. Haz clic en **"Guardar"** (icono de nube o usando Ctrl+S).

### 4.4 Editar un producto

1. Abre el producto que deseas modificar.
2. Haz clic en **"Editar"** (botón en la parte superior) o directamente sobre el campo a modificar.
3. Realiza los cambios necesarios.
4. Haz clic en **"Guardar"** para confirmar o **"Descartar"** para cancelar.

### 4.5 Cambiar el estado de un producto

Desde el formulario de detalle, puedes cambiar el estado de venta mediante:

- **Barra de estado** (parte superior del formulario): haz clic en el estado deseado.
  - Borrador → Disponible → Reservado → Vendido / Eliminado

O modificando el campo **"Estado de Venta"** directamente.

### 4.6 Eliminar un producto

> ⚠️ Solo los administradores pueden eliminar productos permanentemente.

1. Abre el producto.
2. Haz clic en **Acción → Eliminar** (menú de engranaje ⚙).
3. Confirma la eliminación en el diálogo emergente.

Como alternativa segura, cambia el estado a **"Eliminado"** para ocultar el producto sin borrarlo.

---

## 5. Subida y gestión de imágenes

### 5.1 Añadir imágenes a un producto

1. Abre el producto deseado.
2. En el formulario, localiza la sección **"Imágenes"** (pestaña o sección inferior).
3. Haz clic en **"Agregar una línea"** o en el botón de cámara.
4. Se abre el formulario de imagen:
   - **Imagen** *: haz clic en el campo de imagen y selecciona un archivo desde tu equipo (JPG, PNG, máx. 5 MB).
   - **Orden**: número de posición (1 = imagen principal).
   - **Es Principal**: activa esta opción para que sea la imagen portada.
5. Haz clic en **"Guardar"**.

### 5.2 Ver gestión global de imágenes

1. Ve a **Productos → Imágenes de Productos**.
2. Verás un listado de todas las imágenes subidas con su producto asociado.
3. Puedes filtrar por producto o eliminar imágenes desde esta vista.

### 5.3 Eliminar una imagen

1. Desde el formulario del producto, localiza la imagen en la sección de imágenes.
2. Haz clic en el icono de papelera (🗑) a la derecha de la imagen.
3. Confirma la eliminación.

---

## 6. Gestión de etiquetas

Las etiquetas clasifican los productos y facilitan su búsqueda en la app móvil.

### 6.1 Ver listado de etiquetas

1. Ve a **Configuración → Etiquetas**.
2. Verás la lista de etiquetas con nombre, color y número de productos asociados.

### 6.2 Crear una nueva etiqueta

1. En la pantalla de etiquetas, haz clic en **"Nuevo"**.
2. Introduce el **Nombre** (se normaliza automáticamente a minúsculas, sin espacios dobles).
3. Selecciona un **Color** (opcional).
4. Haz clic en **"Guardar"**.

> **Reglas de etiquetas:**
> - Mínimo 2 caracteres, máximo 30.
> - No se permiten duplicados (insensible a mayúsculas).
> - Cada producto puede tener un máximo de 5 etiquetas.

### 6.3 Asignar etiquetas a un producto

1. Abre el formulario de un producto.
2. En el campo **"Etiquetas"**, haz clic y empieza a escribir.
3. Selecciona la etiqueta de la lista desplegable o crea una nueva escribiendo su nombre y presionando Enter.
4. Repite hasta añadir las etiquetas deseadas (máximo 5).
5. Guarda el producto.

### 6.4 Editar una etiqueta

1. Abre la etiqueta desde **Configuración → Etiquetas**.
2. Modifica el nombre o color.
3. Guarda los cambios.

### 6.5 Desactivar una etiqueta

1. Abre la etiqueta.
2. Desmarca el campo **"Activo"**.
3. La etiqueta dejará de aparecer como opción en los productos.

---

## 7. Denuncias e incidencias

### 7.1 Ver listado de denuncias

1. Ve a **Moderación → Denuncias**.
2. Verás el listado de denuncias ordenadas por fecha (más recientes primero).
3. Cada denuncia muestra: tipo, denunciado, categoría, estado y fecha.

**Filtros disponibles:**
- **Pendientes**: denuncias sin revisar.
- **En Revisión**: denuncias asignadas a un moderador.
- **Resueltas** / **Rechazadas**: denuncias cerradas.

### 7.2 Ver detalle de una denuncia

1. Haz clic sobre cualquier denuncia del listado.
2. El formulario muestra:
   - **Tipo**: producto, comentario o usuario denunciado.
   - **Denunciado**: el elemento concreto reportado.
   - **Denunciado por**: usuario que realizó la denuncia.
   - **Motivo**: descripción del problema.
   - **Categoría**: spam, fraude, contenido inapropiado, etc.
   - **Estado actual** y **Empleado asignado**.
   - **Resolución** (si ya fue tratada).

### 7.3 Asignarse una denuncia

1. Abre la denuncia pendiente.
2. Haz clic en el botón **"Asignar a mí"**.
3. El estado cambiará automáticamente a **"En Revisión"** y tu usuario quedará registrado.

### 7.4 Resolver una denuncia

1. Abre la denuncia en revisión.
2. Rellena el campo **"Resolución"** con la acción tomada (ej.: "Producto eliminado por contenido inapropiado").
3. Haz clic en **"Resolver"**.
4. El estado cambia a **"Resuelta"** y se notifica automáticamente al usuario denunciante.

### 7.5 Rechazar una denuncia

1. Abre la denuncia.
2. Haz clic en **"Rechazar"** si la denuncia no es procedente.
3. El estado cambia a **"Rechazada"**.

### 7.6 Ver el elemento denunciado

1. Desde el formulario de la denuncia, haz clic en el enlace del campo **"Producto Denunciado"**, **"Comentario Denunciado"** o **"Usuario Denunciado"**.
2. Se abre directamente el registro correspondiente para que puedas revisarlo.

---

## 8. Estadísticas y dashboard

### 8.1 Resumen general

Ve a **Estadísticas → Resumen General** para ver:
- Total de productos publicados, vendidos y en borrador.
- Número de usuarios activos.
- Gráfico de ventas por periodo.
- Denuncias pendientes de atención.

### 8.2 Dashboard interactivo

Ve a **Estadísticas → Dashboard** para acceder al panel de control con:
- **Gráfico de barras**: productos por categoría.
- **Gráfico de líneas**: evolución de publicaciones por mes.
- **Gráfico circular**: distribución de estados de venta.
- **Ranking de usuarios**: más activos por ventas o valoraciones.

Puedes filtrar el dashboard por **mes** y **año** usando los selectores en la parte superior.

---

## 9. Gestión de usuarios

### 9.1 Ver listado de usuarios

1. Ve a **Usuarios → Usuarios App**.
2. Verás todos los usuarios registrados desde la app móvil con:
   - Nombre, email, teléfono, valoración promedio, productos en venta y vendidos.

### 9.2 Ver perfil de un usuario

1. Haz clic sobre cualquier usuario.
2. El formulario muestra toda la información del usuario y sus estadísticas.
3. Desde aquí puedes ver sus productos, compras realizadas, comentarios y denuncias.

### 9.3 Suspender/Activar un usuario

1. Abre el perfil del usuario.
2. Cambia el campo **"Cuenta Activa"**:
   - Desmarca para **suspender** (el usuario no podrá acceder a la app).
   - Marca para **reactivar**.
3. Guarda los cambios.

---

## 10. Errores habituales y soluciones (FAQ)

### La página no carga / Error de conexión

**Problema:** El navegador muestra "No se puede acceder a este sitio" o tiempo de espera agotado.

**Solución:**
1. Verifica que Docker está corriendo: abre una terminal y ejecuta `docker ps`.
2. Comprueba que el contenedor `odoo` aparece como `Up`.
3. Si no está arrancado, ejecuta `docker-compose up -d` en la carpeta `erp/docker/`.
4. Espera 30-60 segundos y vuelve a cargar la página.

### "Acceso denegado" al abrir un menú

**Problema:** Aparece el mensaje "No tienes permisos para acceder a este recurso".

**Solución:**
1. Tu usuario no tiene el rol adecuado.
2. Pide al administrador que asigne el grupo correcto:
   - **Usuario**: solo lectura general.
   - **Moderador**: puede gestionar denuncias y moderar contenido.
   - **Administrador**: acceso completo.

### No aparecen datos en el listado

**Problema:** El listado de productos, usuarios o denuncias aparece vacío.

**Solución:**
1. Comprueba si hay filtros activos en la barra de búsqueda (elimínalos con la X).
2. Verifica que la base de datos tiene datos cargados (contacta con el administrador).
3. Si es la primera instalación, importa los datos demo desde **Configuración → Módulos**.

### El formulario no guarda / Aparece error de validación

**Problema:** Al guardar un formulario, aparece un mensaje de error en rojo.

**Solución:**
1. Lee el mensaje de error: indica qué campo es incorrecto.
2. Errores comunes:
   - **"Ya existe una etiqueta con este nombre"**: la etiqueta ya existe, búscala en el listado.
   - **"El motivo debe tener al menos 10 caracteres"**: amplía la descripción del motivo.
   - **"Debes especificar el producto/usuario/comentario denunciado"**: el tipo de denuncia no coincide con el campo rellenado.

### La imagen no sube

**Problema:** Al intentar subir una imagen, no se guarda o aparece error.

**Solución:**
1. Verifica que el archivo es JPG o PNG.
2. El tamaño máximo es 5 MB. Comprime la imagen si es mayor.
3. Si el error persiste, recarga la página y vuelve a intentarlo.

---

## 11. Glosario

| Término | Definición |
|---------|-----------|
| **Producto** | Artículo de segunda mano publicado por un usuario en la plataforma Renaix para su venta. |
| **Etiqueta** | Palabra clave normalizada (ej: `#gaming`, `#vintage`) que clasifica un producto. Un producto puede tener hasta 5 etiquetas. |
| **Estado del producto** | Condición física del artículo: Nuevo, Como Nuevo, Buen Estado, Estado Aceptable, Para Reparar. |
| **Estado de venta** | Fase en el ciclo de vida del producto: Borrador, Disponible, Reservado, Vendido, Eliminado. |
| **Incidencia / Denuncia** | Reporte realizado por un usuario sobre un producto, comentario u otro usuario que infringe las normas de la plataforma. |
| **Moderador** | Empleado con acceso a gestionar denuncias, editar productos y gestionar comentarios. |
| **Administrador** | Empleado con acceso completo a todos los módulos y configuraciones. |
| **Chatter** | Panel de historial de cambios y comunicación interna visible en la parte inferior de cada formulario. |
| **Valoración** | Puntuación (1-5 estrellas) que un comprador otorga a un vendedor tras completar una transacción. |
| **Categoría** | Clasificación principal del producto (ej: Electrónica, Ropa, Deporte). |
| **Compra** | Transacción registrada cuando un usuario adquiere un producto de otro usuario. |
| **JWT** | JSON Web Token. Mecanismo de autenticación segura usado por la API REST para verificar la identidad de usuarios de la app móvil. |

---

*Manual generado para el Proyecto Intermodular 2025-2026 — IES Eduardo Primo Marqués*
