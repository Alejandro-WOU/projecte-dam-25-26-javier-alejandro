# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Valoracion(models.Model):
    """
    Modelo: Valoración
    Descripción: Valoraciones entre usuarios (1-5 estrellas) tras una compra
    """
    _name = 'renaix.valoracion'
    _description = 'Valoración de Usuario'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'fecha desc, id desc'
    
    # Relación con la compra (obligatoria)
    compra_id = fields.Many2one(
        'renaix.compra',
        string='Compra',
        required=True,
        ondelete='cascade',
        tracking=True,
        help='Compra asociada a esta valoración'
    )
    
    # Tipo de valoración
    tipo_valoracion = fields.Selection([
        ('comprador_a_vendedor', 'Comprador valora a Vendedor'),
        ('vendedor_a_comprador', 'Vendedor valora a Comprador'),
    ], string='Tipo',
       required=True,
       tracking=True,
       help='Indica quién valora a quién'
    )
    
    # Usuario que hace la valoración
    usuario_valorador_id = fields.Many2one(
        'res.partner',
        string='Usuario Valorador',
        required=True,
        ondelete='restrict',
        domain=[('es_usuario_app', '=', True)],
        tracking=True,
        help='Usuario que hace la valoración'
    )
    
    # Usuario que recibe la valoración
    usuario_valorado_id = fields.Many2one(
        'res.partner',
        string='Usuario Valorado',
        required=True,
        ondelete='restrict',
        domain=[('es_usuario_app', '=', True)],
        tracking=True,
        help='Usuario que recibe la valoración'
    )
    
    # Puntuación (1-5 estrellas)
    puntuacion = fields.Integer(
        string='Puntuación',
        required=True,
        tracking=True,
        help='Puntuación de 1 a 5 estrellas'
    )
    
    # Comentario opcional
    comentario = fields.Text(
        string='Comentario',
        help='Comentario opcional sobre la transacción'
    )
    
    # Fecha de la valoración
    fecha = fields.Datetime(
        string='Fecha',
        default=fields.Datetime.now,
        required=True,
        tracking=True
    )
    
    # Campos relacionados (para facilitar búsquedas)
    comprador_id = fields.Many2one(
        related='compra_id.comprador_id',
        string='Comprador',
        store=True,
        readonly=True
    )
    
    vendedor_id = fields.Many2one(
        related='compra_id.vendedor_id',
        string='Vendedor',
        store=True,
        readonly=True
    )
    
    producto_id = fields.Many2one(
        related='compra_id.producto_id',
        string='Producto',
        store=True,
        readonly=True
    )
    
    # Constraints SQL
    _sql_constraints = [
        ('puntuacion_rango', 
         'CHECK(puntuacion >= 1 AND puntuacion <= 5)', 
         'La puntuación debe estar entre 1 y 5.'),
        ('valoracion_unica',
         'UNIQUE(compra_id, tipo_valoracion)',
         'Ya existe una valoración de este tipo para esta compra.'),
    ]
    
    @api.constrains('puntuacion')
    def _check_puntuacion(self):
        """Valida que la puntuación esté entre 1 y 5"""
        for valoracion in self:
            if valoracion.puntuacion < 1 or valoracion.puntuacion > 5:
                raise ValidationError('La puntuación debe estar entre 1 y 5 estrellas.')
    
    @api.constrains('usuario_valorador_id', 'usuario_valorado_id')
    def _check_no_autovaloracion(self):
        """Valida que no se pueda valorar a uno mismo"""
        for valoracion in self:
            if valoracion.usuario_valorador_id == valoracion.usuario_valorado_id:
                raise ValidationError('No puedes valorarte a ti mismo.')
    
    @api.constrains('compra_id', 'tipo_valoracion', 'usuario_valorador_id')
    def _check_valoracion_coherente(self):
        """Valida que la valoración sea coherente con la compra"""
        for valoracion in self:
            compra = valoracion.compra_id
            
            if valoracion.tipo_valoracion == 'comprador_a_vendedor':
                # El valorador debe ser el comprador
                if valoracion.usuario_valorador_id != compra.comprador_id:
                    raise ValidationError(
                        'Solo el comprador puede valorar al vendedor.'
                    )
                # El valorado debe ser el vendedor
                if valoracion.usuario_valorado_id != compra.vendedor_id:
                    raise ValidationError(
                        'El usuario valorado debe ser el vendedor de la compra.'
                    )
            
            elif valoracion.tipo_valoracion == 'vendedor_a_comprador':
                # El valorador debe ser el vendedor
                if valoracion.usuario_valorador_id != compra.vendedor_id:
                    raise ValidationError(
                        'Solo el vendedor puede valorar al comprador.'
                    )
                # El valorado debe ser el comprador
                if valoracion.usuario_valorado_id != compra.comprador_id:
                    raise ValidationError(
                        'El usuario valorado debe ser el comprador de la compra.'
                    )
    
    @api.constrains('compra_id')
    def _check_compra_completada(self):
        """Valida que solo se pueda valorar compras completadas"""
        for valoracion in self:
            if valoracion.compra_id.estado != 'completada':
                raise ValidationError(
                    'Solo puedes valorar una compra que haya sido completada.'
                )
    
    @api.model
    def create(self, vals):
        """Al crear: notificar al usuario valorado"""
        valoracion = super(Valoracion, self).create(vals)
        
        # Notificar al usuario valorado
        estrellas = '⭐' * valoracion.puntuacion
        valoracion.message_post(
            body=f"""
                <h3>✨ Nueva valoración recibida</h3>
                <p><b>De:</b> {valoracion.usuario_valorador_id.name}</p>
                <p><b>Puntuación:</b> {estrellas} ({valoracion.puntuacion}/5)</p>
                <p><b>Comentario:</b> {valoracion.comentario or 'Sin comentario'}</p>
            """,
            subject='Nueva Valoración',
            partner_ids=[valoracion.usuario_valorado_id.id]
        )
        
        # Notificar en la compra
        valoracion.compra_id.message_post(
            body=f'{valoracion.usuario_valorador_id.name} ha valorado con {estrellas}',
            subject='Nueva Valoración'
        )
        
        return valoracion
    
    def name_get(self):
        """Personaliza cómo se muestra en selects"""
        result = []
        for valoracion in self:
            estrellas = '⭐' * valoracion.puntuacion
            name = f"{valoracion.usuario_valorador_id.name} → {valoracion.usuario_valorado_id.name} ({estrellas})"
            result.append((valoracion.id, name))
        return result
