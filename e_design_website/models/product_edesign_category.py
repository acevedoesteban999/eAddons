from odoo import models , fields , api
class ProductEDesign(models.Model):
    _inherit = "product.edesign.category"
    
    is_published = fields.Boolean("Is Published",help="Is Published on Website",default=True)
    has_subcategories_designs = fields.Boolean(compute="_compute_has_subcategories_designs")
    
    @api.depends('subcategories_ids')
    def _compute_has_subcategories_designs(self):
        for rec in self:
            rec.has_subcategories_designs = (rec.is_published and rec.design_ids) or any(rec.subcategories_ids.mapped('has_subcategories_designs'))
            
    def get_subcategories_ids_recursive(self):
        ids = []
        for rec in self:
            ids.append(rec.id)
            ids.extend(rec.subcategories_ids.get_subcategories_ids_recursive())
        return ids