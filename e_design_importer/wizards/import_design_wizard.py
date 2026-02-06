import os
import base64
from pathlib import Path

from odoo import models, fields, api, _
from odoo.exceptions import UserError

from ..utils.utils import FolderScanner


class ImportDesignWizard(models.TransientModel):
    _name = 'import.design.wizard'
    _description = 'Import Design Wizard'
    
    folder_path = fields.Char(string='Desktop Folder Path', required=True, default="E:\\Esteban\\Programacion\\Python\\Odoo\\Odoo18\\designs")
    preview_data = fields.Json(string='Preview Data', default=dict)
    state = fields.Selection([
        ('select', 'Select Folder'),
        ('preview', 'Preview'),
        ('done', 'Done')
    ], default='select')
    
    def action_scan_folder(self):
        self.ensure_one()
        if not os.path.exists(self.folder_path):
            raise UserError(_('Folder does not exist: %s') % self.folder_path)
        
        scanner = FolderScanner(self.folder_path)
        data = scanner.scan()
        
        def check_design(des):
            if not des:
                return None
            existing_des = self.env['product.edesign'].search([
                ('default_code', '=', des['code'])
            ], limit=1)
            result = {
                'name': des['name'],
                'code': des['code'],
                'path': des['path'],
                'image': des.get('image'),
                'file': des.get('file'),
                'attachments': des.get('attachments', [])
            }
            if existing_des:
                result['existing'] = {
                    'name': existing_des.name,
                    'id': existing_des.id
                }
            return result
        
        def check_product(prod):
            if not prod:
                return None
            existing_prod = self.env['product.template'].search([
                ('default_code', '=', prod['code']),
                ('design_ok', '=', True)
            ], limit=1)
            result = {
                'name': prod['name'],
                'code': prod['code'],
                'path': prod['path'],
                'designs': []
            }
            for des in prod.get('designs', []):
                checked_des = check_design(des)
                if checked_des:
                    result['designs'].append(checked_des)
            if existing_prod:
                result['existing'] = {
                    'name': existing_prod.name,
                    'id': existing_prod.id
                }
            return result
        
        def check_subcategory(sub):
            if not sub:
                return None
            existing_sub = self.env['product.edesign.category'].search([
                ('default_code', '=', sub['code'])
            ], limit=1)
            result = {
                'name': sub['name'],
                'code': sub['code'],
                'path': sub['path'],
                'products': [],
                'designs': []
            }
            for prod in sub.get('products', []):
                checked_prod = check_product(prod)
                if checked_prod:
                    result['products'].append(checked_prod)
            for des in sub.get('designs', []):
                checked_des = check_design(des)
                if checked_des:
                    result['designs'].append(checked_des)
            if existing_sub:
                result['existing'] = {
                    'name': existing_sub.name,
                    'id': existing_sub.id
                }
            return result
        
        def check_category(cat):
            if not cat:
                return None
            existing_cat = self.env['product.edesign.category'].search([
                ('default_code', '=', cat['code'])
            ], limit=1)
            result = {
                'name': cat['name'],
                'code': cat['code'],
                'path': cat['path'],
                'subcategories': [],
                'products': [],
                'designs': []
            }
            for sub in cat.get('subcategories', []):
                checked_sub = check_subcategory(sub)
                if checked_sub:
                    result['subcategories'].append(checked_sub)
            for prod in cat.get('products', []):
                checked_prod = check_product(prod)
                if checked_prod:
                    result['products'].append(checked_prod)
            for des in cat.get('designs', []):
                checked_des = check_design(des)
                if checked_des:
                    result['designs'].append(checked_des)
            if existing_cat:
                result['existing'] = {
                    'name': existing_cat.name,
                    'id': existing_cat.id
                }
            return result
        
        preview_data = {
            'categories': [],
            'products': [],
            'designs': []
        }
        
        for cat in data.get('categories', []):
            checked_cat = check_category(cat)
            if checked_cat:
                preview_data['categories'].append(checked_cat)
        
        for prod in data.get('products', []):
            checked_prod = check_product(prod)
            if checked_prod:
                preview_data['products'].append(checked_prod)
        
        for des in data.get('designs', []):
            checked_des = check_design(des)
            if checked_des:
                preview_data['designs'].append(checked_des)
        
        
        self.write({
            'preview_data': preview_data,
            'state': 'preview'
        })
        
        return self._reload_wizard()
    
    def action_confirm_import(self):
        self.ensure_one()
        scanner = FolderScanner(self.folder_path)
        data = scanner.scan()
        
        category_map = {}
        for cat_data in data['categories']:
            cat = self.env['product.edesign.category'].search([
                ('default_code', '=', cat_data['code'])
            ], limit=1)
            if not cat:
                cat = self.env['product.edesign.category'].create({
                    'name': cat_data['name'],
                    'default_code': cat_data['code']
                })
            category_map[cat_data['code']] = cat.id
        
        for sub_data in data['subcategories']:
            sub = self.env['product.edesign.category'].search([
                ('default_code', '=', sub_data['code'])
            ], limit=1)
            if not sub:
                sub = self.env['product.edesign.category'].create({
                    'name': sub_data['name'],
                    'default_code': sub_data['code'],
                    'parent_id': category_map.get(sub_data['parent_code'])
                })
                category_map[sub_data['code']] = sub.id
        
        for design_data in data['designs']:
            preview_data = self.env['product.edesign'].search([
                ('default_code', '=', design_data['code'])
            ], limit=1)
            if not preview_data:
                files_data = scanner.get_design_files_data(design_data)
                attachment_ids = self._create_attachments(files_data)
                
                self.env['product.edesign'].create({
                    'name': design_data['name'],
                    'default_code': design_data['code'],
                    'category_id': category_map.get(design_data['category_code']),
                    'attachment_ids': [(6, 0, attachment_ids)]
                })
        
        for prod_data in data['products']:
            product = self.env['product.template'].search([
                ('default_code', '=', prod_data['code'])
            ], limit=1)
            design_ids = []
            for d in prod_data['designs']:
                design = self.env['product.edesign'].search([
                    ('default_code', '=', d['code'])
                ], limit=1)
                if design:
                    design_ids.append(design.id)
            
            vals = {
                'name': prod_data['name'],
                'default_code': prod_data['code'],
                'design_ok': True,
                'design_ids': [(6, 0, design_ids)]
            }
            
            if product:
                product.write(vals)
            else:
                self.env['product.template'].create(vals)
        
        self.state = 'done'
        return self._reload_wizard()
    
    def _create_attachments(self, files_data):
        attachment_ids = []
        
        for name, data in files_data['attachments']:
            try:
                attachment = self.env['ir.attachment'].create({
                    'name': name,
                    'datas': data,
                    'res_model': 'product.edesign',
                    'type': 'binary'
                })
                attachment_ids.append(attachment.id)
            except Exception:
                continue
        
        if files_data['image']:
            try:
                name, data = files_data['image']
                attachment = self.env['ir.attachment'].create({
                    'name': name,
                    'datas': data,
                    'res_model': 'product.edesign',
                    'type': 'binary'
                })
                attachment_ids.append(attachment.id)
            except Exception:
                pass
        
        if files_data['file']:
            try:
                name, data = files_data['file']
                attachment = self.env['ir.attachment'].create({
                    'name': name,
                    'datas': data,
                    'res_model': 'product.edesign',
                    'type': 'binary'
                })
                attachment_ids.append(attachment.id)
            except Exception:
                pass
        
        return attachment_ids
    
    def action_back(self):
        self.write({'state': 'select', 'preview_data': {}})
        return self._reload_wizard()
    
    def _reload_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }