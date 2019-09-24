from odoo import fields,models,api

class ProjectProposal(models.TransientModel):
    _name='project.proposal'

    project_title=fields.Many2one('project.project',string="Title")
    customer=fields.Many2one('res.partner',string="Customer")
    date=fields.Date("Date")
    objective=fields.Html("Objective")
    suggest_solution=fields.Html("Suggest Solution")
    approach=fields.Html("Approach")
    timeline=fields.One2many('project.proposal.timeline','timeline_id',string="Timeline")

    def print_report(self):
        return self.env.ref('hv_project_proposal.action_create_proposal_report').report_action(self)