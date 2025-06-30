{
    'name': 'Project Team Rules',
    'version': '16.0.1.0.0',
    'category': 'Project',
    'summary': 'Manage project team rules and permissions',
    'description': """""",
    'author': 'Md Mazharul Islam',
    'website': 'https://mazharul.odoo.com',
    'license': 'LGPL-3',
    'depends': ['base', 'project'],
    'data': [
        'security/ir.model.access.csv',
        'security/project_security.xml',

        'views/dashboard_views.xml',
        'views/project_team_views.xml',
        'views/project_views.xml',
        'views/project_task_views.xml',

        'views/menu_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'project_team_rules/static/src/js/task_dashboard.js',
            'project_team_rules/static/src/xml/task_dashboard.xml',
        ],
    },
    'demo': [],
    'installable': True,
    'application': False,
    'auto_install': False,
}
