# -*- coding: utf-8 -*-
{
    'name': 'e_pos_mrp_design',
    'version': '18.0.0.1',
    'summary': """Integration POS-MRP with E_Design""",
    'author': 'acevedoesteban999@gmail.com',
    'website': '',
    'category': '',
    'depends': ['sale_mrp', 'e_pos_mrp','e_design'],
    "data": [
        "views/mrp_production.xml",
    ],
    
    'application': False,
    'installable': True,
    'auto_install': True,
    'license': 'LGPL-3',
}
