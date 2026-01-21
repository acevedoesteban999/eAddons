from odoo import models, fields, api, _

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    _description = 'SaleOrderLine'

    design_id = fields.Many2one('product.edesign',"Design")
    is_designable_product = fields.Boolean(related='product_template_id.design_ok')
    
    
    def write(self,vals):
        return super().write(vals)