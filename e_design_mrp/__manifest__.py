# -*- coding: utf-8 -*-
{
    'name': 'ePosMrp',
    'version': '18.1.0.0',
    'summary': """Integration POS-MRP with eDesign""",
    'description':"""
                    It allows you to view the designs of the product 
                    to be manufactured in the manufacturing orders.
                """,
    'author': 'acevedoesteban999@gmail.com',
    'website': 'https://github.com/acevedoesteban999/eAddons/blob/18.0/e_design_mrp',
    'category': 'Customizations',
    'depends': ['sale_mrp','e_design'],
    "data": [
        "views/mrp_production.xml",
    ],
    'images': [
        'static/description/banner.png',
    ],
    'application': False,
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
