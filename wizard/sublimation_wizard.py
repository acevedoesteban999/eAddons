from odoo import fields,models,api

class SublimationWizard(models.TransientModel):
    _name = 'sublimation.wizard'
    _description = 'Product Product Wizard'

    name = fields.Char(string='Name', required=True)
    product_tmpl_sublimation_id = fields.Many2one('product.template', string='Product', required=True, domain=[('sublimation_ok','=',True)])
    image_1920 = fields.Image("Image", max_width=1920, max_height=1920)
    price_extra = fields.Float(string='Extra Price', default=0.0)
    attachment_ids = fields.Many2many('ir.attachment', string='Attachments')

    def action_create_sublimation(self):
        new_product = self.env['product.template'].create({
            'name': self.product_tmpl_sublimation_id.name + " " + self.name,
            'sublimation_ok':True,
            'product_tmpl_sublimation_id': self.product_tmpl_sublimation_id.id,
            'default_code': f'SUB-{self.id}',
            'list_price': self.product_tmpl_sublimation_id.list_price + self.price_extra,
            'sublimation_price_extra':self.price_extra,
            'image_1920': self.image_1920,
        })

        for att in self.attachment_ids:
            att.write({
                'res_model': 'product.template',
                'res_id': new_product.id,
            })


        return {
            'type': 'ir.actions.act_window_close',
            'infos': {
                'new_product_id': new_product.id,
            },
        }