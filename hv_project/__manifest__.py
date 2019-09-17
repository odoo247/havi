{
    'name': 'Custom Portal Template',
    'depends': [
        'portal',
        'web',
        'project',
        'mail',
    ],
    'description': "",
    'data': [
        'views/project_portal_template.xml',
        'views/load_button_upload.xml',
        'views/project_view.xml',
        'data/mail_data.xml',
    ],

    'qweb':[
        'static/src/xml/button_upload.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}