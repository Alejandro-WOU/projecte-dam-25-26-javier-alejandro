# -*- coding: utf-8 -*-
"""Controlador de Etiquetas"""

import json
import logging
from odoo import http
from odoo.http import request
from ..models.utils import jwt_utils, response_helpers, serializers

_logger = logging.getLogger(__name__)

class EtiquetasController(http.Controller):

    @http.route('/api/v1/etiquetas', type='http', auth='none', methods=['GET'], csrf=False, cors='*')
    def listar_etiquetas(self, **params):
        try:
            etiquetas = request.env['renaix.etiqueta'].sudo().search([], order='producto_count DESC', limit=50)
            etiquetas_data = [serializers.serialize_etiqueta(e) for e in etiquetas]

            return response_helpers.success_response(data=etiquetas_data, message='Etiquetas populares recuperadas')
        except Exception as e:
            _logger.error(f'Error: {str(e)}')
            return response_helpers.server_error_response(str(e))

    @http.route('/api/v1/etiquetas', type='http', auth='public', methods=['POST'], csrf=False, cors='*')
    def crear_etiqueta(self, **params):
        """
        Crear una nueva etiqueta.

        Body JSON:
        {
            "nombre": "gaming"
        }

        Returns:
            JSON: {etiqueta} - Si ya existe, devuelve la existente
        """
        try:
            jwt_utils.verify_token(request)
            data = json.loads(request.httprequest.data.decode('utf-8'))

            if not data.get('nombre'):
                return response_helpers.validation_error_response('Campo "nombre" requerido')

            nombre = data['nombre'].strip()

            if len(nombre) < 2:
                return response_helpers.validation_error_response('El nombre debe tener al menos 2 caracteres')

            if len(nombre) > 30:
                return response_helpers.validation_error_response('El nombre no puede superar 30 caracteres')

            Etiqueta = request.env['renaix.etiqueta'].sudo()

            # Buscar si ya existe (case-insensitive)
            existing = Etiqueta.search([('name', '=ilike', nombre.lower())], limit=1)
            if existing:
                return response_helpers.success_response(
                    data=serializers.serialize_etiqueta(existing),
                    message='Etiqueta ya existente'
                )

            # Crear nueva etiqueta (el modelo normaliza el nombre)
            etiqueta = Etiqueta.create({'name': nombre})

            _logger.info(f'Etiqueta creada: {etiqueta.name} (ID: {etiqueta.id})')

            return response_helpers.success_response(
                data=serializers.serialize_etiqueta(etiqueta),
                message='Etiqueta creada exitosamente',
                status=201
            )

        except json.JSONDecodeError:
            return response_helpers.validation_error_response('JSON inválido')
        except Exception as e:
            _logger.error(f'Error al crear etiqueta: {str(e)}')
            return response_helpers.server_error_response(str(e))

    @http.route('/api/v1/etiquetas/buscar', type='http', auth='none', methods=['GET'], csrf=False, cors='*')
    def buscar_etiquetas(self, **params):
        try:
            query = params.get('q', '')
            if not query or len(query) < 2:
                return response_helpers.validation_error_response('La búsqueda debe tener al menos 2 caracteres')

            etiquetas = request.env['renaix.etiqueta'].sudo().search([('name', 'ilike', query)], limit=20)
            etiquetas_data = [serializers.serialize_etiqueta(e) for e in etiquetas]

            return response_helpers.success_response(data=etiquetas_data, message=f'Se encontraron {len(etiquetas)} etiquetas')
        except Exception as e:
            _logger.error(f'Error: {str(e)}')
            return response_helpers.server_error_response(str(e))
