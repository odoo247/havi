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
                        for i in self.project_id.message_follower_ids:
                            mail_obj=self.env['mail.mail']
                            print("send")
                            mail=mail_obj.create({
                                'body_html':"The remaining time is very low",
                                'email_to':i.partner_id.email,
                                'subject':'Remind'
                            })
                            mail.send()
                        this_project.write({'first_reminder': True})
            second_reminder=self.env['project.project'].search([('name','=',self.project_id.name)])
            if not second_reminder.second_reminder:
                if total_hours_project <= 0:
                    for i in self.project_id.message_follower_ids:
                        mail_obj = self.env['mail.mail']
                        mail=mail_obj.create({
                            'body_html':"The time is over",
                            'email_to': i.partner_id.email,
                            'subject':"Notice",
                        })
                        mail.send()
                    second_reminder.write({'second_reminder':True})
        self.remain_hour_support=total_hours_project
        this_project.write({'remaining_hour':total_hours_project})