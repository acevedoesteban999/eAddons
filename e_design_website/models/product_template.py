from odoo import models , fields , api
class ProductTemplate(models.Model):
    _inherit = "product.template"
    
    ewebsite_published = fields.Boolean("Is Published",help="Is Published on eWebsite",default=False)
    