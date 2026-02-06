# -*- coding: utf-8 -*-
from odoo import models,fields,_

class MrpProduction(models.Model):
    
    _inherit = 'mrp.production'
       
    def action_view_pos_order(self):
        self.ensure_one()
        return {
            'name': _("POS Order"),
            'res_model': 'pos.order',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_id': self.pos_order_id.id,
        }