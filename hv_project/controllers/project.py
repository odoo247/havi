from odoo import http
from odoo.addons.project.controllers.portal import CustomerPortal

from odoo.http import request


class CustomerPortal(CustomerPortal):
    @http.route()
    def portal_my_projects(self,**kw):
        response=super().portal_my_projects(self,**kw)
        tasks=request.env['project.task']
        response.qcontext['tasks']=tasks
        return response