from odoo import models,fields

class EUpdateBackup(models.TransientModel):
    _name = 'ir.module.e_update.backup'
    _description = 'model.technical.name'

    version = fields.Char("Name")
    e_update_module_id = fields.Many2one('ir.module.e_update',"eUpdate Module")
    path = fields.Char()
    
    def action_backup(self):
        pass