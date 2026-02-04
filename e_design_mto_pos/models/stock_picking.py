from odoo import models , api
class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    @api.model
    def read_picking_lines(self, picking_id):
        lines = super().read_picking_lines(picking_id)
        for line in lines:
            order_line = self.env['pos.order.line'].browse(line.get('id'))
            if order_line.design_id:
                line.update({
                    'design_id':{
                        'default_code': order_line.design_id.default_code or '',
                    }
                })
                
        return lines
        
    