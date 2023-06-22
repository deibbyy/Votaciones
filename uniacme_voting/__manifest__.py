# -*- coding: utf-8 -*-
{
    'name': 'Modulo de Votación UNIACME',

    'summary': 'Gestión de procesos de votación para la universidad UNIACME',
    'description': 'Módulo para administrar los procesos de votación en la universidad UNIACME.',
    'author': 'Jon Deiby Estrada Cadavid',
    'category': 'Uncategorized',
    'depends': ['base', 'web', 'website'],
    'data': [
        'views/votacion_views.xml',
        'views/sede_views.xml',
        'views/candidato_views.xml',
        'views/estudiante_views.xml',
        'security/ir.model.access.csv',
        'template/votacion_exitosa_template.xml',
        'template/participar_votacion_template.xml',
        'template/documento_invalido_template.xml',
        'template/ingresar_documento_template.xml',
        'template/votacion_invalida_template.xml',
        'template/votar_template.xml',
        'wizard/votacion_import_wizard_views.xml',
        'data/uniacme_voting_data.xml',
        # 'template/website_template.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}