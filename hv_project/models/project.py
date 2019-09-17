from odoo import fields,models,api
from odoo.exceptions import Warning,ValidationError
import datetime
from datetime import date,time
class ProjectExtend(models.Model):
    _inherit="project.project"

    first_reminder = fields.Boolean(default=False)
    second_reminder = fields.Boolean(default=False)
    hour_support=fields.Float("Hours Support")
    remaining_hour=fields.Float("Remaining",readonly=True)
    percent=fields.Float("Percent Reminder")

    @api.onchange('hour_support')
    def change_value(self):
        a=self.env['project.project'].search([('name','=',self.name)])
        total=self.hour_support
        total_tasks = self.env['project.task'].search([('project_id.name', '=', self.name)])
        for i in total_tasks:
            for j in i.timesheet_ids:
                if date.today().month == j.date.month:
                    total-=j.unit_amount
        a.write({'remaining_hour':total})

class TaskExtend(models.Model):
    _inherit="project.task"

    remain_hour_support=fields.Float("Remain Hours Support",compute='_computer_hour_support',readonly=True)

    def act_send_email(self):
        template_id=self.env.ref('hv_project.email_template_project_task').id
        template=self.env['mail.template'].browse(template_id)
        follower=self.env['project.project'].search([('name','=',self.project_id.name)]).message_follower_ids
        for i in follower:
            template.write({'email_to':i.partner_id.email})
            template.send_mail(self.id,force_send=True)

    def _computer_hour_support(self):
        total_hours_project=self.project_id.hour_support
        total_tasks=self.env['project.task'].search([('project_id','=',self.project_id.name)])
        for i in total_tasks:
            for j in i.timesheet_ids:
                if date.today().month == j.date.month:
                    total_hours_project-=j.unit_amount
        state=self.project_id.first_reminder
        this_project = self.env['project.project'].search([('name','=',self.project_id.name)])
        if self.project_id.hour_support != 0:
            if total_hours_project != 0:
                if not state:
                    if (total_hours_project/self.project_id.hour_support)*100 < self.project_id.percent:
                        template_id = self.env.ref('hv_project.email_template_project_task_remind_first').id
                        template = self.env['mail.template'].browse(template_id)
                        follower = self.env['project.project'].search([('name', '=', self.project_id.name)]).message_follower_ids
                        for i in follower:
                            template.write({'email_to': i.partner_id.email})
                            template.send_mail(self.id, force_send=True)
                    this_project.write({'first_reminder': True})
            second_reminder=self.env['project.project'].search([('name','=',self.project_id.name)])
            if not second_reminder.second_reminder:
                if total_hours_project <= 0:
                    template_id = self.env.ref('hv_project.email_template_project_task_remind_second').id
                    template = self.env['mail.template'].browse(template_id)
                    follower = self.env['project.project'].search([('name', '=', self.project_id.name)]).message_follower_ids
                    for i in follower:
                        template.write({'email_to': i.partner_id.email})
                        template.send_mail(self.id, force_send=True)
                    second_reminder.write({'second_reminder':True})
        self.remain_hour_support=total_hours_project
        this_project.write({'remaining_hour':total_hours_project})