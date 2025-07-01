from odoo import models, fields, api, tools
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


class ProjectTaskDashboard(models.Model):
    _name = 'project.task.dashboard'
    _description = 'Project Task Dashboard'
    _auto = False
    _order = 'task_count desc'

    name = fields.Char(string='Period')
    task_count = fields.Integer(string='Total Tasks')
    done_count = fields.Integer(string='Done Tasks')
    in_progress_count = fields.Integer(string='In Progress Tasks')
    todo_count = fields.Integer(string='To Do Tasks')
    assignee_id = fields.Many2one('res.users', string='Assignee')
    project_id = fields.Many2one('project.project', string='Project')
    
    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW %s AS (
                SELECT
                    row_number() OVER () as id,
                    rel.user_id as assignee_id,
                    t.project_id as project_id,
                    COUNT(DISTINCT t.id) as task_count,
                    SUM(CASE WHEN t.stage_id IN (
                        SELECT id FROM project_task_type WHERE fold = true
                    ) THEN 1 ELSE 0 END) as done_count,
                    SUM(CASE WHEN t.stage_id IN (
                        SELECT id FROM project_task_type WHERE fold = false
                    ) AND rel.user_id IS NOT NULL THEN 1 ELSE 0 END) as in_progress_count,
                    SUM(CASE WHEN t.stage_id IN (
                        SELECT id FROM project_task_type WHERE fold = false
                    ) AND rel.user_id IS NULL THEN 1 ELSE 0 END) as todo_count,
                    'All' as name
                FROM project_task t
                LEFT JOIN project_task_user_rel rel ON rel.task_id = t.id
                JOIN project_project p ON t.project_id = p.id
                WHERE t.active = true
                GROUP BY rel.user_id, t.project_id
            )
        """ % self._table)

    @api.model
    def get_task_statistics(self, period='all', assignee_id=False):
        """Get task statistics based on period and assignee filters"""
        domain = []
        
        # Apply period filter
        today = fields.Date.today()
        if period == 'this_week':
            week_start = today - timedelta(days=today.weekday())
            domain.append(('create_date', '>=', week_start))
        elif period == 'prev_week':
            week_start = today - timedelta(days=today.weekday() + 7)
            week_end = today - timedelta(days=today.weekday())
            domain.extend([('create_date', '>=', week_start), ('create_date', '<', week_end)])
        elif period == 'this_month':
            month_start = today.replace(day=1)
            domain.append(('create_date', '>=', month_start))
        elif period == 'prev_month':
            month_start = (today - relativedelta(months=1)).replace(day=1)
            month_end = today.replace(day=1)
            domain.extend([('create_date', '>=', month_start), ('create_date', '<', month_end)])
        
        # Apply assignee filter
        if assignee_id:
            domain.append(('user_ids', 'in', assignee_id))
        
        # Apply team security
        user = self.env.user
        if not user.has_group('project.group_project_manager'):
            team_projects = self.env['project.project'].search([
                ('team_id.member_ids', 'in', user.id)
            ]).ids
            domain.append(('project_id', 'in', team_projects))
        
        # Group tasks by stage name
        stage_groups = self.env['project.task'].read_group(
            domain,
            ['stage_id'],
            ['stage_id']
        )
        
        # Calculate statistics dynamically based on stage names
        total_tasks = sum(group['stage_id_count'] for group in stage_groups)
        stages = {}
        
        for group in stage_groups:
            if group['stage_id']:
                stage_name = group['stage_id'][1]  # stage_id returns (id, name)
                if stage_name not in stages:
                    stages[stage_name] = {
                        'name': stage_name,
                        'count': 0
                    }
                stages[stage_name]['count'] += group['stage_id_count']

        # Convert stages dict to list
        stages = list(stages.values())

        stats = {
            'total_tasks': total_tasks,
            'stages': stages,
            'assignees': []
        }
        
        # Get all active users who have access to projects
        all_users = self.env['res.users'].search([
            ('active', '=', True),
            ('share', '=', False)
        ])
        
        # Filter users based on team membership if not a project manager
        if not user.has_group('project.group_project_manager'):
            team_user_ids = self.env['project.project'].search([
                ('team_id.member_ids', 'in', user.id)
            ]).mapped('team_id.member_ids').ids
            all_users = all_users.filtered(lambda u: u.id in team_user_ids)
        
        # Initialize assignee data for all users
        assignee_data = {}
        for u in all_users:
            assignee_data[u.id] = {
                'id': u.id,
                'name': u.name,
                'total_tasks': 0,
                'stages': []
            }
        
        # Count tasks for users by stage using read_group
        user_stage_groups = self.env['project.task'].read_group(
            domain + [('user_ids', '!=', False)],
            ['user_ids', 'stage_id'],
            ['user_ids', 'stage_id'],
            lazy=False
        )
        
        # Process the grouped data
        user_stage_counts = {}
        for group in user_stage_groups:
            if group['user_ids'] and group['stage_id']:
                stage_name = group['stage_id'][1]
                count = group['__count']
                
                for user_id in group['user_ids']:
                    if user_id not in user_stage_counts:
                        user_stage_counts[user_id] = {}
                    if stage_name not in user_stage_counts[user_id]:
                        user_stage_counts[user_id][stage_name] = 0
                    user_stage_counts[user_id][stage_name] += count
        
        # Build assignee data with stage counts
        for user_id, stage_counts in user_stage_counts.items():
            if user_id in assignee_data:
                # assignee_data[user_id]['stages'] = [
                #     {'name': stage_name, 'count': count}
                #     for stage_name, count in stage_counts.items()
                # ]
                assignee_stages = {}
                for stage_name, count in stage_counts.items():
                    if stage_name not in assignee_stages:
                        assignee_stages[stage_name] = {
                            'name': stage_name,
                            'count': 0
                        }
                    assignee_stages[stage_name]['count'] += count

                assignee_data[user_id]['stages'] = list(assignee_stages.values())
                assignee_data[user_id]['total_tasks'] = sum(stage_counts.values())
        
        stats['assignees'] = sorted(list(assignee_data.values()), key=lambda x: x['name'])
        
        return stats