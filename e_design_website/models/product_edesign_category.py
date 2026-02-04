from odoo import models , fields , api
class ProductEDesign(models.Model):
    _inherit = "product.edesign.category"
    
    ewebsite_published = fields.Boolean("Is Published",help="Is Published on eWebsite",default=True)
    