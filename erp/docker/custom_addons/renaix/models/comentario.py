# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Comentario(models.Model):
    """
    Modelo: Comentario
    Descripción: Comentarios que los usuarios hacen en productos
    """
    _name = 'renaix.comentario'
    _description = 'Comentario de Producto'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'fecha desc, id desc'
    
    # Relación con producto
    producto_id = fields.Many2one(
        'renaix.producto',
        string='Producto',
        required=True,
        ondelete='cascade',
        tracking=True,
        help='Producto comentado'
    )
    
    # Usuario que hace el comentario
    usuario_id = fields.Many2one(
        'res.partner',
        string='Usuario',
        required=True,
        ondelete='restrict',
        domain=[('es_usuario_app', '=', True)],
        tracking=True,
        help='Usuario que hace el comentario'
    )
    
    # Texto del comentario
    texto = fields.Text(
        string='Comentario',
        required=True,
        help='Contenido del comentario'
    )
    
    # Fecha del comentario
    fecha = fields.Datetime(
        string='Fecha',
        default=fields.Datetime.now,
        required=True,
        readonly=True
    )
    
    # Control de estado
    active = fields.Boolean(
        string='Activo',
        default=True,
        tracking=True,
        help='Si está inactivo, el comentario fue eliminado por moderación'
    )
    
    # Campos relacionados (para facilitar búsquedas)
    producto_nombre = fields.Char(
        related='producto_id.name',
        string='Producto',
        store=True,
        readonly=True
    )
    
    usuario_nombre = fields.Char(
        related='usuario_id.name',
        string='Usuario',
        store=True,
        readonly=True
    )
    
    propietario_producto_id = fields.Many2one(
        related='producto_id.propietario_id',
        string='Propietario del Producto',
        store=True,
        readonly=True
    )
    
    @api.constrains('texto')
    def _check_texto(self):
        """Validaciones del texto del comentario"""
        for comentario in self:
            if not comentario.texto or not comentario.texto.strip():
                raise ValidationError('El comentario no puede estar vacío.')
            
            if len(comentario.texto) < 3:
                raise ValidationError('El comentario debe tener al menos 3 caracteres.')
            
            if len(comentario.texto) > 1000:
                raise ValidationError('El comentario no puede superar 1000 caracteres.')
    
    @api.constrains('usuario_id', 'producto_id')
    def _check_no_spam(self):
        """Evita que un usuario haga múltiples comentarios muy seguidos"""
        for comentario in self:
            # Buscar comentarios recientes del mismo usuario en el mismo producto
            recent_comments = self.search([
                ('usuario_id', '=', comentario.usuario_id.id),
                ('producto_id', '=', comentario.producto_id.id),
                ('id', '!=', comentario.id),
                ('fecha', '>=', fields.Datetime.now().replace(hour=0, minute=0, second=0))
            ])
            
            if len(recent_comments) >= 5:
                raise ValidationError(
                    'Has alcanzado el límite de comentarios por día en este producto.'
                )
    
    @api.model
    def create(self, vals):
        """Al crear: notificar al propietario del producto"""
        comentario = super(Comentario, self).create(vals)
        
        # Notificar al propietario del producto
        propietario = comentario.producto_id.propietario_id
        
        if propietario and propietario != comentario.usuario_id:
            comentario.producto_id.message_post(
                body=f"""
                    <h3>💬 Nuevo comentario en tu producto</h3>
                    <p><b>Usuario:</b> {comentario.usuario_id.name}</p>
                    <p><b>Comentario:</b> {comentario.texto}</p>
                """,
                subject=f'Nuevo comentario en: {comentario.producto_id.name}',
                partner_ids=[propietario.id]
            )
        
        return comentario
    
    def write(self, vals):
        """Al desactivar: notificar al usuario"""
        if 'active' in vals and not vals['active']:
            for comentario in self:
                comentario.message_post(
                    body='Este comentario ha sido eliminado por un moderador',
                    subject='Comentario Eliminado',
                    partner_ids=[comentario.usuario_id.id]
                )
        
        return super(Comentario, self).write(vals)
    
    def action_eliminar(self):
        """Elimina (desactiva) el comentario"""
        for comentario in self:
            comentario.active = False
    
    def action_restaurar(self):
        """Restaura un comentario eliminado"""
        for comentario in self:
            comentario.active = True
    
    def name_get(self):
        """Personaliza cómo se muestra en selects"""
        result = []
        for comentario in self:
            # Truncar texto si es muy largo
            texto_preview = comentario.texto[:50] + '...' if len(comentario.texto) > 50 else comentario.texto
            name = f"{comentario.usuario_id.name}: {texto_preview}"
            result.append((comentario.id, name))
        return result
