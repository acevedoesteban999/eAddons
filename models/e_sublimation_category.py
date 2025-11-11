# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class E_sublimationCategory(models.Model):
    _name = 'e_sublimation.category'
    _description = 'E_sublimationCategory'

    name = fields.Char('Name')
    image = fields.Image("Image")
    description = fields.Text("Description")
    child_ids = fields.One2many('product.template','category_sublimation_id','Childs')
