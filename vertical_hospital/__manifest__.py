# -*- coding: utf-8 -*-
{
    'name': "vertical_hospital",
    'summary': "Aplicación para gestión de hospitales",
    'description': "Gestión de pacientes y tratamientos en hospitales",
    'author': "Pedro Julio Guerrero",
    'category': 'Healthcare',
    'version': '1.0',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/views.xml',
        'views/config_views.xml',
        'views/hospital_menu.xml',
        'views/paciente_views.xml',
        'views/tratamiento_views.xml',
        'views/paciente_report.xml',
        # 'views/report_templates.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'vertical_hospital/static/description/icon.png',
        ]
    },
    'License': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
}
