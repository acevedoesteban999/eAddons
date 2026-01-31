# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ProductProduct(models.Model):
    _inherit = 'product.product'

    has_create_mto_pos = fields.Boolean(
        compute="_compute_has_create_mto_pos")
    
    def _compute_has_create_mto_pos(self):
        for rec in self:
            rec.has_create_mto_pos = rec.product_tmpl_id.can_create_mto_pos