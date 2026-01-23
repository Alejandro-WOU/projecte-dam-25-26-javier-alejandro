# -*- coding: utf-8 -*-
"""
Utilidades para manejo de JWT (JSON Web Tokens)
"""

import jwt
import logging
from datetime import datetime, timedelta
from odoo.http import request
from odoo.exceptions import AccessDenied
from ...config import settings

_logger = logging.getLogger(__name__)


def generate_access_token(partner):
    """
    Genera un access token JWT para un usuario.
    
    Args:
        partner (res.partner): Usuario autenticado
    
    Returns:
        str: Token JWT
    """
    # Calcular tiempo de expiración
    expiration = datetime.utcnow() + timedelta(
        hours=settings.ACCESS_TOKEN_EXPIRATION_HOURS
    )
    
    # Payload del token
    payload = {
        'user_id': partner.id,
        'partner_gid': partner.partner_gid,
        'email': partner.email,
        'iat': datetime.utcnow(),  # Issued at
        'exp': expiration,          # Expiration
        'type': 'access'            # Tipo de token
    }
    
    # Generar token
    token = jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    
    return token


def generate_refresh_token(partner):
    """
    Genera un refresh token JWT para renovar el access token.
    
    Args:
        partner (res.partner): Usuario autenticado
    
    Returns:
        str: Refresh token JWT
    """
    # Calcular tiempo de expiración (más largo)
    expiration = datetime.utcnow() + timedelta(
        days=settings.REFRESH_TOKEN_EXPIRATION_DAYS
    )
    
    # Payload del refresh token
    payload = {
        'user_id': partner.id,
        'partner_gid': partner.partner_gid,
        'iat': datetime.utcnow(),
        'exp': expiration,
        'type': 'refresh'  # Tipo de token
    }
    
    # Generar token
    token = jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    
    # Guardar en BD para poder invalidarlo después
    partner.sudo().write({'api_token': token})
    
    return token


def verify_token(http_request):
    """
    Verifica el token JWT del header Authorization y devuelve el usuario.
    
    Args:
        http_request: Request HTTP de Odoo
    
    Returns:
        res.partner: Usuario autenticado
    
    Raises:
        Exception: Si el token es inválido o ha expirado
    """
    # Extraer token del header Authorization
    auth_header = http_request.httprequest.headers.get('Authorization')
    
    if not auth_header:
        raise Exception('Token no proporcionado')
    
    # Formato: "Bearer <token>"
    parts = auth_header.split()
    
    if len(parts) != 2 or parts[0].lower() != 'bearer':
        raise Exception('Formato de token inválido. Use: Bearer <token>')
    
    token = parts[1]
    
    try:
        # Decodificar token
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        
        # Verificar que sea un access token
        if payload.get('type') != 'access':
            raise Exception('Tipo de token inválido')
        
        # Obtener user_id del payload
        user_id = payload.get('user_id')
        
        if not user_id:
            raise Exception('Token inválido: falta user_id')
        
        # Buscar usuario en la BD
        partner = http_request.env['res.partner'].sudo().browse(user_id)
        
        if not partner.exists():
            raise Exception('Usuario no encontrado')
        
        # Verificar que sea usuario app
        if not partner.es_usuario_app:
            raise Exception('Usuario no autorizado')
        
        # Verificar que la cuenta esté activa
        if not partner.cuenta_activa:
            raise Exception('Cuenta desactivada')
        
        # Actualizar última actividad
        partner.sudo().write({
            'fecha_ultima_actividad': datetime.now()
        })
        
        return partner
        
    except jwt.ExpiredSignatureError:
        _logger.warning('Token expirado')
        raise Exception('Token expirado')
    
    except jwt.InvalidTokenError as e:
        _logger.warning(f'Token inválido: {str(e)}')
        raise Exception('Token inválido')
    
    except Exception as e:
        _logger.error(f'Error al verificar token: {str(e)}')
        raise


def verify_refresh_token(refresh_token):
    """
    Verifica un refresh token y devuelve el usuario.
    
    Args:
        refresh_token (str): Refresh token JWT
    
    Returns:
        res.partner: Usuario autenticado
    
    Raises:
        Exception: Si el token es inválido o ha expirado
    """
    try:
        # Decodificar token
        payload = jwt.decode(
            refresh_token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        
        # Verificar que sea un refresh token
        if payload.get('type') != 'refresh':
            raise Exception('Tipo de token inválido')
        
        # Obtener user_id
        user_id = payload.get('user_id')
        
        if not user_id:
            raise Exception('Token inválido: falta user_id')
        
        # Buscar usuario
        partner = request.env['res.partner'].sudo().browse(user_id)
        
        if not partner.exists():
            raise Exception('Usuario no encontrado')
        
        # Verificar que el token coincida con el guardado en BD
        if partner.api_token != refresh_token:
            raise Exception('Refresh token inválido o revocado')
        
        # Verificar cuenta activa
        if not partner.cuenta_activa:
            raise Exception('Cuenta desactivada')
        
        return partner
        
    except jwt.ExpiredSignatureError:
        _logger.warning('Refresh token expirado')
        raise Exception('Refresh token expirado')
    
    except jwt.InvalidTokenError as e:
        _logger.warning(f'Refresh token inválido: {str(e)}')
        raise Exception('Refresh token inválido')
    
    except Exception as e:
        _logger.error(f'Error al verificar refresh token: {str(e)}')
        raise


def revoke_refresh_token(partner):
    """
    Revoca el refresh token de un usuario (logout).
    
    Args:
        partner (res.partner): Usuario
    """
    partner.sudo().write({'api_token': False})
    _logger.info(f'Refresh token revocado para usuario {partner.id}')
