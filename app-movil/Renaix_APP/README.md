# Renaix - App Movil Android

Marketplace de productos de segunda mano desarrollado con Jetpack Compose.

## Informacion del Proyecto

| Campo | Valor |
|-------|-------|
| Package | `com.renaix` |
| Min SDK | 26 (Android 8.0) |
| Target SDK | 35 |
| Lenguaje | Kotlin |

## Arquitectura

El proyecto sigue Clean Architecture con patron MVVM:

```
com.renaix/
├── data/
│   ├── local/
│   │   ├── database/        # SQLDelight (cache local)
│   │   └── preferences/     # EncryptedSharedPreferences
│   ├── remote/
│   │   ├── api/             # Ktor Client + RenaixApi
│   │   ├── datasource/      # Data Sources remotos
│   │   ├── dto/             # Request/Response DTOs
│   │   └── firebase/        # Firebase Cloud Messaging
│   ├── mapper/              # Mappers DTO <-> Domain
│   └── repository/          # Implementaciones de repositorios
├── domain/
│   ├── model/               # Modelos de negocio
│   └── repository/          # Interfaces de repositorios
├── presentation/
│   ├── screens/             # Pantallas (Screen + ViewModel)
│   ├── navigation/          # NavGraph
│   └── common/              # Componentes y estados reutilizables
├── di/                      # Inyeccion de dependencias manual
├── ui/theme/                # Tema Material 3
└── util/                    # Constantes y extensiones
```

## Stack Tecnologico

| Categoria | Tecnologia |
|-----------|------------|
| UI | Jetpack Compose + Material 3 |
| Navegacion | Navigation Compose |
| Networking | Ktor Client |
| Serializacion | Kotlinx Serialization |
| Base de Datos Local | SQLDelight |
| Almacenamiento Seguro | EncryptedSharedPreferences |
| Carga de Imagenes | Coil |
| Mapas | Google Maps Compose |
| Asincronia | Coroutines + Flow |
| Notificaciones Push | Firebase Cloud Messaging |
| DI | Manual (AppContainer) |

## Pantallas

| Pantalla | Descripcion |
|----------|-------------|
| Splash | Carga inicial y verificacion de sesion |
| Login | Inicio de sesion |
| Register | Registro de usuario |
| Main | Pantalla principal con navegacion |
| Product List | Lista de productos disponibles |
| Product Detail | Detalle con comentarios, valoraciones y mapa |
| Create Product | Crear nuevo producto con imagenes |
| Edit Product | Editar producto existente |
| Search | Busqueda con filtros (categoria, precio, orden) |
| Chat | Lista de conversaciones |
| Chat Detail | Mensajes de una conversacion |
| Map | Mapa con ubicacion de productos |
| Profile | Perfil de usuario |

## Modelos de Dominio

- **User** - Usuario con perfil y valoraciones
- **Product** - Producto con imagenes, estado y ubicacion
- **Category** - Categoria de productos
- **Message** - Mensaje de chat
- **Comment** - Comentario en producto
- **Rating** - Valoracion de usuario
- **Report** - Denuncia de producto/usuario
- **Purchase** - Compra/transaccion
- **Tag** - Etiqueta de producto

## Configuracion

### 1. Clonar el repositorio

```bash
git clone https://github.com/H3rr41z/Proyecto-Intermodular-DAM-2025.git
cd Proyecto-Intermodular-DAM-2025/app-movil/Renaix_APP
```

### 2. Configurar API Key de Google Maps

Editar el archivo `local.properties` en la raiz del proyecto:

```properties
MAPS_API_KEY=tu_api_key_de_google_maps
```

> Este archivo no se sube al repositorio por seguridad.

### 3. Configurar Backend

La app se conecta a un backend Odoo. La URL se configura en `util/Constants.kt`:

- **Emulador:** `http://10.0.2.2:8069` (apunta a localhost del PC)
- **Dispositivo fisico:** Usar IP de la maquina

### 4. Ejecutar

1. Abrir en Android Studio
2. Sync Gradle
3. Run en emulador o dispositivo

## Funcionalidades

### Autenticacion
- Login/Registro con JWT
- Persistencia segura de tokens con EncryptedSharedPreferences
- Sesion persistente entre reinicios

### Productos
- Listado con scroll infinito
- Detalle con galeria de imagenes
- Crear/Editar productos con subida de imagenes
- Busqueda con filtros:
  - Por texto (con debounce)
  - Por categoria
  - Por rango de precio
  - Ordenamiento (fecha, precio)

### Social
- Sistema de chat entre usuarios
- Comentarios en productos
- Valoraciones de usuarios
- Sistema de denuncias

### Mapas
- Visualizacion de ubicacion de productos
- Geolocalizacion del usuario

### Notificaciones
- Push notifications con Firebase Cloud Messaging

## Troubleshooting

| Error | Solucion |
|-------|----------|
| Cannot resolve symbol | Sync Gradle o Rebuild Project |
| Error de conexion a API | Verificar que el backend esta corriendo |
| Maps no funciona | Verificar `MAPS_API_KEY` en `local.properties` |

## Autores

**Javier Herraiz & Alejandro Sanchez**
Proyecto DAM 2025-26
