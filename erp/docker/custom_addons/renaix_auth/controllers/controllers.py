# -*- coding: utf-8 -*-
# from odoo import http


# class RenaixAuth(http.Controller):
#     @http.route('/renaix_auth/renaix_auth', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/renaix_auth/renaix_auth/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('renaix_auth.listing', {
#             'root': '/renaix_auth/renaix_auth',
#             'objects': http.request.env['renaix_auth.renaix_auth'].search([]),
#         })

#     @http.route('/renaix_auth/renaix_auth/objects/<model("renaix_auth.renaix_auth"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('renaix_auth.object', {
#             'object': obj
#         })

