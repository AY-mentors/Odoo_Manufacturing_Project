# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'EgyMentors Manufacturing',
    'version': '16.1.1',
    'category': 'Generic Modules/Human Resources',
    'author': 'Odoo Mates',
    'sequence': -100,
    'summary': 'Test Manufacturing',
    'description': """
This module contains all the common features of Sales Management and eCommerce.
    """,
    'depends': ['sale_management', 'base', 'hr', 'project', 'crm', 'mrp_plm', 'timesheet_grid'],
    'data': [
        'security/ir.model.access.csv',
        'views/project_task_inherit_view.xml',
        'views/project_task_view.xml',
        'views/sales_order_inherit_view.xml',
        'views/tasks_kanban_inherit_view.xml',
    ],
    'demo': [],
    'application': True,
    'installable': True,
    # 'auto_install': False,
    'license': 'LGPL-3',
    # 'assets': {},
}
