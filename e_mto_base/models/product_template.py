# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    mto_ok = fields.Boolean(compute="_compute_mto_ok")
    
    @api.depends('route_ids')
    def _compute_mto_ok(self):
        for rec in self:
            try:
                mto_route = self.env['stock.warehouse']._find_or_create_global_route('stock.route_warehouse0_mto', _('Replenish on Order (MTO)'), create=False)
            except:
                mto_route = False

            rec.mto_ok = mto_route in rec.route_ids