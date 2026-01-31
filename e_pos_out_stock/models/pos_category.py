# -*- coding: utf-8 -*-
from odoo import models, fields



class PosCategory(models.Model):
    _inherit = 'pos.category'

    show_pos_outstock = fields.Boolean("Show products in POS with Out of Stock")
    
    def get_show_pos_outstock_recursive(self):
        if self:
            return any(self.mapped('show_pos_outstock')) or (self.parent_id.get_show_pos_outstock_recursive() if self.parent_id else False)
        return False