from odoo import models, fields, api


class ProjectTask(models.Model):
    _inherit = 'project.task'

    project_team_member_ids = fields.Many2many(
        'res.users',
        related='project_id.team_id.member_ids',
        string='Project Team Members',
        readonly=True, store=False
    )

    @api.onchange('project_id')
    def _onchange_project_id_team_filter(self):
        """Clear assignees when project changes to ensure only team members are assigned"""
        if self.project_id and self.user_ids:
            # Filter out users who are not in the new project's team
            team_member_ids = self.project_id.team_id.member_ids.ids
            invalid_assignees = self.user_ids.filtered(lambda u: u.id not in team_member_ids)
            self.user_ids -= invalid_assignees
        else:
            self.user_ids = False
