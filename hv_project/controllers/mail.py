from odoo import http
import base64
import werkzeug
from odoo.exceptions import AccessError
from odoo.http import request
from odoo.addons.portal.controllers.mail import PortalChatter  # Import the class


class CustomPortalChatter(PortalChatter):  # Inherit in your custom class

    @http.route(['/mail/chatter_post'], type='http', methods=['POST'], auth='public', website=True)
    def portal_chatter_post(self, res_model, res_id, message, **kw):
        res = super(CustomPortalChatter, self).portal_chatter_post(res_model, res_id, message)
        files = request.httprequest.files.getlist('file_upload')
        for file in files:
            attachment_value = {
                'name': file.filename,
                'datas': base64.encodestring(file.read()),
                'datas_fname': file.filename,
                'res_model': res_model,
                'res_id': res_id,
            }
            request.env['ir.attachment'].sudo().create(attachment_value)
        return res