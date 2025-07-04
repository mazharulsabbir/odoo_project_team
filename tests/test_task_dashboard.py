from odoo.tests import common, tagged
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


@tagged('post_install', '-at_install')
class TestTaskDashboard(common.TransactionCase):
    
    def setUp(self):
        super(TestTaskDashboard, self).setUp()
        
        # Create test users
        self.user_manager = self.env['res.users'].create({
            'name': 'Dashboard Manager',
            'login': 'dash_manager',
            'email': 'dash_manager@test.com',
            'groups_id': [(6, 0, [self.env.ref('project.group_project_manager').id])]
        })
        
        self.user1 = self.env['res.users'].create({
            'name': 'User 1',
            'login': 'user1_dash',
            'email': 'user1_dash@test.com',
            'groups_id': [(6, 0, [self.env.ref('project.group_project_user').id])]
        })
        
        self.user2 = self.env['res.users'].create({
            'name': 'User 2',
            'login': 'user2_dash',
            'email': 'user2_dash@test.com',
            'groups_id': [(6, 0, [self.env.ref('project.group_project_user').id])]
        })
        
        # Create team
        self.team = self.env['project.team'].create({
            'name': 'Dashboard Team',
            'member_ids': [(6, 0, [self.user1.id, self.user2.id])]
        })
        
        # Create project
        self.project = self.env['project.project'].create({
            'name': 'Dashboard Project',
            'privacy_visibility': 'team',
            'team_id': self.team.id
        })
        
        # Create task stages
        self.stage_todo = self.env['project.task.type'].create({
            'name': 'To Do',
            'sequence': 1,
            'fold': False
        })
        
        self.stage_progress = self.env['project.task.type'].create({
            'name': 'In Progress',
            'sequence': 2,
            'fold': False
        })
        
        self.stage_done = self.env['project.task.type'].create({
            'name': 'Done',
            'sequence': 3,
            'fold': True
        })
        
        # Set stages on project
        self.project.type_ids = [(6, 0, [
            self.stage_todo.id,
            self.stage_progress.id,
            self.stage_done.id
        ])]
    
    def _create_tasks_with_dates(self):
        """Helper method to create tasks with different dates"""
        today = datetime.now().date()
        
        # This week tasks
        self.env['project.task'].create({
            'name': 'This Week Task 1',
            'project_id': self.project.id,
            'user_ids': [(6, 0, [self.user1.id])],
            'stage_id': self.stage_progress.id,
            'create_date': today
        })
        
        # Previous week tasks
        prev_week = today - timedelta(days=7)
        task_prev = self.env['project.task'].create({
            'name': 'Previous Week Task',
            'project_id': self.project.id,
            'user_ids': [(6, 0, [self.user2.id])],
            'stage_id': self.stage_done.id,
        })
        task_prev.create_date = prev_week
        
        # This month tasks
        self.env['project.task'].create({
            'name': 'This Month Task',
            'project_id': self.project.id,
            'user_ids': [(6, 0, [self.user1.id])],
            'stage_id': self.stage_todo.id,
            'create_date': today.replace(day=1)
        })
        
        # Previous month tasks
        prev_month = today - relativedelta(months=1)
        task_prev_month = self.env['project.task'].create({
            'name': 'Previous Month Task',
            'project_id': self.project.id,
            'stage_id': self.stage_done.id,
        })
        task_prev_month.create_date = prev_month
    
    def test_01_dashboard_statistics_all_time(self):
        """Test dashboard statistics for all time period"""
        # Create various tasks
        self._create_tasks_with_dates()
        
        # Add some unassigned tasks
        self.env['project.task'].create({
            'name': 'Unassigned Task',
            'project_id': self.project.id,
            'stage_id': self.stage_todo.id
        })
        
        # Get statistics
        dashboard = self.env['project.task.dashboard']
        stats = dashboard.with_user(self.user_manager).get_task_statistics('all', False)
        
        # Verify totals
        self.assertEqual(stats['total_tasks'], 5)
        
        # Verify stages
        self.assertIn('stages', stats)
        stage_names = [s['name'] for s in stats['stages']]
        self.assertIn('To Do', stage_names)
        self.assertIn('In Progress', stage_names)
        self.assertIn('Done', stage_names)
        
        # Verify stage counts
        for stage in stats['stages']:
            if stage['name'] == 'Done':
                self.assertEqual(stage['count'], 2)
            elif stage['name'] == 'To Do':
                self.assertEqual(stage['count'], 2)
            elif stage['name'] == 'In Progress':
                self.assertEqual(stage['count'], 1)
        
        # Verify assignees
        self.assertEqual(len(stats['assignees']), 4)  # Should show both users
    
    def test_02_dashboard_statistics_this_week(self):
        """Test dashboard statistics for this week filter"""
        self._create_tasks_with_dates()
        
        dashboard = self.env['project.task.dashboard']
        stats = dashboard.with_user(self.user_manager).get_task_statistics('this_week', False)
        
        # Should only count this week's task
        self.assertEqual(stats['total_tasks'], 4)
        
        # Verify stages for this week
        in_progress_stage = next((s for s in stats['stages'] if s['name'] == 'In Progress'), None)
        self.assertIsNotNone(in_progress_stage)
        self.assertEqual(in_progress_stage['count'], 1)
    
    def test_03_dashboard_statistics_user_filter(self):
        """Test dashboard statistics with user filter"""
        self._create_tasks_with_dates()
        
        dashboard = self.env['project.task.dashboard']
        stats = dashboard.with_user(self.user_manager).get_task_statistics('all', self.user1.id)
        
        # Should only show user1's tasks
        self.assertEqual(stats['total_tasks'], 2)  # User1 has 2 tasks
        
        # Assignees should still show all users
        self.assertEqual(len(stats['assignees']), 4)
    
    def test_04_dashboard_security_team_member(self):
        """Test dashboard respects team security for non-managers"""
        # Create another team and project
        other_team = self.env['project.team'].create({
            'name': 'Other Team',
            'member_ids': [(6, 0, [self.user_manager.id])]
        })
        
        other_project = self.env['project.project'].create({
            'name': 'Other Project',
            'privacy_visibility': 'team',
            'team_id': other_team.id
        })
        
        # Create task in other project
        self.env['project.task'].create({
            'name': 'Other Team Task',
            'project_id': other_project.id,
            'user_ids': [(6, 0, [self.user_manager.id])]
        })
        
        # Create task in user's team project
        self.env['project.task'].create({
            'name': 'My Team Task',
            'project_id': self.project.id,
            'user_ids': [(6, 0, [self.user1.id])]
        })
        
        # Get statistics as team member (not manager)
        dashboard = self.env['project.task.dashboard']
        stats = dashboard.with_user(self.user1).get_task_statistics('all', False)
        
        # Should only see tasks from their team's projects
        self.assertEqual(stats['total_tasks'], 1)
    
    def test_05_dashboard_all_users_visible(self):
        """Test that all active users are visible in assignees even with no tasks"""
        # Create user with no tasks
        user_no_tasks = self.env['res.users'].create({
            'name': 'No Tasks User',
            'login': 'no_tasks',
            'email': 'no_tasks@test.com',
            'groups_id': [(6, 0, [self.env.ref('project.group_project_user').id])]
        })
        
        # Add to team
        self.team.member_ids = [(4, user_no_tasks.id)]
        
        # Create one task for another user
        self.env['project.task'].create({
            'name': 'Single Task',
            'project_id': self.project.id,
            'user_ids': [(6, 0, [self.user1.id])]
        })
        
        # Get statistics
        dashboard = self.env['project.task.dashboard']
        stats = dashboard.with_user(self.user_manager).get_task_statistics('all', False)
        
        # All team members should be visible
        assignee_names = [a['name'] for a in stats['assignees']]
        self.assertIn(user_no_tasks.name, assignee_names)
        
        # User with no tasks should have 0 counts
        no_task_user_stat = next(
            (a for a in stats['assignees'] if a['id'] == user_no_tasks.id),
            None
        )
        self.assertIsNotNone(no_task_user_stat)
        self.assertEqual(no_task_user_stat['total_tasks'], 0)
        self.assertEqual(len(no_task_user_stat['stages']), 0)
    
    def test_06_assignee_stages_breakdown(self):
        """Test that assignees show correct stage breakdowns"""
        # Create tasks in different stages for user1
        self.env['project.task'].create({
            'name': 'User1 Todo Task 1',
            'project_id': self.project.id,
            'user_ids': [(6, 0, [self.user1.id])],
            'stage_id': self.stage_todo.id
        })
        
        self.env['project.task'].create({
            'name': 'User1 Todo Task 2',
            'project_id': self.project.id,
            'user_ids': [(6, 0, [self.user1.id])],
            'stage_id': self.stage_todo.id
        })
        
        self.env['project.task'].create({
            'name': 'User1 Progress Task',
            'project_id': self.project.id,
            'user_ids': [(6, 0, [self.user1.id])],
            'stage_id': self.stage_progress.id
        })
        
        self.env['project.task'].create({
            'name': 'User1 Done Task',
            'project_id': self.project.id,
            'user_ids': [(6, 0, [self.user1.id])],
            'stage_id': self.stage_done.id
        })
        
        # Get statistics
        dashboard = self.env['project.task.dashboard']
        stats = dashboard.with_user(self.user_manager).get_task_statistics('all', False)
        
        # Find user1 in assignees
        user1_stat = next(
            (a for a in stats['assignees'] if a['id'] == self.user1.id),
            None
        )
        
        self.assertIsNotNone(user1_stat)
        self.assertEqual(user1_stat['total_tasks'], 4)
        self.assertEqual(len(user1_stat['stages']), 3)  # Should have 3 different stages
        
        # Verify stage counts
        stage_dict = {s['name']: s['count'] for s in user1_stat['stages']}
        self.assertEqual(stage_dict.get('To Do', 0), 2)
        self.assertEqual(stage_dict.get('In Progress', 0), 1)
        self.assertEqual(stage_dict.get('Done', 0), 1)