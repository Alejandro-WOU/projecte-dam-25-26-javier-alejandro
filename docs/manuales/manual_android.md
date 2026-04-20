# Manual de Usuario — App Android Renaix

**Proyecto:** Renaix — Marketplace de Segunda Mano
**Versión:** 1.0.0
**Fecha:** Marzo 2026
**Autores:** Javier Herraiz Calatayud & Alejandro Sánchez Serrano
**Plataforma:** Android (Kotlin + Jetpack Compose)

---

## Índice

1. [Instalación y requisitos](#1-instalación-y-requisitos)
2. [Inicio de sesión y registro](#2-inicio-de-sesión-y-registro)
3. [Pantalla principal y navegación](#3-pantalla-principal-y-navegación)
4. [Listado y búsqueda de productos](#4-listado-y-búsqueda-de-productos)
5. [Detalle de producto](#5-detalle-de-producto)
6. [Alta de producto (crear)](#6-alta-de-producto-crear)
7. [Edición de producto](#7-edición-de-producto)
8. [Denuncias](#8-denuncias)
9. [Perfil de usuario](#9-perfil-de-usuario)
10. [Chat / Mensajería](#10-chat--mensajería)
11. [Casos típicos paso a paso](#11-casos-típicos-paso-a-paso)
12. [Problemas frecuentes y soluciones](#12-problemas-frecuentes-y-soluciones)
13. [Glosario](#13-glosario)

---

## 1. Instalación y requisitos

### 1.1 Requisitos del dispositivo

| Requisito | Detalle |
|-----------|---------|
| **Sistema operativo** | Android 8.0 (API 26) o superior |
| **Espacio libre** | Mínimo 100 MB |
| **Conexión** | Wi-Fi o datos móviles (misma red que el servidor si es local) |
| **Permisos requeridos** | Cámara, Almacenamiento, Internet |

### 1.2 Instalación mediante APK

1. Descarga el archivo `renaix-app.apk` desde el repositorio del proyecto o desde el enlace proporcionado por el equipo.
2. En tu dispositivo Android, ve a **Ajustes → Seguridad** (o **Privacidad**).
3. Activa la opción **"Instalar aplicaciones de fuentes desconocidas"** (o **"Instalar apps desconocidas"** en Android 8+).
4. Abre el archivo APK descargado desde el gestor de archivos.
5. Toca **"Instalar"** y espera a que finalice la instalación.
6. Toca **"Abrir"** para lanzar la app.

### 1.3 Permisos necesarios

La primera vez que uses ciertas funciones, la app solicitará permisos:

- **Cámara**: necesario para hacer fotos de productos.
- **Almacenamiento / Archivos**: necesario para seleccionar imágenes de la galería.
- **Notificaciones**: para recibir alertas de mensajes (Android 13+).

> Acepta todos los permisos para disfrutar de la funcionalidad completa.

### 1.4 Primera apertura

Al abrir la app por primera vez:
1. Aparece la pantalla de **Splash** con el logo de Renaix durante 2-3 segundos.
2. La app verifica si hay una sesión activa guardada.
   - Si existe sesión previa: vas directamente a la pantalla principal.
   - Si no hay sesión: vas a la pantalla de **Login**.

---

## 2. Inicio de sesión y registro

### 2.1 Iniciar sesión

1. En la pantalla de **Login**, introduce tu **email** y **contraseña**.
2. Toca el botón **"Iniciar sesión"**.
3. Si las credenciales son correctas, accedes a la pantalla principal.
4. La sesión queda guardada automáticamente (no necesitas volver a introducir datos al reabrir la app).

> **Credenciales de prueba:**
> - Email: `usuario@renaix.com`
> - Contraseña: `renaix123`

### 2.2 Registrarse (nuevo usuario)

1. En la pantalla de Login, toca **"¿No tienes cuenta? Regístrate"**.
2. Rellena el formulario de registro:
   - **Nombre completo** *
   - **Email** * (debe ser único)
   - **Contraseña** * (mínimo 8 caracteres)
   - **Teléfono** (opcional)
3. Toca **"Crear cuenta"**.
4. Si el registro es exitoso, accedes directamente a la pantalla principal.

**Requisitos de contraseña:**
- Mínimo 8 caracteres.
- Al menos una letra mayúscula.
- Al menos un número.

### 2.3 Mantener la sesión activa

La sesión se mantiene automáticamente usando tokens JWT seguros almacenados en el dispositivo. No es necesario volver a hacer login mientras:
- No cierres sesión manualmente.
- No pase el tiempo de expiración del token (7 días).

### 2.4 Cerrar sesión

1. Ve a la pestaña **Perfil** (icono de persona en la barra inferior).
2. Desplázate hacia abajo y toca **"Cerrar sesión"**.
3. Confirma en el diálogo emergente.
4. Serás redirigido a la pantalla de Login. Los datos locales del usuario se borran del dispositivo.

---

## 3. Pantalla principal y navegación

### 3.1 Barra de navegación inferior

La app usa una barra de navegación con 5 pestañas:

| Icono | Pestaña | Función |
|-------|---------|---------|
| 🏠 | **Inicio** | Listado principal de productos disponibles |
| 🔍 | **Buscar** | Búsqueda y filtros avanzados |
| ➕ | **Publicar** | Crear nuevo producto |
| 💬 | **Chats** | Conversaciones con otros usuarios |
| 👤 | **Perfil** | Tu perfil y ajustes |

### 3.2 Pantalla de inicio

Al acceder a la pestaña **Inicio** verás:
- **Barra de búsqueda rápida** en la parte superior.
- **Grid de productos** disponibles ordenados por fecha de publicación (más recientes primero).
- Cada tarjeta de producto muestra: imagen principal, nombre, precio y ubicación.
- Desliza hacia abajo para cargar más productos (paginación infinita).

---

## 4. Listado y búsqueda de productos

### 4.1 Explorar el catálogo

1. Desde la pestaña **Inicio** (o **Buscar**), verás el grid de productos.
2. Desliza hacia abajo para ver más productos.
3. Toca cualquier tarjeta para ver el detalle completo.

### 4.2 Búsqueda por texto

1. Toca la **barra de búsqueda** en la parte superior.
2. Escribe el término a buscar (nombre del producto, marca, etc.).
3. Los resultados se actualizan en tiempo real.
4. Para limpiar la búsqueda, toca la X dentro del campo.

### 4.3 Filtrar y ordenar

1. Ve a la pestaña **Buscar** (icono de lupa).
2. Usa los filtros disponibles:
   - **Categoría**: Electrónica, Ropa, Deporte, etc.
   - **Estado**: Nuevo, Como Nuevo, Buen Estado…
   - **Precio**: introduce rango mínimo y/o máximo.
   - **Etiquetas**: busca por hashtags (#gaming, #vintage…).
3. Toca **"Aplicar filtros"** para ver los resultados.
4. Para eliminar filtros, toca **"Limpiar"**.

---

## 5. Detalle de producto

### 5.1 Ver detalle

1. Toca cualquier tarjeta de producto desde el listado.
2. Se abre la pantalla de detalle con:
   - **Galería de imágenes** (desliza horizontalmente para ver todas).
   - **Nombre** y **precio** del producto.
   - **Estado** (condición física y estado de venta).
   - **Descripción** completa.
   - **Ubicación** del vendedor.
   - **Etiquetas** asociadas.
   - **Información del vendedor**: nombre, valoración, número de ventas.
   - **Comentarios** de otros usuarios.
   - **Botones de acción**: Comprar, Favorito, Chat con vendedor, Denunciar.

### 5.2 Añadir a favoritos

1. En la pantalla de detalle, toca el icono de corazón (♡).
2. El corazón se rellena (❤️) indicando que está en favoritos.
3. Para quitar de favoritos, toca de nuevo el corazón.
4. Tus favoritos están disponibles en **Perfil → Mis Favoritos**.

### 5.3 Contactar al vendedor

1. En la pantalla de detalle, toca **"Enviar mensaje"** o el icono de chat.
2. Se abre la conversación directa con el vendedor.
3. Escribe tu mensaje y toca **Enviar**.

### 5.4 Comentar un producto

1. En la pantalla de detalle, desplázate hasta la sección **"Comentarios"**.
2. Toca el campo de texto **"Escribe un comentario..."**.
3. Escribe tu comentario y toca el botón de enviar (➤).
4. Tu comentario aparece en el listado.

---

## 6. Alta de producto (crear)

### 6.1 Crear un nuevo producto

1. Toca el botón central **➕** en la barra de navegación.
2. Se abre el formulario **"Nuevo Producto"**.

### 6.2 Rellenar el formulario

Rellena los campos del formulario:

**Campos obligatorios:**
- **Nombre del producto** *: escribe un título claro y descriptivo.
- **Precio** *: introduce el precio en euros (usa el teclado numérico).
- **Descripción**: detalla el estado, características y cualquier defecto.
- **Estado del producto** *: selecciona la condición física.
- **Categoría** *: elige la categoría más adecuada.

**Campos opcionales:**
- **Antigüedad**: indica cuánto tiempo llevas con el producto.
- **Ubicación**: tu ciudad o código postal.
- **Etiquetas**: añade hasta 5 hashtags para mejorar la visibilidad.

### 6.3 Añadir imágenes

1. En el formulario, toca el área de imágenes o el botón **"Añadir foto"**.
2. Elige una opción:
   - **Cámara**: hace una foto en el momento.
   - **Galería**: selecciona desde tus fotos guardadas.
3. Puedes añadir hasta **10 imágenes**.
4. La primera imagen añadida será la **imagen principal** (portada).
5. Para reordenar: mantén pulsada una imagen y arrástrala a la posición deseada.
6. Para eliminar: toca la imagen y selecciona el icono de papelera.

### 6.4 Publicar el producto

1. Una vez relleno el formulario, toca **"Publicar"**.
2. El producto se crea con estado **"Disponible"** y queda visible para otros usuarios.
3. Para guardar como borrador (sin publicar), toca **"Guardar borrador"**.

---

## 7. Edición de producto

### 7.1 Acceder a mis productos

1. Ve a la pestaña **Perfil**.
2. Toca **"Mis productos"**.
3. Verás la lista de tus productos publicados y borradores.

### 7.2 Editar un producto

1. En **Mis productos**, toca el producto que deseas editar.
2. Toca el icono de lápiz (✏️) o el botón **"Editar"**.
3. Modifica los campos que necesites (nombre, descripción, precio, imágenes, etiquetas…).
4. Toca **"Guardar cambios"** para confirmar.

### 7.3 Cambiar el estado del producto

Desde **Mis productos** o desde el detalle del producto:
1. Toca **"Cambiar estado"** o el selector de estado.
2. Selecciona el nuevo estado:
   - **Disponible**: activo en el marketplace.
   - **Reservado**: reservado para un comprador específico.
   - **Vendido**: transacción completada.
3. Confirma el cambio.

### 7.4 Eliminar un producto

1. Desde **Mis productos**, desliza la tarjeta del producto hacia la izquierda.
2. Toca el botón **"Eliminar"** (rojo).
3. Confirma en el diálogo emergente.

> El producto pasará a estado **"Eliminado"** y dejará de ser visible en el marketplace.

---

## 8. Denuncias

### 8.1 Denunciar un producto

1. Abre el producto que deseas denunciar.
2. Toca el icono de bandera (🚩) o el botón **"Denunciar"** (visible en la esquina superior derecha o al final del detalle).
3. Rellena el formulario de denuncia:
   - **Categoría**: Spam, Fraude/Estafa, Contenido Inapropiado, Violencia, Información Falsa, Otro.
   - **Motivo**: describe el problema con detalle (mínimo 10 caracteres).
4. Toca **"Enviar denuncia"**.
5. Aparece un mensaje de confirmación: "Denuncia enviada. Nuestro equipo la revisará."

### 8.2 Denunciar un comentario

1. Mantén pulsado el comentario que deseas denunciar.
2. En el menú contextual, selecciona **"Denunciar comentario"**.
3. Elige la categoría y escribe el motivo.
4. Toca **"Enviar"**.

### 8.3 Denunciar un usuario

1. Accede al perfil público del usuario (toca su nombre en cualquier producto o comentario).
2. Toca el icono de tres puntos (⋮) o **"Denunciar usuario"**.
3. Completa el formulario de denuncia.
4. Toca **"Enviar denuncia"**.

### 8.4 Ver mis denuncias

1. Ve a **Perfil → Mis denuncias**.
2. Verás el historial de denuncias que has enviado con su estado actual:
   - **Pendiente**: en espera de revisión.
   - **En revisión**: un moderador está analizando el caso.
   - **Resuelta**: la denuncia fue atendida.
   - **Rechazada**: la denuncia no fue considerada procedente.

---

## 9. Perfil de usuario

### 9.1 Ver tu perfil

1. Toca la pestaña **Perfil** (icono de persona) en la barra inferior.
2. Verás tu información: nombre, foto, email, teléfono, valoración promedio.
3. También aparecen estadísticas: productos publicados, vendidos y comprados.

### 9.2 Editar tu perfil

1. En la pantalla de Perfil, toca **"Editar perfil"** o el icono de lápiz.
2. Modifica los campos que desees:
   - **Nombre**
   - **Teléfono**
   - **Foto de perfil**: toca la imagen actual para cambiarla (cámara o galería).
3. Toca **"Guardar cambios"**.

### 9.3 Ver perfil público de otro usuario

1. Desde el detalle de cualquier producto, toca el nombre o foto del vendedor.
2. Se abre su perfil público con: nombre, foto, valoración, número de ventas y sus productos activos.

### 9.4 Mis compras y mis ventas

Desde la pestaña **Perfil** puedes acceder a:

- **Mis compras**: listado de productos que has comprado con estado de cada transacción.
- **Mis ventas**: listado de productos vendidos con información del comprador.
- **Mis favoritos**: productos que has marcado con corazón.
- **Mis denuncias**: historial de denuncias enviadas (ver sección 8.4).

---

## 10. Chat / Mensajería

### 10.1 Ver conversaciones

1. Toca la pestaña **Chats** (icono de burbuja de diálogo) en la barra inferior.
2. Aparece la lista de conversaciones activas con otros usuarios.
3. Cada conversación muestra: foto y nombre del usuario, último mensaje y hora.
4. Las conversaciones con mensajes no leídos aparecen resaltadas.

### 10.2 Enviar un mensaje

1. Desde la lista de chats, toca una conversación para abrirla.
2. Escribe tu mensaje en el campo de texto inferior.
3. Toca el icono de enviar (➤) o pulsa Enter.

Para iniciar una nueva conversación:
1. Ve al detalle de un producto.
2. Toca **"Enviar mensaje al vendedor"**.
3. Se crea automáticamente una conversación nueva.

---

## 11. Casos típicos paso a paso

### Caso 1: Crear un producto con foto y etiquetas

1. Toca **➕** en la barra de navegación.
2. Escribe el **nombre** del producto (ej: "Bicicleta de montaña Trek").
3. Introduce el **precio** (ej: `150`).
4. Escribe una **descripción** detallada.
5. Selecciona **Estado del producto**: `Buen Estado`.
6. Selecciona **Categoría**: `Deporte`.
7. Toca **"Añadir foto"** → **Galería** → selecciona 3 fotos de la bicicleta.
8. En el campo **Etiquetas**, escribe `bicicleta` → selecciona. Repite con `deporte`, `trek`.
9. Toca **"Publicar"**.
10. ✅ El producto aparece en el marketplace.

### Caso 2: Editar etiquetas de un producto existente

1. Ve a **Perfil → Mis productos**.
2. Toca el producto que deseas editar.
3. Toca **"Editar"** (icono de lápiz).
4. En el campo **Etiquetas**, toca la X junto a la etiqueta que deseas eliminar.
5. Escribe una nueva etiqueta y selecciónala de la lista.
6. Toca **"Guardar cambios"**.
7. ✅ Las etiquetas actualizadas son visibles en el detalle del producto.

### Caso 3: Denunciar y consultar el estado

1. Abre el producto que contiene contenido inapropiado.
2. Toca el icono de bandera (🚩).
3. Selecciona categoría: `Contenido Inapropiado`.
4. Escribe el motivo: "Este producto contiene imágenes inapropiadas que no son del artículo descrito."
5. Toca **"Enviar denuncia"**.
6. Ve a **Perfil → Mis denuncias**.
7. ✅ Verás tu denuncia con estado `Pendiente`.

---

## 12. Problemas frecuentes y soluciones

### Sin conexión / "No se puede conectar al servidor"

**Síntoma:** La app muestra un mensaje de error de red o no carga los productos.

**Solución:**
1. Verifica que tu dispositivo tiene conexión a Internet (Wi-Fi o datos).
2. Si el servidor es local, asegúrate de estar en la misma red Wi-Fi que el servidor.
3. Si el servidor está en la nube, verifica que esté operativo.
4. Cierra y vuelve a abrir la app.
5. Si el problema persiste, espera unos minutos y vuelve a intentarlo.

### Token caducado / "Sesión expirada"

**Síntoma:** La app muestra "Tu sesión ha caducado. Inicia sesión de nuevo."

**Solución:**
1. La sesión expira automáticamente tras 7 días de inactividad.
2. Ve a la pantalla de Login (la app te redirige automáticamente).
3. Introduce tus credenciales de nuevo.
4. La nueva sesión se inicia y se guarda automáticamente.

### Error al subir imagen

**Síntoma:** Al añadir una foto a un producto, aparece "Error al subir imagen" o la imagen no aparece.

**Solución:**
1. Verifica que la app tiene permiso de **Almacenamiento** (Ajustes → Aplicaciones → Renaix → Permisos).
2. Comprueba que el archivo es JPG o PNG y no supera 5 MB.
3. Asegúrate de tener conexión estable. Las imágenes requieren más ancho de banda.
4. Intenta seleccionar la imagen de nuevo.
5. Si el error persiste, reinicia la app e intenta de nuevo.

### La app se cierra inesperadamente (crash)

**Síntoma:** La app se cierra sola al realizar una acción.

**Solución:**
1. Cierra la app completamente (desde el selector de apps recientes).
2. Vuelve a abrirla.
3. Si el problema es recurrente, desinstala y reinstala la app desde el APK.
4. Verifica que tu dispositivo tiene Android 8.0 o superior.

### No aparecen mis productos

**Síntoma:** En **Mis Productos** la lista aparece vacía aunque has publicado productos.

**Solución:**
1. Asegúrate de que la sesión es correcta (Perfil → comprueba tu nombre de usuario).
2. Desliza hacia abajo para refrescar la lista.
3. Si creaste productos como borrador, verifica que el filtro no oculte borradores.

---

## 13. Glosario

| Término | Definición |
|---------|-----------|
| **Producto** | Artículo de segunda mano publicado en la plataforma para su venta. |
| **Etiqueta** | Hashtag normalizado (ej: `#gaming`) que clasifica un producto. Máximo 5 por producto. |
| **Estado del producto** | Condición física: Nuevo, Como Nuevo, Buen Estado, Estado Aceptable, Para Reparar. |
| **Estado de venta** | Fase del ciclo de vida: Disponible, Reservado, Vendido. |
| **Favorito** | Producto marcado con corazón para guardarlo en tu lista personal. |
| **Denuncia** | Reporte de contenido inapropiado enviado a los moderadores de la plataforma. |
| **Valoración** | Puntuación de 1 a 5 estrellas que un comprador otorga a un vendedor. |
| **JWT** | Token de autenticación seguro guardado en el dispositivo para mantener la sesión. |
| **Splash** | Pantalla de inicio con el logo que aparece al abrir la app. |
| **APK** | Formato de archivo de instalación de aplicaciones Android. |
| **Borrador** | Producto guardado pero no publicado, invisible para otros usuarios. |

---

*Manual generado para el Proyecto Intermodular 2025-2026 — IES Eduardo Primo Marqués*
