# -*- coding: utf-8 -*-
"""Controlador de Denuncias"""

import json
import logging
from odoo import http
from odoo.http import request
from ..models.utils import jwt_utils, validators, response_helpers, serializers

_logger = logging.getLogger(__name__)

class DenunciasController(http.Controller):
    
    @http.route('/api/v1/denuncias', type='http', auth='public', methods=['POST'], csrf=False, cors='*')
    def crear_denuncia(self, **params):
        try:
            partner = jwt_utils.verify_token(request)
            data = json.loads(request.httprequest.data.decode('utf-8'))
            
            is_valid, error_msg = validators.validate_denuncia_data(data)
            if not is_valid:
                return response_helpers.validation_error_response(error_msg)
            
            denuncia_vals = {
                'usuario_reportante_id': partner.id,
                'tipo': data['tipo'],
                'motivo': data['motivo'],
                'categoria': data['categoria'],
                'producto_id': data.get('producto_id'),
                'comentario_id': data.get('comentario_id'),
                'usuario_reportado_id': data.get('usuario_reportado_id'),
            }
            
            denuncia = request.env['renaix.denuncia'].sudo().create(denuncia_vals)
            
            return response_helpers.success_response(data=serializers.serialize_denuncia(denuncia), message='Denuncia creada', status=201)
        except json.JSONDecodeError:
            return response_helpers.validation_error_response('JSON inválido')
        except Exception as e:
            _logger.error(f'Error: {str(e)}')
            return response_helpers.server_error_response(str(e))
    
    @http.route('/api/v1/denuncias/mis-denuncias', type='http', auth='public', methods=['GET'], csrf=False, cors='*')
    def listar_mis_denuncias(self, **params):
        try:
            partner = jwt_utils.verify_token(request)
            denuncias = request.env['renaix.denuncia'].sudo().search([('usuario_reportante_id', '=', partner.id)], order='fecha_denuncia DESC')
            
            denuncias_data = [serializers.serialize_denuncia(d) for d in denuncias]
            
            return response_helpers.success_response(data=denuncias_data, message='Denuncias recuperadas')
        except Exception as e:
            _logger.error(f'Error: {str(e)}')
            return response_helpers.server_error_response(str(e))
