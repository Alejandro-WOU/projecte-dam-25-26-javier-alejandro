# -*- coding: utf-8 -*-
"""
Helpers para autenticación y gestión de passwords
"""

import re
from werkzeug.security import generate_password_hash, check_password_hash
from ...config import settings


def hash_password(password):
    """
    Hashea una contraseña usando werkzeug.
    
    Args:
        password (str): Contraseña en texto plano
    
    Returns:
        str: Hash de la contraseña
    """
    return generate_password_hash(password)


def verify_password(password, password_hash):
    """
    Verifica si una contraseña coincide con su hash.
    
    Args:
        password (str): Contraseña en texto plano
        password_hash (str): Hash almacenado
    
    Returns:
        bool: True si coincide, False si no
    """
    if not password_hash:
        return False
    return check_password_hash(password_hash, password)


def validate_email_format(email):
    """
    Valida el formato de un email.
    
    Args:
        email (str): Email a validar
    
    Returns:
        bool: True si el formato es válido
    """
    if not email:
        return False
    
    # Patrón básico de email
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_password_strength(password):
    """
    Valida la fortaleza de una contraseña según la configuración.
    
    Args:
        password (str): Contraseña a validar
    
    Returns:
        tuple: (bool, str) - (es_válida, mensaje_error)
    """
    if not password:
        return False, 'La contraseña no puede estar vacía'
    
    # Validar longitud mínima
    if len(password) < settings.PASSWORD_MIN_LENGTH:
        return False, f'La contraseña debe tener al menos {settings.PASSWORD_MIN_LENGTH} caracteres'
    
    # Validar mayúsculas (si está habilitado)
    if settings.PASSWORD_REQUIRE_UPPERCASE:
        if not any(c.isupper() for c in password):
            return False, 'La contraseña debe contener al menos una mayúscula'
    
    # Validar números (si está habilitado)
    if settings.PASSWORD_REQUIRE_NUMBERS:
        if not any(c.isdigit() for c in password):
            return False, 'La contraseña debe contener al menos un número'
    
    return True, ''


def generate_api_token():
    """
    Genera un token aleatorio para refresh tokens.
    
    Returns:
        str: Token aleatorio (UUID)
    """
    import uuid
    return str(uuid.uuid4())


def validate_phone_number(phone):
    """
    Valida formato básico de número de teléfono.
    
    Args:
        phone (str): Número de teléfono
    
    Returns:
        bool: True si el formato es válido
    """
    if not phone:
        return True  # Opcional
    
    # Patrón básico: permite +, espacios, guiones y números
    pattern = r'^[\+]?[(]?[0-9]{1,4}[)]?[-\s\.]?[(]?[0-9]{1,4}[)]?[-\s\.]?[0-9]{1,9}$'
    return re.match(pattern, phone.replace(' ', '')) is not None
