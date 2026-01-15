# -*- coding: utf-8 -*-

from odoo import models, fields


class ResCompany(models.Model):
    """
    Modelo: res.company extendido
    Descripción: Añade campos dummy para evitar errores en vistas heredadas de res.partner
    """
    _inherit = 'res.company'
    
    # ========================================
    # CAMPOS DUMMY (para compatibilidad de vistas)
    # ========================================
    # Estos campos existen solo para que las vistas heredadas de res.partner
    # no generen errores cuando se cargan en el contexto de res.company
    
    partner_gid = fields.Char(
        string='Global ID',
        compute='_compute_partner_gid',
        store=False,
        help='Campo dummy - no se usa en compañías'
    )
    
    es_usuario_app = fields.Boolean(
        string='Es Usuario App',
        compute='_compute_es_usuario_app',
        store=False,
        help='Campo dummy - siempre False para compañías'
    )
    
    additional_info = fields.Text(
        string='Información Adicional',
        compute='_compute_additional_info',
        store=False,
        help='Campo dummy - no se usa en compañías'
    )
    
    fecha_registro_app = fields.Datetime(
        string='Fecha Registro',
        compute='_compute_fecha_registro_app',
        store=False
    )
    
    cuenta_activa = fields.Boolean(
        string='Cuenta Activa',
        compute='_compute_cuenta_activa',
        store=False
    )
    
    fecha_ultima_actividad = fields.Datetime(
        string='Última Actividad',
        compute='_compute_fecha_ultima_actividad',
        store=False
    )
    
    valoracion_promedio = fields.Float(
        string='Valoración',
        compute='_compute_valoracion_promedio',
        store=False
    )
    
    total_comentarios = fields.Integer(
        string='Comentarios',
        compute='_compute_total_comentarios',
        store=False
    )
    
    total_denuncias_realizadas = fields.Integer(
        string='Denuncias',
        compute='_compute_total_denuncias_realizadas',
        store=False
    )
    
    productos_en_venta = fields.Integer(
        string='En Venta',
        compute='_compute_productos_en_venta',
        store=False
    )
    
    productos_comprados = fields.Integer(
        string='Comprados',
        compute='_compute_productos_comprados',
        store=False
    )
    
    productos_vendidos = fields.Integer(
        string='Vendidos',
        compute='_compute_productos_vendidos',
        store=False
    )
    
    api_token = fields.Char(
        string='API Token',
        compute='_compute_api_token',
        store=False
    )
    
    # Campo IAP (si el módulo partner_autocomplete está instalado)
    iap_enrich_auto_done = fields.Boolean(
        string='IAP Enrich Auto Done',
        compute='_compute_iap_enrich_auto_done',
        store=False,
        help='Campo dummy para compatibilidad con partner_autocomplete'
    )
    
    # ========================================
    # MÉTODOS COMPUTE (todos retornan valores vacíos/False)
    # ========================================
    
    def _compute_partner_gid(self):
        for company in self:
            company.partner_gid = False
    
    def _compute_es_usuario_app(self):
        for company in self:
            company.es_usuario_app = False
    
    def _compute_additional_info(self):
        for company in self:
            company.additional_info = False
    
    def _compute_fecha_registro_app(self):
        for company in self:
            company.fecha_registro_app = False
    
    def _compute_cuenta_activa(self):
        for company in self:
            company.cuenta_activa = False
    
    def _compute_fecha_ultima_actividad(self):
        for company in self:
            company.fecha_ultima_actividad = False
    
    def _compute_valoracion_promedio(self):
        for company in self:
            company.valoracion_promedio = 0.0
    
    def _compute_total_comentarios(self):
        for company in self:
            company.total_comentarios = 0
    
    def _compute_total_denuncias_realizadas(self):
        for company in self:
            company.total_denuncias_realizadas = 0
    
    def _compute_productos_en_venta(self):
        for company in self:
            company.productos_en_venta = 0
    
    def _compute_productos_comprados(self):
        for company in self:
            company.productos_comprados = 0
    
    def _compute_productos_vendidos(self):
        for company in self:
            company.productos_vendidos = 0
    
    def _compute_api_token(self):
        for company in self:
            company.api_token = False
    
    def _compute_iap_enrich_auto_done(self):
        for company in self:
            company.iap_enrich_auto_done = False
