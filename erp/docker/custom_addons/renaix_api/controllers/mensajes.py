# -*- coding: utf-8 -*-
"""Controlador de Mensajes"""

import json
import logging
from odoo import http
from odoo.http import request
from ..models.utils import jwt_utils, validators, response_helpers, serializers

_logger = logging.getLogger(__name__)

class MensajesController(http.Controller):
    
    @http.route('/api/v1/mensajes/conversaciones', type='http', auth='public', methods=['GET'], csrf=False, cors='*')
    def listar_conversaciones(self, **params):
        try:
            partner = jwt_utils.verify_token(request)
            mensajes = request.env['renaix.mensaje'].sudo().search([
                '|', ('emisor_id', '=', partner.id), ('receptor_id', '=', partner.id)
            ], order='fecha DESC')
            
            conversaciones = {}
            for mensaje in mensajes:
                if mensaje.hilo_id not in conversaciones:
                    conversaciones[mensaje.hilo_id] = []
                conversaciones[mensaje.hilo_id].append(mensaje)
            
            conversaciones_data = [serializers.serialize_conversacion(msgs) for msgs in conversaciones.values()]
            
            return response_helpers.success_response(data=conversaciones_data, message='Conversaciones recuperadas')
        except Exception as e:
            _logger.error(f'Error: {str(e)}')
            return response_helpers.server_error_response(str(e))
    
    @http.route('/api/v1/mensajes', type='http', auth='public', methods=['POST'], csrf=False, cors='*')
    def enviar_mensaje(self, **params):
        try:
            partner = jwt_utils.verify_token(request)
            data = json.loads(request.httprequest.data.decode('utf-8'))
            
            is_valid, error_msg = validators.validate_mensaje_data(data)
            if not is_valid:
                return response_helpers.validation_error_response(error_msg)
            
            mensaje_vals = {
                'emisor_id': partner.id,
                'receptor_id': data['receptor_id'],
                'texto': data['texto'],
                'producto_id': data.get('producto_id'),
            }
            
            mensaje = request.env['renaix.mensaje'].sudo().create(mensaje_vals)
            
            return response_helpers.success_response(data=serializers.serialize_mensaje(mensaje), message='Mensaje enviado', status=201)
        except json.JSONDecodeError:
            return response_helpers.validation_error_response('JSON inválido')
        except Exception as e:
            _logger.error(f'Error: {str(e)}')
            return response_helpers.server_error_response(str(e))
    
    @http.route('/api/v1/mensajes/<int:mensaje_id>/marcar-leido', type='http', auth='public', methods=['PUT'], csrf=False, cors='*')
    def marcar_leido(self, mensaje_id, **params):
        try:
            partner = jwt_utils.verify_token(request)
            mensaje = request.env['renaix.mensaje'].sudo().browse(mensaje_id)
            
            if not mensaje.exists():
                return response_helpers.not_found_response('Mensaje no encontrado')
            
            if mensaje.receptor_id.id != partner.id:
                return response_helpers.forbidden_response('No tienes permiso')
            
            mensaje.sudo().write({'leido': True})
            
            return response_helpers.success_response(message='Mensaje marcado como leído')
        except Exception as e:
            _logger.error(f'Error: {str(e)}')
            return response_helpers.server_error_response(str(e))
