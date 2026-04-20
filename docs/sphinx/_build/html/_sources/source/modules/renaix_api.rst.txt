Módulo: renaix_api (API REST)
=============================

.. contents:: Tabla de contenidos
   :depth: 3
   :local:

Descripción funcional
---------------------

El módulo ``renaix_api`` expone una **API REST** segura con autenticación **JWT**
para servir datos a la aplicación móvil Android (Kotlin + Jetpack Compose).

**¿Qué resuelve?**

- Autenticación segura de usuarios móviles mediante JWT (access token + refresh token).
- CRUD completo de productos, imágenes, comentarios, etiquetas y valoraciones.
- Sistema de denuncias desde la app móvil.
- Mensajería privada entre usuarios.
- Búsqueda y filtrado de productos.
- Gestión del perfil de usuario.

Instalación y dependencias
---------------------------

.. code-block:: python

   # __manifest__.py
   'depends': [
       'base',
       'mail',
       'renaix',   # Requiere el módulo core
   ]

**Dependencias externas Python:**

- ``PyJWT``: para generación y verificación de tokens JWT.
- Instalado manualmente en el contenedor Docker.

.. code-block:: bash

   # En el contenedor Odoo
   pip install PyJWT

Estructura de archivos
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   renaix_api/
   ├── __init__.py
   ├── __manifest__.py
   ├── config/
   │   └── settings.py          # Configuración JWT (secreto, expiración)
   ├── controllers/
   │   ├── auth.py              # Login, registro, refresh, logout
   │   ├── productos.py         # CRUD de productos
   │   ├── categorias.py        # Listado de categorías
   │   ├── etiquetas.py         # Listado y búsqueda de etiquetas
   │   ├── comentarios.py       # Comentarios en productos
   │   ├── compras.py           # Transacciones de compraventa
   │   ├── valoraciones.py      # Valoraciones de usuarios
   │   ├── mensajes.py          # Mensajería privada
   │   ├── denuncias.py         # Sistema de denuncias
   │   └── usuarios.py          # Perfil y gestión de usuarios
   ├── models/
   │   └── utils/
   │       ├── jwt_utils.py     # Funciones JWT
   │       ├── auth_helpers.py  # Validaciones de autenticación
   │       ├── validators.py    # Validación de datos de entrada
   │       ├── response_helpers.py  # Helpers de respuesta HTTP
   │       └── serializers.py   # Serialización de modelos a JSON
   └── tests/
       └── test_api.py

Autenticación JWT
-----------------

El módulo usa autenticación basada en **JSON Web Tokens (JWT)**:

- **Access Token**: válido 24 horas. Se envía en la cabecera ``Authorization: Bearer <token>``.
- **Refresh Token**: válido 30 días. Permite renovar el access token sin volver a autenticarse.

**Flujo de autenticación:**

.. code-block:: text

   Cliente                              Servidor
      |                                    |
      |-- POST /api/v1/auth/login -------> |
      |   { email, password }              |
      |                                    |
      |<-- { access_token, refresh_token } |
      |                                    |
      |-- GET /api/v1/productos            |
      |   Authorization: Bearer <token> -> |
      |                                    |
      |<-- { productos }                   |
      |                                    |
      |-- POST /api/v1/auth/refresh -----> |
      |   { refresh_token }                |
      |                                    |
      |<-- { new_access_token }            |

**Formato de respuesta estándar:**

.. code-block:: json

   {
     "success": true,
     "message": "Descripción del resultado",
     "data": { ... },
     "status": 200
   }

**Formato de error:**

.. code-block:: json

   {
     "success": false,
     "error": "Descripción del error",
     "status": 400
   }

Endpoints de la API
-------------------

Autenticación
~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 10 35 25 30

   * - Método
     - URL
     - Auth
     - Descripción
   * - POST
     - ``/api/v1/auth/register``
     - Pública
     - Registro de nuevo usuario
   * - POST
     - ``/api/v1/auth/login``
     - Pública
     - Inicio de sesión, devuelve JWT
   * - POST
     - ``/api/v1/auth/refresh``
     - Pública (refresh token)
     - Renovar access token
   * - POST
     - ``/api/v1/auth/logout``
     - JWT requerido
     - Cerrar sesión (invalida tokens)

**Ejemplo — Login:**

.. code-block:: http

   POST /api/v1/auth/login HTTP/1.1
   Content-Type: application/json

   {
     "email": "usuario@example.com",
     "password": "miPassword123"
   }

.. code-block:: json

   {
     "success": true,
     "data": {
       "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
       "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
       "user": {
         "id": 42,
         "name": "Juan Pérez",
         "email": "usuario@example.com"
       }
     }
   }

Productos
~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 10 35 25 30

   * - Método
     - URL
     - Auth
     - Descripción
   * - GET
     - ``/api/v1/productos``
     - Pública
     - Listar productos disponibles (paginado)
   * - GET
     - ``/api/v1/productos/<id>``
     - Pública
     - Detalle de un producto
   * - POST
     - ``/api/v1/productos``
     - JWT requerido
     - Crear nuevo producto
   * - PUT
     - ``/api/v1/productos/<id>``
     - JWT requerido (propietario)
     - Actualizar producto
   * - DELETE
     - ``/api/v1/productos/<id>``
     - JWT requerido (propietario)
     - Eliminar (marcar eliminado) producto
   * - GET
     - ``/api/v1/productos/buscar``
     - Pública
     - Buscar productos con filtros
   * - POST
     - ``/api/v1/productos/<id>/imagenes``
     - JWT requerido
     - Subir imagen (base64)
   * - DELETE
     - ``/api/v1/productos/<id>/imagenes/<img_id>``
     - JWT requerido
     - Eliminar imagen de producto

**Ejemplo — Listar productos:**

.. code-block:: http

   GET /api/v1/productos?page=1&limit=20 HTTP/1.1

**Ejemplo — Crear producto:**

.. code-block:: http

   POST /api/v1/productos HTTP/1.1
   Authorization: Bearer <access_token>
   Content-Type: application/json

   {
     "name": "Bicicleta de montaña",
     "descripcion": "Buen estado, poco uso.",
     "precio": 150.00,
     "estado_producto": "buen_estado",
     "categoria_id": 3,
     "etiqueta_ids": [1, 4, 7],
     "ubicacion": "Valencia"
   }

Denuncias
~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 10 35 25 30

   * - Método
     - URL
     - Auth
     - Descripción
   * - POST
     - ``/api/v1/denuncias``
     - JWT requerido
     - Crear una nueva denuncia
   * - GET
     - ``/api/v1/denuncias/mis-denuncias``
     - JWT requerido
     - Listar denuncias del usuario autenticado

**Ejemplo — Crear denuncia:**

.. code-block:: http

   POST /api/v1/denuncias HTTP/1.1
   Authorization: Bearer <access_token>
   Content-Type: application/json

   {
     "tipo": "producto",
     "producto_id": 15,
     "categoria": "fraude",
     "motivo": "El producto no coincide con la descripción."
   }

Comentarios
~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 10 35 25 30

   * - Método
     - URL
     - Auth
     - Descripción
   * - GET
     - ``/api/v1/comentarios/producto/<id>``
     - Pública
     - Comentarios de un producto
   * - POST
     - ``/api/v1/comentarios``
     - JWT requerido
     - Añadir comentario
   * - DELETE
     - ``/api/v1/comentarios/<id>``
     - JWT requerido (autor)
     - Eliminar comentario propio

Usuarios
~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 10 35 25 30

   * - Método
     - URL
     - Auth
     - Descripción
   * - GET
     - ``/api/v1/usuarios/perfil``
     - JWT requerido
     - Ver perfil propio
   * - PUT
     - ``/api/v1/usuarios/perfil``
     - JWT requerido
     - Actualizar perfil (nombre, teléfono, foto)
   * - GET
     - ``/api/v1/usuarios/<id>/perfil-publico``
     - Pública
     - Ver perfil público de otro usuario

Mensajería
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 10 35 25 30

   * - Método
     - URL
     - Auth
     - Descripción
   * - GET
     - ``/api/v1/mensajes/conversaciones``
     - JWT requerido
     - Listar conversaciones del usuario
   * - GET
     - ``/api/v1/mensajes/conversaciones/<id>``
     - JWT requerido
     - Mensajes de una conversación
   * - POST
     - ``/api/v1/mensajes``
     - JWT requerido
     - Enviar mensaje

Códigos de estado HTTP
----------------------

.. list-table::
   :header-rows: 1
   :widths: 15 85

   * - Código
     - Significado
   * - 200
     - OK — Operación completada con éxito
   * - 201
     - Created — Recurso creado correctamente
   * - 400
     - Bad Request — Error de validación en los datos enviados
   * - 401
     - Unauthorized — Token JWT ausente, inválido o expirado
   * - 403
     - Forbidden — Sin permisos para realizar la operación
   * - 404
     - Not Found — Recurso no encontrado
   * - 409
     - Conflict — Conflicto (ej: email duplicado)
   * - 500
     - Internal Server Error — Error inesperado en el servidor

Referencia de API (autodoc)
----------------------------

.. automodule:: renaix_api.controllers.auth
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: renaix_api.controllers.productos
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: renaix_api.controllers.denuncias
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: renaix_api.controllers.comentarios
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: renaix_api.controllers.usuarios
   :members:
   :undoc-members:
   :show-inheritance:
