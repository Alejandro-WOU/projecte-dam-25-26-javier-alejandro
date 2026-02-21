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

    # ==================== SISTEMA DE OFERTAS ====================

    @http.route('/api/v1/mensajes/oferta', type='http', auth='public', methods=['POST'], csrf=False, cors='*')
    def enviar_oferta(self, **params):
        """
        Enviar una oferta de precio sobre un producto.

        Body JSON:
        {
            "producto_id": 123,
            "precio_ofertado": 45.50
        }

        Returns:
            JSON: {mensaje de oferta creado}
        """
        try:
            partner = jwt_utils.verify_token(request)
            data = json.loads(request.httprequest.data.decode('utf-8'))

            if not data.get('producto_id'):
                return response_helpers.validation_error_response('producto_id requerido')

            if not data.get('precio_ofertado'):
                return response_helpers.validation_error_response('precio_ofertado requerido')

            producto = request.env['renaix.producto'].sudo().browse(data['producto_id'])

            if not producto.exists():
                return response_helpers.not_found_response('Producto no encontrado')

            if producto.estado_venta != 'disponible':
                return response_helpers.validation_error_response('Producto no disponible')

            if producto.propietario_id.id == partner.id:
                return response_helpers.validation_error_response('No puedes hacer oferta sobre tu propio producto')

            precio_ofertado = float(data['precio_ofertado'])
            if precio_ofertado <= 0:
                return response_helpers.validation_error_response('El precio ofertado debe ser mayor que 0')

            mensaje_vals = {
                'emisor_id': partner.id,
                'receptor_id': producto.propietario_id.id,
                'producto_id': producto.id,
                'texto': f'Oferta de {precio_ofertado:.2f}€ por {producto.name}',
                'tipo_mensaje': 'offer',
                'precio_ofertado': precio_ofertado,
                'precio_original': producto.precio,
            }

            mensaje = request.env['renaix.mensaje'].sudo().create(mensaje_vals)

            _logger.info(f'Oferta enviada: {mensaje.id} - Producto: {producto.id} - Precio: {precio_ofertado}')

            return response_helpers.success_response(
                data=serializers.serialize_mensaje(mensaje),
                message='Oferta enviada correctamente',
                status=201
            )

        except json.JSONDecodeError:
            return response_helpers.validation_error_response('JSON inválido')
        except Exception as e:
            _logger.error(f'Error al enviar oferta: {str(e)}')
            return response_helpers.server_error_response(str(e))

    @http.route('/api/v1/mensajes/oferta/<int:mensaje_id>/aceptar', type='http', auth='public', methods=['POST'], csrf=False, cors='*')
    def aceptar_oferta(self, mensaje_id, **params):
        """
        Aceptar una oferta recibida. Crea una compra con el precio negociado.

        Returns:
            JSON: {mensaje de aceptación + compra creada}
        """
        try:
            partner = jwt_utils.verify_token(request)
            oferta = request.env['renaix.mensaje'].sudo().browse(mensaje_id)

            if not oferta.exists():
                return response_helpers.not_found_response('Oferta no encontrada')

            if oferta.tipo_mensaje not in ('offer', 'counter_offer'):
                return response_helpers.validation_error_response('Este mensaje no es una oferta')

            # Solo el receptor (vendedor) puede aceptar
            if oferta.receptor_id.id != partner.id:
                return response_helpers.forbidden_response('Solo el vendedor puede aceptar la oferta')

            producto = oferta.producto_id
            if not producto.exists() or producto.estado_venta != 'disponible':
                return response_helpers.validation_error_response('Producto ya no disponible')

            # Crear mensaje de aceptación
            mensaje_aceptacion = request.env['renaix.mensaje'].sudo().create({
                'emisor_id': partner.id,
                'receptor_id': oferta.emisor_id.id,
                'producto_id': producto.id,
                'texto': f'Oferta aceptada: {oferta.precio_ofertado:.2f}€ por {producto.name}',
                'tipo_mensaje': 'offer_accepted',
                'precio_ofertado': oferta.precio_ofertado,
                'precio_original': oferta.precio_original,
                'oferta_relacionada_id': oferta.id,
            })

            # Crear la compra con el precio negociado
            compra = request.env['renaix.compra'].sudo().create({
                'producto_id': producto.id,
                'comprador_id': oferta.emisor_id.id,
                'vendedor_id': partner.id,
                'precio_final': oferta.precio_ofertado,
                'notas': f'Compra con precio negociado. Oferta original: {oferta.precio_original:.2f}€',
            })

            _logger.info(f'Oferta aceptada: {oferta.id} - Compra creada: {compra.id}')

            return response_helpers.success_response(
                data={
                    'mensaje': serializers.serialize_mensaje(mensaje_aceptacion),
                    'compra': serializers.serialize_compra(compra)
                },
                message='Oferta aceptada y compra creada'
            )

        except Exception as e:
            _logger.error(f'Error al aceptar oferta: {str(e)}')
            return response_helpers.server_error_response(str(e))

    @http.route('/api/v1/mensajes/oferta/<int:mensaje_id>/rechazar', type='http', auth='public', methods=['POST'], csrf=False, cors='*')
    def rechazar_oferta(self, mensaje_id, **params):
        """
        Rechazar una oferta recibida.

        Returns:
            JSON: {mensaje de rechazo}
        """
        try:
            partner = jwt_utils.verify_token(request)
            oferta = request.env['renaix.mensaje'].sudo().browse(mensaje_id)

            if not oferta.exists():
                return response_helpers.not_found_response('Oferta no encontrada')

            if oferta.tipo_mensaje not in ('offer', 'counter_offer'):
                return response_helpers.validation_error_response('Este mensaje no es una oferta')

            # Solo el receptor puede rechazar
            if oferta.receptor_id.id != partner.id:
                return response_helpers.forbidden_response('Solo el receptor puede rechazar la oferta')

            producto = oferta.producto_id

            # Crear mensaje de rechazo
            mensaje_rechazo = request.env['renaix.mensaje'].sudo().create({
                'emisor_id': partner.id,
                'receptor_id': oferta.emisor_id.id,
                'producto_id': producto.id if producto else None,
                'texto': f'Oferta rechazada: {oferta.precio_ofertado:.2f}€',
                'tipo_mensaje': 'offer_rejected',
                'precio_ofertado': oferta.precio_ofertado,
                'precio_original': oferta.precio_original,
                'oferta_relacionada_id': oferta.id,
            })

            _logger.info(f'Oferta rechazada: {oferta.id}')

            return response_helpers.success_response(
                data=serializers.serialize_mensaje(mensaje_rechazo),
                message='Oferta rechazada'
            )

        except Exception as e:
            _logger.error(f'Error al rechazar oferta: {str(e)}')
            return response_helpers.server_error_response(str(e))

    @http.route('/api/v1/mensajes/contraoferta', type='http', auth='public', methods=['POST'], csrf=False, cors='*')
    def enviar_contraoferta(self, **params):
        """
        Enviar una contraoferta sobre una oferta existente.

        Body JSON:
        {
            "oferta_id": 123,
            "precio_contraoferta": 50.00
        }

        Returns:
            JSON: {mensaje de contraoferta}
        """
        try:
            partner = jwt_utils.verify_token(request)
            data = json.loads(request.httprequest.data.decode('utf-8'))

            if not data.get('oferta_id'):
                return response_helpers.validation_error_response('oferta_id requerido')

            if not data.get('precio_contraoferta'):
                return response_helpers.validation_error_response('precio_contraoferta requerido')

            oferta_original = request.env['renaix.mensaje'].sudo().browse(data['oferta_id'])

            if not oferta_original.exists():
                return response_helpers.not_found_response('Oferta original no encontrada')

            if oferta_original.tipo_mensaje not in ('offer', 'counter_offer'):
                return response_helpers.validation_error_response('El mensaje referenciado no es una oferta')

            # Solo el receptor de la oferta puede hacer contraoferta
            if oferta_original.receptor_id.id != partner.id:
                return response_helpers.forbidden_response('Solo el receptor puede hacer contraoferta')

            producto = oferta_original.producto_id
            if not producto.exists() or producto.estado_venta != 'disponible':
                return response_helpers.validation_error_response('Producto ya no disponible')

            precio_contraoferta = float(data['precio_contraoferta'])
            if precio_contraoferta <= 0:
                return response_helpers.validation_error_response('El precio debe ser mayor que 0')

            mensaje_vals = {
                'emisor_id': partner.id,
                'receptor_id': oferta_original.emisor_id.id,
                'producto_id': producto.id,
                'texto': f'Contraoferta: {precio_contraoferta:.2f}€ por {producto.name}',
                'tipo_mensaje': 'counter_offer',
                'precio_ofertado': precio_contraoferta,
                'precio_original': oferta_original.precio_original,
                'oferta_relacionada_id': oferta_original.id,
            }

            mensaje = request.env['renaix.mensaje'].sudo().create(mensaje_vals)

            _logger.info(f'Contraoferta enviada: {mensaje.id}')

            return response_helpers.success_response(
                data=serializers.serialize_mensaje(mensaje),
                message='Contraoferta enviada correctamente',
                status=201
            )

        except json.JSONDecodeError:
            return response_helpers.validation_error_response('JSON inválido')
        except Exception as e:
            _logger.error(f'Error al enviar contraoferta: {str(e)}')
            return response_helpers.server_error_response(str(e))
