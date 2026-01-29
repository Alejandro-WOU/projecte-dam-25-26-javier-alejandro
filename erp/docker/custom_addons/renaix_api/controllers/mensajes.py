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
    
    @http.route('/api/v1/mensajes/conversacion/<int:user_id>', type='http', auth='public', methods=['GET'], csrf=False, cors='*')
    def get_conversacion(self, user_id, **params):
        """
        Obtener conversacion con un usuario especifico.

        Query params:
            producto_id: Filtrar por producto (opcional)

        Returns:
            JSON: {mensajes}
        """
        try:
            partner = jwt_utils.verify_token(request)

            # Verificar que el otro usuario existe
            otro_usuario = request.env['res.partner'].sudo().browse(user_id)
            if not otro_usuario.exists() or not otro_usuario.es_usuario_app:
                return response_helpers.not_found_response('Usuario no encontrado')

            # No puede conversar consigo mismo
            if otro_usuario.id == partner.id:
                return response_helpers.validation_error_response('No puedes ver conversacion contigo mismo')

            # Usar el metodo del modelo
            producto_id = int(params.get('producto_id', 0)) if params.get('producto_id') else None
            mensajes = request.env['renaix.mensaje'].sudo().get_conversacion(
                partner.id, user_id, producto_id=producto_id
            )

            mensajes_data = [serializers.serialize_mensaje(m) for m in mensajes]

            return response_helpers.success_response(
                data=mensajes_data,
                message='Conversacion recuperada'
            )
        except Exception as e:
            _logger.error(f'Error al obtener conversacion: {str(e)}')
            return response_helpers.server_error_response(str(e))

    @http.route('/api/v1/mensajes/no-leidos', type='http', auth='public', methods=['GET'], csrf=False, cors='*')
    def get_no_leidos(self, **params):
        """
        Obtener mensajes no leidos del usuario autenticado.

        Returns:
            JSON: {mensajes, total}
        """
        try:
            partner = jwt_utils.verify_token(request)

            # Usar el metodo del modelo
            mensajes = request.env['renaix.mensaje'].sudo().get_mensajes_no_leidos(partner.id)

            mensajes_data = [serializers.serialize_mensaje(m) for m in mensajes]

            return response_helpers.success_response(
                data={
                    'total': len(mensajes),
                    'mensajes': mensajes_data
                },
                message='Mensajes no leidos recuperados'
            )
        except Exception as e:
            _logger.error(f'Error al obtener mensajes no leidos: {str(e)}')
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

            mensaje.sudo().action_marcar_leido()

            return response_helpers.success_response(message='Mensaje marcado como leído')
        except Exception as e:
            _logger.error(f'Error: {str(e)}')
            return response_helpers.server_error_response(str(e))
