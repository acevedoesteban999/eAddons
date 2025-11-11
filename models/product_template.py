from odoo import fields,models,api

class ProductProduct(models.Model):
    _inherit = 'product.template'

    sublimation_ok = fields.Boolean(string='Sublimation')
    product_sublimation_count = fields.Integer(
        string='Sublimations (Total)',
        compute='_compute_total_attribute_line',
    )

    product_tmpl_sublimation_id = fields.Many2one('product.template', 'Product Template Sublimation')
    product_childs_sublimation_ids = fields.One2many('product.template', 'product_tmpl_sublimation_id', string='Product Products Sublimation', readonly=True)
    
    attachment_ids = fields.Many2many(
        'ir.attachment',
        string="Attachments",
        compute='_compute_attachment_ids',
        store=False
    )
    sublimation_price_extra = fields.Float(string='Sublimation Extra Price', default=0.0)
    
    list_price = fields.Float(compute="_compute_list_price",store=True)
    
    @api.depends('product_tmpl_sublimation_id.list_price','sublimation_price_extra')
    def _compute_list_price(slef):
        for rec in slef:
            if rec.sublimation_ok and rec.product_tmpl_sublimation_id:
                rec.list_price = rec.product_tmpl_sublimation_id.list_price + rec.sublimation_price_extra
            else:
                rec.list_price = rec.list_price or 1
    
    def _compute_attachment_ids(self):
        for product in self:
            product.attachment_ids = self.env['ir.attachment'].search([
                ('res_model', '=', 'product.template'),
                ('res_id', '=', product.id)
            ])

    @api.depends('product_sublimation_count')
    def _compute_total_attribute_line(self):
        self._create_variant_ids()
        for rec in self:
            rec.product_sublimation_count = len(rec.product_childs_sublimation_ids)
    
    def _compute_display_name(self):
        for rec in self:
            if rec.sublimation_ok and rec.product_tmpl_sublimation_id:
                rec.display_name = rec.product_tmpl_sublimation_id.name + " " + rec.name
            else:
                super(ProductProduct,rec)._compute_display_name()

    
    def action_open_product_template(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'product.template',
            'view_mode': 'form',
            'target': 'current',
            'res_id': self.id,
            'view_id': self.env.ref('product.product_template_only_form_view').id,
        }
    def action_open_product_tmpl_sublimation_id(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'product.template',
            'view_mode': 'form',
            'target': 'new',
            'res_id': self.product_tmpl_sublimation_id.id,
            'view_id': self.env.ref('product.product_template_only_form_view').id,
        }

    def action_open_product_childs_sublimation(self):
        return {
            'name': f'{self.name}',
            'type': 'ir.actions.act_window',
            'res_model': 'product.template',
            'view_mode': 'kanban,list,form',
            'target': 'current',
            'domain': [('id','in',self.product_childs_sublimation_ids.ids)],
            'context': {'default_product_tmpl_sublimation_id': self.id},
            'views': [
                (self.env.ref('e_sublimation.product_childs_view_kanban_sublimation').id,'kanban'),
                (self.env.ref('e_sublimation.product_childs_view_list_sublimation').id,'list'),
                (self.env.ref('product.product_template_only_form_view').id,'form'),  
            ],
        }

    def action_open_sublimation_attachment_wizard(self):
        return {
            'name': 'Create Sublimation Attachments',
            'type': 'ir.actions.act_window',
            'res_model': 'sublimation.attachment.wizard',
            'view_mode': 'form',
            'target': 'new',
            'views': [(self.env.ref('e_sublimation.sublimation_attachment_wizard_view_form').id,'form')],
            'context': {'default_product_tmpl_sublimation_id': self.id}
        }
    
    @api.model
    def action_open_sublimation_wizard(self,id_model = False):
        model = self or self.env['product.template'].browse(id_model)
        return {
            'name': 'Create Sublimación',
            'type': 'ir.actions.act_window',
            'res_model': 'sublimation.wizard',
            'view_mode': 'form',
            'target': 'new',
            'views': [(self.env.ref('e_sublimation.sublimation_wizard_view_form').id,'form')],
            'context': {'default_product_tmpl_sublimation_id': model.id}
        }

    def unlink(self):
        if self.product_childs_sublimation_ids:
            self.product_childs_sublimation_ids.unlink()
        return super().unlink()

