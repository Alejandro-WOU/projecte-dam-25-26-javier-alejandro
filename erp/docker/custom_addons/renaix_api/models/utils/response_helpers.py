# -*- coding: utf-8 -*-
"""
Helpers para respuestas HTTP estandarizadas
"""

import json
from odoo.http import request


def success_response(data=None, message='Operación exitosa', status=200):
    """
    Respuesta HTTP de éxito estandarizada.
    
    Args:
        data: Datos a devolver (dict, list, etc.)
        message: Mensaje descriptivo
        status: Código HTTP (default: 200)
    
    Returns:
        Response: Respuesta HTTP JSON
    """
    response_data = {
        'success': True,
        'message': message
    }
    
    if data is not None:
        response_data['data'] = data
    
    return request.make_json_response(response_data, status=status)


def error_response(error='Error en la operación', code='ERROR', status=400):
    """
    Respuesta HTTP de error estandarizada.
    
    Args:
        error: Mensaje de error
        code: Código de error (ej: 'INVALID_TOKEN', 'VALIDATION_ERROR')
        status: Código HTTP (default: 400)
    
    Returns:
        Response: Respuesta HTTP JSON
    """
    response_data = {
        'success': False,
        'error': error,
        'code': code
    }
    
    return request.make_json_response(response_data, status=status)


def paginated_response(items, total, page=1, limit=20, message='Datos recuperados'):
    """
    Respuesta HTTP paginada estandarizada.
    
    Args:
        items: Lista de elementos de la página actual
        total: Total de elementos disponibles
        page: Página actual
        limit: Elementos por página
        message: Mensaje descriptivo
    
    Returns:
        Response: Respuesta HTTP JSON con paginación
    """
    total_pages = (total + limit - 1) // limit  # Redondeo hacia arriba
    
    response_data = {
        'success': True,
        'message': message,
        'data': items,
        'pagination': {
            'total': total,
            'page': page,
            'limit': limit,
            'total_pages': total_pages,
            'has_next': page < total_pages,
            'has_prev': page > 1
        }
    }
    
    return request.make_json_response(response_data, status=200)


def unauthorized_response(message='No autorizado'):
    """
    Respuesta HTTP 401 Unauthorized.
    
    Args:
        message: Mensaje de error
    
    Returns:
        Response: Respuesta HTTP JSON 401
    """
    return error_response(
        error=message,
        code='UNAUTHORIZED',
        status=401
    )


def forbidden_response(message='Acceso prohibido'):
    """
    Respuesta HTTP 403 Forbidden.
    
    Args:
        message: Mensaje de error
    
    Returns:
        Response: Respuesta HTTP JSON 403
    """
    return error_response(
        error=message,
        code='FORBIDDEN',
        status=403
    )


def not_found_response(message='Recurso no encontrado'):
    """
    Respuesta HTTP 404 Not Found.
    
    Args:
        message: Mensaje de error
    
    Returns:
        Response: Respuesta HTTP JSON 404
    """
    return error_response(
        error=message,
        code='NOT_FOUND',
        status=404
    )


def validation_error_response(message='Error de validación'):
    """
    Respuesta HTTP 400 Bad Request para errores de validación.
    
    Args:
        message: Mensaje de error
    
    Returns:
        Response: Respuesta HTTP JSON 400
    """
    return error_response(
        error=message,
        code='VALIDATION_ERROR',
        status=400
    )


def server_error_response(message='Error interno del servidor'):
    """
    Respuesta HTTP 500 Internal Server Error.
    
    Args:
        message: Mensaje de error
    
    Returns:
        Response: Respuesta HTTP JSON 500
    """
    return error_response(
        error=message,
        code='INTERNAL_ERROR',
        status=500
    )
