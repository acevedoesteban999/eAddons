from odoo import fields,models,api

class SublimationWizardAttchment(models.TransientModel):
    _name = 'sublimation.attachment.wizard'
    _description = 'Product Product Wizard'

    product_tmpl_sublimation_id = fields.Many2one('product.template', string='Product', required=True)
    attachment_ids = fields.Many2many('ir.attachment', string='Attachments')

    def action_create_attachemnt_sublimation(self):
        for att in self.attachment_ids:
            att.write({
                'res_model': 'product.template',
                'res_id': self.product_tmpl_sublimation_id.id,
            })

        

        return {
            'type': 'ir.actions.act_window_close',
        }