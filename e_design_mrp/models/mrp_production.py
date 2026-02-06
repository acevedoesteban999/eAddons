# -*- coding: utf-8 -*-
from odoo import models,fields,api


class MrpProduction(models.Model):
    
    _inherit = 'mrp.production'
    
    design_id = fields.Many2one(
        'product.edesign',
        "Design",
        compute="_compute_design",
        readonly=False,
        store=True,
    )
    
    has_design_id = fields.Boolean(compute="_compute_has_design_id")
    product_tmpl_designs_ids = fields.Many2many(related='product_tmpl_id.design_ids')
            
        
    
    def _check_design_routes(self):
        if self.sale_line_id:
            self.design_id = self.sale_line_id.design_id.id
        else:
            order_line = self._get_move_dest_order_line(self.move_dest_ids)
            if order_line:
                self.design_id = order_line.design_id.id
            else:
                self.design_id = False
    
    @api.depends('product_tmpl_id')
    def _compute_has_design_id(self):
        for rec in self:
            rec.has_design_id = rec.product_tmpl_id.design_ok and rec.product_tmpl_id.design_ids

    @api.depends('product_tmpl_id')
    def _compute_design(self):
        for rec in self:
            rec._check_design_routes()