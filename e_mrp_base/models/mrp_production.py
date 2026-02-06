# -*- coding: utf-8 -*-
from odoo import models,fields,_

class MrpProduction(models.Model):
    
    _inherit = 'mrp.production'
    
        
    def _get_move_dest_order_line(self,move_finished_ids):
        for move in move_finished_ids:
            while move:
                if move.sale_line_id:
                    return move.sale_line_id
                move = move.move_dest_ids[:1]
        return False