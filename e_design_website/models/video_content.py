from odoo import models, fields, api

class DesignVideo(models.Model):
    _name = 'e_design_website.video.content'
    _inherit = 'video.content'
    _description = "Video Content"
    
    name = fields.Char("Video Name", required=True)
    ewebsite_published = fields.Boolean("Is Published", default=False)
    