# 🚀 Renaix API REST - Documentación Completa

## 📋 Índice
- [Descripción](#descripción)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Endpoints Disponibles](#endpoints-disponibles)
- [Autenticación JWT](#autenticación-jwt)
- [Ejemplos de Uso](#ejemplos-de-uso)
- [Testing con Thunder Client/Postman](#testing)

---

## 📖 Descripción

API REST completa para la aplicación móvil Renaix (marketplace de segunda mano) construida sobre Odoo 17/18.

**Características principales:**
- ✅ Autenticación JWT con access y refresh tokens
- ✅ CRUD completo de productos
- ✅ Sistema de compra-venta con estados
- ✅ Comentarios y valoraciones
- ✅ Mensajería entre usuarios
- ✅ Sistema de denuncias
- ✅ Búsqueda avanzada con filtros
- ✅ Gestión de imágenes
- ✅ Paginación en todos los listados
- ✅ Respuestas JSON estandarizadas
- ✅ CORS habilitado para desarrollo

---

## 📁 Estructura del Proyecto

```
renaix_api/
├── __manifest__.py                    # Configuración del módulo
├── __init__.py
│
├── config/
│   └── settings.py                    # Configuración JWT y API
│
├── controllers/                       # 🎮 Endpoints HTTP
│   ├── __init__.py
│   ├── auth.py                        # Login, registro, refresh, logout
│   ├── usuarios.py                    # Gestión de usuarios
│   ├── productos.py                   # CRUD productos + búsqueda
│   ├── compras.py                     # Flujo de compra-venta
│   ├── comentarios.py                 # Comentarios en productos
│   ├── valoraciones.py                # Sistema de ratings
│   ├── mensajes.py                    # Chat entre usuarios
│   ├── denuncias.py                   # Reportes
│   ├── categorias.py                  # Listar categorías
│   └── etiquetas.py                   # Listar/buscar etiquetas
│
└── models/
    ├── __init__.py
    └── utils/                         # 🛠️ Utilidades
        ├── __init__.py
        ├── jwt_utils.py               # Generación/verificación JWT
        ├── auth_helpers.py            # Hash de passwords
        ├── validators.py              # Validaciones de datos
        ├── serializers.py             # Modelo → JSON
        └── response_helpers.py        # Respuestas HTTP
```

---

## 🔧 Instalación

### Paso 1: Copiar el módulo

```bash
# Extraer el archivo
cd /ruta/a/tu/proyecto/custom_addons
tar -xzf renaix_api_completo.tar.gz

# O copiar manualmente la carpeta renaix_api/
```

### Paso 2: Instalar dependencias Python

```bash
# Dentro del contenedor de Odoo:
pip install PyJWT --break-system-packages
```

### Paso 3: Actualizar lista de módulos en Odoo

1. Ir a **Apps**
2. Click en **⋮** (tres puntos)  → **Update Apps List**
3. Buscar **"Renaix API REST"**
4. Click en **Install**

### Paso 4: Verificar instalación

Acceder a: `http://localhost:8069/api/v1/categorias`

Deberías ver un JSON con las categorías disponibles.

---

## ⚙️ Configuración

### Archivo: `config/settings.py`

```python
# ⚠️ IMPORTANTE: Cambiar en producción
JWT_SECRET_KEY = 'renaix_secret_key_2025_CHANGE_IN_PRODUCTION'

# Expiración de tokens
ACCESS_TOKEN_EXPIRATION_HOURS = 1      # Access token: 1 hora
REFRESH_TOKEN_EXPIRATION_DAYS = 7      # Refresh token: 7 días

# Contraseñas
PASSWORD_MIN_LENGTH = 6

# Paginación
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100

# CORS (útil para desarrollo)
CORS_ENABLED = True
```

**Para producción:**
1. Cambiar `JWT_SECRET_KEY` a un valor aleatorio seguro
2. Considerar reducir `REFRESH_TOKEN_EXPIRATION_DAYS`
3. Aumentar `PASSWORD_MIN_LENGTH` a 8
4. Configurar CORS solo para dominios específicos

---

## 🔐 Autenticación JWT

### Sistema de Dual Token

**Access Token** (1 hora):
- Usado en TODAS las peticiones autenticadas
- Se envía en header: `Authorization: Bearer <access_token>`
- Expira en 1 hora

**Refresh Token** (7 días):
- Solo para renovar el access token
- Se guarda en el cliente de forma segura
- Expira en 7 días

### Flujo de Autenticación

```
1. Usuario hace login/registro
   ↓
2. Recibe access_token + refresh_token
   ↓
3. Usa access_token en todas las peticiones (1h válido)
   ↓
4. Cuando access_token expira (401 error)
   ↓
5. Llama a /api/v1/auth/refresh con refresh_token
   ↓
6. Recibe nuevo access_token
   ↓
7. Si refresh_token expira (7 días) → Re-login completo
```

---

## 📡 Endpoints Disponibles

### 🔐 Autenticación (No requieren token)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/v1/auth/register` | Registrar nuevo usuario |
| POST | `/api/v1/auth/login` | Iniciar sesión |
| POST | `/api/v1/auth/refresh` | Renovar access token |
| POST | `/api/v1/auth/logout` | Cerrar sesión (requiere token) |

### 👤 Usuarios

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/v1/usuarios/perfil` | Obtener mi perfil |
| PUT | `/api/v1/usuarios/perfil` | Actualizar mi perfil |
| GET | `/api/v1/usuarios/{id}` | Ver perfil público |
| GET | `/api/v1/usuarios/perfil/productos` | Mis productos |
| GET | `/api/v1/usuarios/perfil/compras` | Mis compras |
| GET | `/api/v1/usuarios/perfil/ventas` | Mis ventas |
| GET | `/api/v1/usuarios/perfil/valoraciones` | Mis valoraciones |
| GET | `/api/v1/usuarios/perfil/estadisticas` | Mis estadísticas |

### 📦 Productos

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/v1/productos` | Listar productos (público) |
| GET | `/api/v1/productos/{id}` | Detalle producto (público) |
| POST | `/api/v1/productos` | Crear producto |
| PUT | `/api/v1/productos/{id}` | Actualizar producto |
| DELETE | `/api/v1/productos/{id}` | Eliminar producto |
| POST | `/api/v1/productos/{id}/publicar` | Publicar producto |
| GET | `/api/v1/productos/buscar` | Búsqueda avanzada (público) |
| POST | `/api/v1/productos/{id}/imagenes` | Añadir imagen |
| DELETE | `/api/v1/productos/{id}/imagenes/{img_id}` | Eliminar imagen |

### 🛒 Compras

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/v1/compras` | Comprar producto |
| GET | `/api/v1/compras/{id}` | Detalle de compra |
| POST | `/api/v1/compras/{id}/confirmar` | Confirmar (vendedor) |
| POST | `/api/v1/compras/{id}/completar` | Completar (comprador) |
| POST | `/api/v1/compras/{id}/cancelar` | Cancelar compra |

### 💬 Comentarios

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/v1/productos/{id}/comentarios` | Listar comentarios |
| POST | `/api/v1/productos/{id}/comentarios` | Crear comentario |
| DELETE | `/api/v1/comentarios/{id}` | Eliminar comentario |

### ⭐ Valoraciones

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/v1/compras/{id}/valorar` | Valorar transacción |
| GET | `/api/v1/usuarios/{id}/valoraciones` | Ver valoraciones |

### 💌 Mensajes

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/v1/mensajes/conversaciones` | Mis conversaciones |
| POST | `/api/v1/mensajes` | Enviar mensaje |
| PUT | `/api/v1/mensajes/{id}/marcar-leido` | Marcar como leído |

### 🚨 Denuncias

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/v1/denuncias` | Crear denuncia |
| GET | `/api/v1/denuncias/mis-denuncias` | Mis denuncias |

### 🏷️ Categorías y Etiquetas

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/v1/categorias` | Listar categorías |
| GET | `/api/v1/etiquetas` | Etiquetas populares |
| GET | `/api/v1/etiquetas/buscar?q=gaming` | Buscar etiquetas |

---

## 📝 Ejemplos de Uso

### 1. Registro de Usuario

```bash
POST http://localhost:8069/api/v1/auth/register
Content-Type: application/json

{
  "name": "Juan Pérez",
  "email": "juan@example.com",
  "password": "password123",
  "phone": "612345678"
}
```

**Respuesta:**
```json
{
  "success": true,
  "message": "Usuario registrado exitosamente",
  "data": {
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "user": {
      "id": 10,
      "name": "Juan Pérez",
      "email": "juan@example.com",
      "partner_gid": "123e4567-e89b-12d3-a456-426614174000",
      "valoracion_promedio": 0.0,
      ...
    }
  }
}
```

### 2. Login

```bash
POST http://localhost:8069/api/v1/auth/login
Content-Type: application/json

{
  "email": "juan@example.com",
  "password": "password123"
}
```

### 3. Crear Producto

```bash
POST http://localhost:8069/api/v1/productos
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
Content-Type: application/json

{
  "nombre": "iPhone 12 Pro",
  "descripcion": "Buen estado, batería al 85%",
  "precio": 450.00,
  "categoria_id": 1,
  "estado_producto": "como_nuevo",
  "antiguedad": "1_anno",
  "ubicacion": "Madrid",
  "etiqueta_ids": [1, 2]
}
```

### 4. Búsqueda Avanzada

```bash
GET http://localhost:8069/api/v1/productos/buscar?query=iphone&precio_max=500&categoria_id=1&page=1&limit=20
```

### 5. Comprar Producto

```bash
POST http://localhost:8069/api/v1/compras
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
Content-Type: application/json

{
  "producto_id": 5,
  "notas": "¿Puedo recogerlo mañana?"
}
```

### 6. Renovar Token

```bash
POST http://localhost:8069/api/v1/auth/refresh
Content-Type: application/json

{
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

## 🧪 Testing

### Con Thunder Client (VSCode)

1. Instalar extensión Thunder Client
2. Crear nueva Collection "Renaix API"
3. Añadir requests con las URLs de arriba
4. Guardar el `access_token` como variable de entorno

### Con Postman

1. Importar colección (crear manualmente)
2. Configurar variable de entorno `{{base_url}}` = `http://localhost:8069`
3. Configurar variable `{{access_token}}`
4. En la pestaña Authorization, usar Type: Bearer Token con `{{access_token}}`

### Flujo de Testing Recomendado

```
1. POST /auth/register → Guardar access_token
2. GET /categorias → Verificar que funciona
3. POST /productos → Crear producto de prueba
4. GET /productos → Ver que aparece
5. GET /productos/buscar?query=test
6. POST /auth/logout
```

---

## 🔒 Seguridad

### Buenas Prácticas Implementadas

✅ Passwords hasheados con werkzeug
✅ Tokens JWT firmados
✅ Validación de permisos en cada endpoint
✅ Cuentas desactivadas no pueden hacer login
✅ Refresh tokens revocables
✅ Validación de entrada en todos los endpoints

### Consideraciones de Producción

⚠️ Cambiar `JWT_SECRET_KEY`
⚠️ Configurar HTTPS
⚠️ Limitar rate de peticiones
⚠️ Configurar CORS solo para dominios específicos
⚠️ Implementar logging y monitoring
⚠️ Backup regular de la base de datos

---

## 📞 Soporte

**Desarrolladores:**
- Javier Herraiz
- Alejandro Sánchez

**Proyecto:** Sprint 2 - API REST para Renaix
**Tecnología:** Odoo 17/18 + PyJWT
**Fecha:** Enero 2026

---

## 📄 Licencia

LGPL-3

---

## ✅ Checklist de Evaluación

- [x] Autenticación JWT (access + refresh tokens)
- [x] Verificación centralizada de tokens
- [x] Gestión de usuarios (registro, perfil)
- [x] CRUD completo de productos
- [x] Sistema de compra-venta
- [x] Comentarios en productos
- [x] Sistema de valoraciones
- [x] Sistema de denuncias
- [x] Mensajería entre usuarios
- [x] Gestión de imágenes
- [x] Búsqueda avanzada con filtros
- [x] Paginación en listados
- [x] Respuestas JSON estandarizadas
- [x] Código modular y documentado
- [x] Validaciones de entrada
- [x] Manejo de errores

---

¡API REST completa y lista para usar! 🚀
