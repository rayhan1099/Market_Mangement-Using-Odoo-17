{
    'name': 'Market Management System',
    'version': '1.0',
    'summary': ' ',
    'description': """ """,
    'author': 'Rayhan',
    'website': 'shajgoj.com',
    'category': 'Management',
    'depends': ['base', 'mail',],
    'data': [
        'security/market_management_security.xml',
        'security/ir.model.access.csv',
        'views/market_views.xml',
        'views/shop_bill_views.xml',
        'views/security_camera.xml',
        'views/lease_agreement_views.xml',
        # 'views/staff_management_views.xml',
        # 'views/sale.xml',
        'views/shop_views.xml',
        'views/tenant_views.xml',
        'views/actions.xml',
        'views/parking_space.xml',
        'views/parking_transaction_views.xml',
        'views/menu.xml',
        # # 'data/ir_cron_data.xml',
        # 'data/lease_agreement_views.xml',
        # 'data/lease_reminder_email_template.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
