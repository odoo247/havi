from odoo import api,models,fields

class ProposalTimeline(models.TransientModel):
    _name="project.proposal.timeline"

    task=fields.Char(string="Task")
    duration=fields.Integer(string="Duration(days)")
    timeline_id=fields.Many2one('project.proposal','Timeline')