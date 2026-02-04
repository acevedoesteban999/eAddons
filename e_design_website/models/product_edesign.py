from odoo import models , fields

class ProductEDesign(models.Model):
    _inherit = "product.edesign"
    
    ewebsite_published = fields.Boolean("Is Published",help="Is Published on eWebsite",default=True)
    
    product_ids = fields.Many2many('product.template','rel_product_edesigns',compute="_compute_product_ids")
    
    
    def _compute_product_ids(self):
        for rec in self:
            rec.product_ids = self.env['product.template'].search([('design_ids','in',rec.id)])    