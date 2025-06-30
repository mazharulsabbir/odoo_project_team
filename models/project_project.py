from odoo import models, fields, api


class ProjectProject(models.Model):
    _inherit = 'project.project'

    team_id = fields.Many2one(
        'project.team',
        string='Project Team',
        required=True,
        help='The team assigned to this project'
    )
    
    @api.model
    def create(self, vals):
        project = super(ProjectProject, self).create(vals)
        if project.team_id:
            project._update_project_visibility()
        return project
    
    def write(self, vals):
        res = super(ProjectProject, self).write(vals)
        if 'team_id' in vals:
            self._update_project_visibility()
        return res
    
    def _update_project_visibility(self):
        for project in self:
            if project.team_id:
                # Add team members to project followers
                project.message_subscribe(partner_ids=project.team_id.member_ids.mapped('partner_id').ids)