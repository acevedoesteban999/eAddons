# -*- coding: utf-8 -*-
from odoo import models,fields,_

class MrpProduction(models.Model):
    
    _inherit = 'mrp.production'
    
    pos_order_id = fields.Many2one('pos.order',"Origin POS",compute="_compute_pos_order_line")
    pos_order_line_id = fields.Many2one('pos.order.line',"Origin POS line")
    
    def _compute_pos_order_line(self):
        for rec in self:
            rec.pos_order_id = rec.pos_order_line_id.order_id
            
    def action_view_pos_order(self):
        self.ensure_one()
        return {
            'name': _("POS Order"),
            'res_model': 'pos.order',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_id': self.pos_order_id.id,
        }