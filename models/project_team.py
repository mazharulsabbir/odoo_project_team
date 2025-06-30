from odoo import models, fields, api


class ProjectTeam(models.Model):
    _name = 'project.team'
    _description = 'Project Team'
    _rec_name = 'name'
    _order = 'name'

    name = fields.Char(string='Team Name', required=True)
    active = fields.Boolean(string='Active', default=True)
    member_ids = fields.Many2many(
        'res.users',
        'project_team_users_rel',
        'team_id',
        'user_id',
        string='Team Members',
        required=True
    )
    project_ids = fields.One2many(
        'project.project',
        'team_id',
        string='Projects'
    )
    
    @api.depends('member_ids')
    def _compute_member_count(self):
        for team in self:
            team.member_count = len(team.member_ids)
    
    member_count = fields.Integer(
        string='Member Count',
        compute='_compute_member_count',
        store=True
    )