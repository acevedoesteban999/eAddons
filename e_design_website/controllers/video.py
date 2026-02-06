from odoo import http, _
from odoo.http import request
import json
from .controllers import Breadcrumb

class VideoController(http.Controller):
    
    @http.route([
        "/edesigns/videos",
    ], type='http', auth='public', website=True)    
    def videos(self, **kw):
        
        videos = http.request.env['e_design_website.video.content'].search([
            ('ewebsite_published','=',True),
            ('video_data','!=',False)
        ])
        
        breadcrumb_manager = Breadcrumb(
            http.request,
            '/edesigns/home',
            [
                ('Home', '/edesigns/home'),
                (_('Videos'), False),
            ] 
        )
        
        
        return http.request.render(
            'e_design_website.VideosContent',
            {
                'title': _("Videos"),
                'breadcrumbs_context': breadcrumb_manager._dict(),
                'videos': videos,
            },
        )
        
    @http.route([
        "/edesigns/videos/<model('e_design_website.video.content'):video>",
    ], type='http', auth='public', website=True)    
    def video(self, video,**kw):
        
        breadcrumb_manager = Breadcrumb(
            http.request,
            '/edesigns/home',
            [
                ('Home', '/edesigns/home'),
                (_('Videos'), '/edesigns/videos'),
                ( video.name, False),
            ] 
        )
        
        
        return http.request.render(
            'e_design_website.VideoContent',
            {
                'title': video.name,
                'breadcrumbs_context': breadcrumb_manager._dict(),
                'video': video,
            },
        )
    