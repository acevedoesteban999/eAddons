# -*- coding: utf-8 -*-

from odoo import models, fields, api, _ , modules , Command


class EGitModuleBase(models.AbstractModel):
    _name = 'ir.module.e_base'
    _description = 'Base Module'
    _rec_name = 'module_name'

    module_name = fields.Char("Module Technical Name", required=True)
    module_icon = fields.Char(compute="_compute_module_icon")
    module_exist = fields.Boolean("Module Exist",compute="_compute_module_exist")
    local_path = fields.Char(compute="_compute_local_path")
    
    _sql_constraints = [
        ('unique_module', 'unique(module_name)', 'Module must be unique!')
    ]
    
    error_msg = fields.Char("Error")
    last_check = fields.Datetime(default=fields.Datetime.now)
    
    # ===================================================================
    # API
    # ===================================================================

    @api.depends('module_name')
    def _compute_local_path(self):
        for rec in self:
            if rec.module_name:
                rec.local_path = modules.get_module_path(rec.module_name)
            else:
                rec.local_path = False
    
    @api.depends('module_name')
    def _compute_module_exist(self):
        for rec in self:
            rec.module_exist = bool(rec.module_name) and  rec.env['ir.module.module'].search_count([('name','=',rec.module_name)]) != 0 and bool(rec.local_path)
    
    
    @api.onchange('module_name')
    def _compute_module_icon(self):
        for rec in self:
            rec.module_icon = f"/{rec.module_name}/static/description/icon.png"