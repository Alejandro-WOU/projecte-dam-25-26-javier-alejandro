Seguridad y control de acceso
==============================

.. contents::
   :depth: 2
   :local:

Grupos de acceso (Odoo)
------------------------

El módulo ``renaix`` define 4 grupos de seguridad mediante ``security/security.xml``:

.. list-table::
   :header-rows: 1
   :widths: 20 30 50

   * - Grupo
     - ID técnico
     - Descripción
   * - Usuario
     - ``renaix.group_renaix_user``
     - Acceso de solo lectura. Para empleados básicos o revisores.
   * - Moderador
     - ``renaix.group_renaix_moderador``
     - Puede gestionar denuncias, moderar comentarios, editar productos.
   * - Administrador
     - ``renaix.group_renaix_admin``
     - Acceso CRUD completo a todos los modelos.
   * - Manager
     - ``renaix.group_renaix_manager``
     - Acceso total + configuración del sistema.

Permisos por modelo (ir.model.access.csv)
-----------------------------------------

La siguiente tabla resume los permisos de cada grupo sobre los modelos principales:

.. list-table::
   :header-rows: 1
   :widths: 30 10 12 12 12 12 12

   * - Modelo
     - Permisos
     - Usuario
     - Moderador
     - Admin
     - Manager
     - Público (API)
   * - ``renaix.producto``
     - RWCD
     - R
     - RWC**D**
     - RWCD
     - RWCD
     - R (GET)
   * - ``renaix.etiqueta``
     - RWCD
     - R
     - RWC
     - RWCD
     - RWCD
     - R (GET)
   * - ``renaix.denuncia``
     - RWCD
     - RC
     - RWCD
     - RWCD
     - RWCD
     - C (POST, con JWT)
   * - ``renaix.comentario``
     - RWCD
     - R
     - RWCD
     - RWCD
     - RWCD
     - R/C (con JWT)
   * - ``renaix.compra``
     - RWCD
     - R
     - RWC
     - RWCD
     - RWCD
     - R/C (con JWT)
   * - ``renaix.valoracion``
     - RWCD
     - R
     - RWCD
     - RWCD
     - RWCD
     - C (con JWT)
   * - ``renaix.mensaje``
     - RWCD
     - RWC
     - RWCD
     - RWCD
     - RWCD
     - R/C (con JWT)

*R=Read, W=Write, C=Create, D=Delete*

Autenticación API (JWT)
------------------------

La API REST del módulo ``renaix_api`` usa **JWT (JSON Web Tokens)**:

**Generación del token:**

1. El cliente envía credenciales al endpoint ``POST /api/v1/auth/login``.
2. El servidor verifica el email y contraseña (hash bcrypt).
3. Si son válidas, genera un **access token** (24h) y un **refresh token** (30 días).
4. El cliente almacena los tokens de forma segura (``EncryptedSharedPreferences`` en Android).

**Verificación:**

Cada endpoint protegido ejecuta ``jwt_utils.verify_token(request)`` que:

1. Extrae el token de la cabecera ``Authorization: Bearer <token>``.
2. Verifica la firma con la clave secreta configurada.
3. Comprueba que no ha expirado.
4. Recupera el ``res.partner`` correspondiente al ``partner_id`` del payload.

**Seguridad en la app móvil:**

- Los tokens se guardan en ``EncryptedSharedPreferences`` (cifrado AES-256 en Android).
- El refresh token permite renovar la sesión sin exponer la contraseña.
- Al cerrar sesión, los tokens se invalidan en el servidor.

Buenas prácticas aplicadas
---------------------------

- Contraseñas almacenadas con **hash bcrypt** (nunca en texto plano).
- CORS configurado en todos los endpoints para control de origen.
- CSRF desactivado en endpoints API (usan JWT en lugar de cookies).
- Validación de entrada en todos los endpoints (``validators.py``).
- Logging de errores sin exponer información sensible al cliente.
- Separación de responsabilidades: la lógica de negocio en modelos Odoo, la API solo serializa.
