# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError
import os
from ..utils.utils import compare_pot_files , get_pot_from_export
NEW_LANG_KEY = '__new__'

class Ir_moduleTranslate(models.Model):
    _name = 'ir.module.e_translate'
    _inherit = "ir.module.e_base"
    _description = 'irModuleTranslate'

    
    has_pot_translations = fields.Boolean("Pot File",compute="_compute_translations")
    po_translations = fields.Json("Languages",compute="_compute_translations")
    pot_keys = fields.Json("Pot Keys")
    
    status = fields.Selection([
        ('up_to_date',"Up todate")
        ('out_of_date',"Out to Date")
    ],required=True)
    
    last_check = fields.Datetime(default=fields.Datetime.now)
    
    @api.depends('module_name')
    def _compute_translations(self):
        for rec in self:
            rec.has_pot_translations = False
            po_translations = []
            if rec.module_exist:
                i18n_path = os.path.join(rec.local_path,'i18n')
                if os.path.exists(i18n_path):
                    for entry in os.scandir(i18n_path):
                        if entry.name == f'{rec.module_name}.pot':
                            rec.has_pot_translations = True
                        if entry.name.endswith('.po'):
                            lang_code = entry.name[:-3]
                            po_translations.append({
                                'name': lang_code,
                            })
            rec.po_translations = po_translations
              
    
    
    def action_recompute_pot(self):
        self.ensure_one()
        result = compare_pot_files(self.local_path,self.module_name,self._cr)
        if result:
            common_keys, missing_in_file, extra_in_file = result
            self.pot_keys = common_keys
            self.status = bool(missing_in_file and extra_in_file)
            self.last_check = fields.Datetime.now()
            
    @api.model
    def get_po_data(self,e_translate_id):
        pass
        