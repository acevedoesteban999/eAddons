# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError
import io
import os
import ast
import base64
from odoo.tools.translate import trans_export, trans_export_records
import json
NEW_LANG_KEY = '__new__'

class Ir_moduleTranslate(models.Model):
    _name = 'ir.module.e_translate'
    _inherit = "ir.module.e_base"
    _description = 'irModuleTranslate'

    
    has_translations = fields.Boolean(compute="_compute_translations")
    translations = fields.Json(compute="_compute_translations")
    
    @api.depends('module_name')
    def _compute_translations(self):
        for rec in self:
            rec.has_translations = False
            translations = []
            if rec.module_exist:
                i18n_path = os.path.join(rec.local_path,'i18n')
                if os.path.exists(i18n_path):
                    for entry in os.scandir(i18n_path):
                        if entry.name == f'{rec.module_name}.pot':
                            rec.has_translations = True
                        if entry.name.endswith('.po'):
                            lang_code = entry.name[:-3]
                            translations.append({
                                'file': entry.name,
                                'lang': lang_code,
                                'path': entry.path,
                            })
                            
            rec.translations =  translations
                
    
    def validate_pot(slef):
        pass
    
    def act_getfile(self):
        this = self[0]
        lang = this.lang if this.lang != NEW_LANG_KEY else False

        with io.BytesIO() as buf:
            if this.export_type == 'model':
                ids = self.env[this.model_name].search(ast.literal_eval(this.domain)).ids
                trans_export_records(lang, this.model_name, ids, buf, this.format, self._cr)
            else:
                mods = sorted(this.mapped('modules.name')) or ['all']
                trans_export(lang, mods, buf, this.format, self._cr)
            out = base64.encodebytes(buf.getvalue())

        filename = 'new'
        if lang:
            filename = tools.get_iso_codes(lang)
        elif this.export_type == 'model':
            filename = this.model_name.replace('.', '_')
        elif len(mods) == 1:
            filename = mods[0]
        extension = this.format
        if not lang and extension == 'po':
            extension = 'pot'
        name = "%s.%s" % (filename, extension)
        this.write({'state': 'get', 'data': out, 'name': name})
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'base.language.export',
            'view_mode': 'form',
            'res_id': this.id,
            'views': [(False, 'form')],
            'target': 'new',
        }