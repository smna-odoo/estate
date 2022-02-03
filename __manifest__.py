# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Real Estate',
    'version': '1.0',
    'category': 'Sales',
    'author': 'smit',
    'depends': ['base','account'],
#     'summary': '',
    'description': "Real Estate",
#     'website': 'https://www.odoo.com/page/estate',
    'installable': True,
    'application': True,
    'auto_install': False,
    'data' : [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/estate.menus.xml',
        'views/estate.property.views.xml',
        'wizard/estate_wizard_views.xml',
        'views/estate_template.xml',
    ],
}
