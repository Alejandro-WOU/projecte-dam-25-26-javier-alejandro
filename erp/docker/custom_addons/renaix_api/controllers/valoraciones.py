# -*- coding: utf-8 -*-
"""
Controlador de Valoraciones
"""

import json
import logging
from odoo import http
from odoo.http import request
from ..models.utils import jwt_utils, validators, response_helpers, serializers

_logger = logging.getLogger(__name__)


class ValoracionesController(http.Controller):
    
    @http.route('/api/v1/compras/<int:compra_id>/valorar', type='http', auth='public', 
                methods=['POST'], csrf=False, cors='*')
    def valorar_transaccion(self, compra_id, **params):
        """Valorar una transacción."""
        try:
            partner = jwt_utils.verify_token(request)
            data = json.loads(request.httprequest.data.decode('utf-8'))
            
            is_valid, error_msg = validators.validate_valoracion_data(data)
            if not is_valid:
                return response_helpers.validation_error_response(error_msg)
            
            compra = request.env['renaix.compra'].sudo().browse(compra_id)
            
            if not compra.exists():
                return response_helpers.not_found_response('Compra no encontrada')
            
            if compra.estado != 'completada':
                return response_helpers.validation_error_response('Solo se pueden valorar compras completadas')
            
            # Determinar tipo de valoración
            if compra.comprador_id.id == partner.id:
                tipo = 'comprador_a_vendedor'
                valorado_id = compra.vendedor_id.id
                if compra.comprador_valoro:
                    return response_helpers.validation_error_response('Ya has valorado esta transacción')
            elif compra.vendedor_id.id == partner.id:
                tipo = 'vendedor_a_comprador'
                valorado_id = compra.comprador_id.id
                if compra.vendedor_valoro:
                    return response_helpers.validation_error_response('Ya has valorado esta transacción')
            else:
                return response_helpers.forbidden_response('No tienes permiso')
            
            valoracion_vals = {
                'compra_id': compra.id,
                'usuario_valorador_id': partner.id,
                'usuario_valorado_id': valorado_id,
                'puntuacion': data['puntuacion'],
                'comentario': data.get('comentario', ''),
                'tipo_valoracion': tipo,
            }
            
            valoracion = request.env['renaix.valoracion'].sudo().create(valoracion_vals)
            
            return response_helpers.success_response(
                data=serializers.serialize_valoracion(valoracion),
                message='Valoración creada',
                status=201
            )
            
        except json.JSONDecodeError:
            return response_helpers.validation_error_response('JSON inválido')
        except Exception as e:
            _logger.error(f'Error: {str(e)}')
            return response_helpers.server_error_response(str(e))
    
    
    @http.route('/api/v1/usuarios/<int:user_id>/valoraciones', type='http', auth='public', 
                methods=['GET'], csrf=False, cors='*')
    def listar_valoraciones(self, user_id, **params):
        """Listar valoraciones de un usuario."""
        try:
            valoraciones = request.env['renaix.valoracion'].sudo().search([
                ('usuario_valorado_id', '=', user_id)
            ], order='fecha DESC')
            
            valoraciones_data = [serializers.serialize_valoracion(v) for v in valoraciones]
            
            return response_helpers.success_response(
                data=valoraciones_data,
                message='Valoraciones recuperadas'
            )
            
        except Exception as e:
            _logger.error(f'Error: {str(e)}')
            return response_helpers.server_error_response(str(e))
