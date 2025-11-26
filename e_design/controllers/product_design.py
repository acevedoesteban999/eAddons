from odoo import http , _


class ProductDesign(http.Controller):
    @http.route("/designs", type='http', auth='public',website=True)    
    def designs(self, **kw):
        return http.request.render(
            'e_design.designs',
            {
                'objects': http.request.env['product.design'].search([]),
            },
        )
    @http.route("/design/<design('product.design')>", type='http', auth='public',website=True)    
    def design(self, design,**kw):
        return http.request.render(
            'e_design.design',
            {
                'object': http.request.env['product.design'].search([('id','=',design.id)]),
            },
        )