from odoo import http , _
import json

class ProductDesign(http.Controller):
    
    @http.route([
        "/catalog",
    ], type='http', auth='public',website=True)    
    def products(self,category=False, **kw):
        products = http.request.env['product.template'].search([('design_ok','=',True)])
        return http.request.render(
            'e_website_design.CatalogProducts',
            {
                'products': products
            },
        )
    @http.route([
        "/catalog/product/<model('product.template'):product>",
    ], type='http', auth='public',website=True)    
    def designs(self,product,**kw):
        referer = http.request.httprequest.headers.get('Referer', '/')
        breadcrumbs_context = {
            'back_url': referer if referer != http.request.httprequest.url else '/catalog',
            'breadcrumbs':[
                {
                    'name':'Catalog',
                    'href':'/catalog'
                },
                {
                    'name':product.name,
                    'href':False
                }
            ],
        }
        controller_context = {
            'product_id':product.id
        }
        return http.request.render(
            'e_website_design.CatalogDesigns',
            {
                'breadcrumbs_context':breadcrumbs_context,
                'controller_context': json.dumps(controller_context), 
            },
        )
    
    @http.route("/catalog/product/<model('product.template'):product>/design/<model('product.design'):design>", type='http', auth='public',website=True)    
    def design(self,design,product=False,**kw):
        if design:
            referer = http.request.httprequest.headers.get('Referer', '/')
            breadcrumbs_context = {
                'back_url': referer if referer != http.request.httprequest.url else '/catalog',
                'breadcrumbs':[
                    {
                        'name':'Catalog',
                        'href':'/catalog'
                    },
                    {
                        'name':product.name,
                        'href':f'/catalog/product/{product.id}'
                    },
                    {
                        'name':design.name,
                        'href':False
                    }
                ],
            }
            return http.request.render(
                'e_website_design.CatalogDesign',
                {
                    'object': design,
                    'breadcrumbs_context':breadcrumbs_context,
                },
            )
        else:
            return http.request.not_found()