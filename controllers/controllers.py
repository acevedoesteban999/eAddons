from odoo import http


class Controllers(http.Controller):
    @http.route(['/general','/main'], type='http', auth='public',website=True)
    def main(self, **kw):
        return http.request.render('e_sublimation.MainComponent')
    
    @http.route(['/products'], type='http', auth='public',website=True)
    def products(self, **kw):
        return http.request.render('e_sublimation.ProductComponent')