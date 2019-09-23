from odoo import api,models,fields

class ProposalTimeline(models.TransientModel):
    _name="project.proposal.timeline"

    task=fields.Char(string="Task")
    duration=fields.Char(string="Duration")
    timeline_id=fields.Many2one('project.proposal','Timeline')