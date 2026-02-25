# Module Renaix App

Aplicacion Android para el marketplace de productos de segunda mano Renaix.

## Arquitectura

El proyecto sigue **Clean Architecture** con patron **MVVM**:

- `data/` - Capa de datos (API, base de datos local, repositorios)
- `domain/` - Capa de dominio (modelos de negocio, interfaces)
- `presentation/` - Capa de presentacion (UI con Jetpack Compose, ViewModels)
- `di/` - Inyeccion de dependencias manual

## Tecnologias

- Jetpack Compose + Material 3
- Ktor Client
- SQLDelight
- Coroutines + Flow
- Google Maps
- Firebase Cloud Messaging

# Package com.renaix.data.remote.api

Cliente HTTP con Ktor para comunicacion con el backend Odoo.

# Package com.renaix.data.local

Persistencia local con SQLDelight y EncryptedSharedPreferences.

# Package com.renaix.domain.model

Modelos de negocio: User, Product, Category, Message, Comment, Rating, etc.

# Package com.renaix.domain.repository

Interfaces de repositorios que definen las operaciones de datos.

# Package com.renaix.presentation.screens

Pantallas de la aplicacion implementadas con Jetpack Compose.

# Package com.renaix.di

Contenedor de dependencias manual (AppContainer).
