# -*- coding: utf-8 -*-
"""
Controlador de Autenticación
Endpoints: login, registro, refresh token, logout
"""

import json
import logging
from odoo import http
from odoo.http import request
from ..models.utils import jwt_utils, auth_helpers, validators, response_helpers, serializers

_logger = logging.getLogger(__name__)


class AuthController(http.Controller):
    
    @http.route('/api/v1/auth/register', type='http', auth='public', 
                methods=['POST'], csrf=False, cors='*')
    def register(self, **params):
        """
        Registro de nuevo usuario.
        
        Body JSON:
        {
            "name": "Juan Pérez",
            "email": "juan@example.com",
            "password": "password123",
            "phone": "612345678"  # opcional
        }
        
        Returns:
            JSON: {access_token, refresh_token, user}
        """
        try:
            # Obtener datos del body
            data = json.loads(request.httprequest.data.decode('utf-8'))
            
            # Validar campos requeridos
            required_fields = ['name', 'email', 'password']
            is_valid, error_msg = validators.validate_required_fields(data, required_fields)
            
            if not is_valid:
                return response_helpers.validation_error_response(error_msg)
            
            # Validar formato de email
            if not auth_helpers.validate_email_format(data['email']):
                return response_helpers.validation_error_response('Formato de email inválido')
            
            # Validar fortaleza de contraseña
            is_valid, error_msg = auth_helpers.validate_password_strength(data['password'])
            if not is_valid:
                return response_helpers.validation_error_response(error_msg)
            
            # Validar teléfono (si se proporciona)
            if data.get('phone') and not auth_helpers.validate_phone_number(data['phone']):
                return response_helpers.validation_error_response('Formato de teléfono inválido')
            
            # Verificar que no existe un usuario con ese email
            existing_user = request.env['res.partner'].sudo().search([
                ('email', '=', data['email']),
                ('es_usuario_app', '=', True)
            ], limit=1)
            
            if existing_user:
                return response_helpers.validation_error_response('Ya existe un usuario con este email')
            
            # Crear usuario
            partner_vals = {
                'name': data['name'],
                'email': data['email'],
                'phone': data.get('phone', ''),
                'es_usuario_app': True,
                'cuenta_activa': True,
            }
            
            partner = request.env['res.partner'].sudo().create(partner_vals)
            
            # Establecer contraseña (hasheada)
            partner.set_password(data['password'])
            
            # Generar tokens
            access_token = jwt_utils.generate_access_token(partner)
            refresh_token = jwt_utils.generate_refresh_token(partner)
            
            _logger.info(f'Nuevo usuario registrado: {partner.email} (ID: {partner.id})')
            
            return response_helpers.success_response(
                data={
                    'access_token': access_token,
                    'refresh_token': refresh_token,
                    'user': serializers.serialize_partner(partner, full=True)
                },
                message='Usuario registrado exitosamente',
                status=201
            )
            
        except json.JSONDecodeError:
            return response_helpers.validation_error_response('JSON inválido')
        
        except Exception as e:
            _logger.error(f'Error en registro: {str(e)}')
            return response_helpers.server_error_response(f'Error al registrar usuario: {str(e)}')
    
    
    @http.route('/api/v1/auth/login', type='http', auth='public', 
                methods=['POST'], csrf=False, cors='*')
    def login(self, **params):
        """
        Login de usuario.
        
        Body JSON:
        {
            "email": "juan@example.com",
            "password": "password123"
        }
        
        Returns:
            JSON: {access_token, refresh_token, user}
        """
        try:
            # Obtener datos del body
            data = json.loads(request.httprequest.data.decode('utf-8'))
            
            # Validar campos requeridos
            required_fields = ['email', 'password']
            is_valid, error_msg = validators.validate_required_fields(data, required_fields)
            
            if not is_valid:
                return response_helpers.validation_error_response(error_msg)
            
            # Autenticar usuario
            partner = request.env['res.partner'].sudo().authenticate_app_user(
                data['email'],
                data['password']
            )
            
            if not partner:
                return response_helpers.unauthorized_response('Credenciales inválidas')
            
            # Generar tokens
            access_token = jwt_utils.generate_access_token(partner)
            refresh_token = jwt_utils.generate_refresh_token(partner)
            
            _logger.info(f'Login exitoso: {partner.email} (ID: {partner.id})')
            
            return response_helpers.success_response(
                data={
                    'access_token': access_token,
                    'refresh_token': refresh_token,
                    'user': serializers.serialize_partner(partner, full=True)
                },
                message='Login exitoso'
            )
            
        except json.JSONDecodeError:
            return response_helpers.validation_error_response('JSON inválido')
        
        except Exception as e:
            _logger.error(f'Error en login: {str(e)}')
            return response_helpers.unauthorized_response('Credenciales inválidas')
    
    
    @http.route('/api/v1/auth/refresh', type='http', auth='public', 
                methods=['POST'], csrf=False, cors='*')
    def refresh_token(self, **params):
        """
        Renovar access token usando refresh token.
        
        Body JSON:
        {
            "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
        }
        
        Returns:
            JSON: {access_token}
        """
        try:
            # Obtener datos del body
            data = json.loads(request.httprequest.data.decode('utf-8'))
            
            if not data.get('refresh_token'):
                return response_helpers.validation_error_response('Refresh token requerido')
            
            # Verificar refresh token
            partner = jwt_utils.verify_refresh_token(data['refresh_token'])
            
            # Generar nuevo access token
            access_token = jwt_utils.generate_access_token(partner)
            
            _logger.info(f'Token renovado para usuario: {partner.email}')
            
            return response_helpers.success_response(
                data={
                    'access_token': access_token
                },
                message='Token renovado exitosamente'
            )
            
        except json.JSONDecodeError:
            return response_helpers.validation_error_response('JSON inválido')
        
        except Exception as e:
            _logger.warning(f'Error al renovar token: {str(e)}')
            return response_helpers.unauthorized_response(str(e))
    
    
    @http.route('/api/v1/auth/logout', type='http', auth='public', 
                methods=['POST'], csrf=False, cors='*')
    def logout(self, **params):
        """
        Logout de usuario (invalida refresh token).
        
        Headers:
            Authorization: Bearer <access_token>
        
        Returns:
            JSON: {message}
        """
        try:
            # Verificar token
            partner = jwt_utils.verify_token(request)
            
            # Revocar refresh token
            jwt_utils.revoke_refresh_token(partner)
            
            _logger.info(f'Logout exitoso: {partner.email}')
            
            return response_helpers.success_response(
                message='Logout exitoso'
            )
            
        except Exception as e:
            _logger.warning(f'Error en logout: {str(e)}')
            return response_helpers.unauthorized_response(str(e))
