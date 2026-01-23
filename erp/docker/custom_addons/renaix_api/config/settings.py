# -*- coding: utf-8 -*-
"""
Configuración centralizada de la API REST Renaix
"""

# ========================================
# CONFIGURACIÓN JWT
# ========================================

# Clave secreta para firmar los tokens JWT
# ⚠️ CAMBIAR EN PRODUCCIÓN
JWT_SECRET_KEY = 'renaix_secret_key_2025_CHANGE_IN_PRODUCTION'

# Algoritmo de cifrado
JWT_ALGORITHM = 'HS256'

# Tiempo de expiración de tokens
ACCESS_TOKEN_EXPIRATION_HOURS = 1      # Access token: 1 hora
REFRESH_TOKEN_EXPIRATION_DAYS = 7      # Refresh token: 7 días

# ========================================
# CONFIGURACIÓN DE PASSWORDS
# ========================================

# Longitud mínima de contraseña
PASSWORD_MIN_LENGTH = 6

# Requiere mayúsculas (deshabilitado por simplicidad)
PASSWORD_REQUIRE_UPPERCASE = False

# Requiere números (deshabilitado por simplicidad)
PASSWORD_REQUIRE_NUMBERS = False

# ========================================
# CONFIGURACIÓN DE PAGINACIÓN
# ========================================

# Número de resultados por defecto por página
DEFAULT_PAGE_SIZE = 20

# Máximo de resultados por página
MAX_PAGE_SIZE = 100

# ========================================
# CONFIGURACIÓN CORS
# ========================================

# Permitir CORS (útil para desarrollo y testing)
CORS_ENABLED = True

# Orígenes permitidos (* = todos)
CORS_ORIGINS = '*'

# ========================================
# CONFIGURACIÓN DE BÚSQUEDA
# ========================================

# Número máximo de productos en búsqueda
MAX_SEARCH_RESULTS = 100

# ========================================
# CONFIGURACIÓN DE IMÁGENES
# ========================================

# Tamaño máximo de imagen (en MB)
MAX_IMAGE_SIZE_MB = 5

# Número máximo de imágenes por producto
MAX_IMAGES_PER_PRODUCT = 10

# ========================================
# CONFIGURACIÓN DE MENSAJES
# ========================================

# Longitud máxima de mensaje
MAX_MESSAGE_LENGTH = 2000

# Longitud máxima de comentario
MAX_COMMENT_LENGTH = 1000
