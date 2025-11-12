from odoo import http


class Controllers(http.Controller):
    @http.route('/catalog', type='http', auth='public',website=True)
    def catalog(self, **kw):
        return http.request.render('e_sublimation.catalog')