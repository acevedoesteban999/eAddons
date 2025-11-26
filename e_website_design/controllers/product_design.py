from odoo import http , _


class ProductDesign(http.Controller):
    
    @http.route([
        "/catalog",
    ], type='http', auth='public',website=True)    
    def products(self,category=False, **kw):
        return http.request.render(
            'e_website_design.CatalogProducts',
            {
                'products': http.request.env['product.template'].search(
                    [('design_ok','=',True)]),
            },
        )
    @http.route([
        "/catalog/product/<model('product.template'):product>",
    ], type='http', auth='public',website=True)    
    def designs(self,product,**kw):
        product._compute_design_ids()
        referer = http.request.httprequest.headers.get('Referer', '/')
        breadcrumbs = {
            'back_url': referer if referer != http.request.httprequest.url else '/catalog',
            'breadcrumbs':[
                {'name':'Catalog','href':'/catalog'},
                {'name':product.name,'href':False}
            ],
        }
        return http.request.render(
            'e_website_design.CatalogDesigns',
            {
                'designs': http.request.env['product.design'].search([('id','in',product.design_ids.ids)]),
                'breadcrumbs': breadcrumbs, 
            },
        )
    
    @http.route("/design/<model('product.design'):design>", type='http', auth='public',website=True)    
    def design(self, design,**kw):
        return http.request.render(
            'e_website_design.CatalogDesign',
            {
                'object': http.request.env['product.design'].search([('id','=',design.id)]),
            },
        )