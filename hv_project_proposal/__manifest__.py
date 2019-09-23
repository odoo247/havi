{
    'name': 'Custom Create Proposal Template',
    'depends': [
        'portal',
        'web',
        'project',
        'mail',
    ],
    'description': "",
    'data': [
        'views/project_view.xml',
        'wizard/create_proposal_view.xml',
        'wizard/project_proposal_timeline.xml',
        'reports/proposal.xml',
        'reports/report.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}