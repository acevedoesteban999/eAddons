{
    'name': 'eDesignImporter',
    'version': '18.0.0.0.0',
    'category': '',
    'summary': '',
    'depends': ['e_design', 'web'],
    'data': [
        'wizards/import_design_wizard.xml',
        'views/menu_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            # 'e_design_import/static/src/components/**/*',
        ],
    },
    'installable': True,
    'application': False,
}