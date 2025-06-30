from odoo.tests import common, tagged
from odoo.exceptions import AccessError


@tagged('post_install', '-at_install')
class TestProjectSecurity(common.TransactionCase):
    
    def setUp(self):
        super(TestProjectSecurity, self).setUp()
        
        # Create test users
        self.user_manager = self.env['res.users'].create({
            'name': 'Project Manager',
            'login': 'pm_test',
            'email': 'pm@test.com',
            'groups_id': [(6, 0, [self.env.ref('project.group_project_manager').id])]
        })
        
        self.user_team_member = self.env['res.users'].create({
            'name': 'Team Member',
            'login': 'tm_test',
            'email': 'tm@test.com',
            'groups_id': [(6, 0, [self.env.ref('project.group_project_user').id])]
        })
        
        self.user_other = self.env['res.users'].create({
            'name': 'Other User',
            'login': 'other_test',
            'email': 'other@test.com',
            'groups_id': [(6, 0, [self.env.ref('project.group_project_user').id])]
        })
        
        # Create teams
        self.team1 = self.env['project.team'].create({
            'name': 'Team 1',
            'member_ids': [(6, 0, [self.user_team_member.id])]
        })
        
        self.team2 = self.env['project.team'].create({
            'name': 'Team 2',
            'member_ids': [(6, 0, [self.user_other.id])]
        })
        
        # Create projects with different privacy settings
        self.project_team_privacy = self.env['project.project'].create({
            'name': 'Team Privacy Project',
            'privacy_visibility': 'team',
            'team_id': self.team1.id
        })
        
        self.project_followers_privacy = self.env['project.project'].create({
            'name': 'Followers Privacy Project',
            'privacy_visibility': 'followers',
            'team_id': self.team2.id
        })
    
    def test_01_project_visibility_team_member(self):
        """Test that team members can see their team's projects"""
        # Team member should see their team's project
        projects = self.env['project.project'].with_user(self.user_team_member).search([])
        self.assertIn(self.project_team_privacy, projects)
        
        # Team member should not see other team's project with team privacy
        project_other_team = self.env['project.project'].create({
            'name': 'Other Team Project',
            'privacy_visibility': 'team',
            'team_id': self.team2.id
        })
        
        projects = self.env['project.project'].with_user(self.user_team_member).search([])
        self.assertNotIn(project_other_team, projects)
    
    def test_02_project_visibility_non_team_member(self):
        """Test that non-team members cannot see team projects"""
        # Other user should not see team1's project
        projects = self.env['project.project'].with_user(self.user_other).search([])
        self.assertNotIn(self.project_team_privacy, projects)
    
    def test_03_project_visibility_manager(self):
        """Test that project managers can see all projects"""
        # Manager should see all projects
        projects = self.env['project.project'].with_user(self.user_manager).search([])
        self.assertIn(self.project_team_privacy, projects)
        self.assertIn(self.project_followers_privacy, projects)
    
    def test_04_project_visibility_followers_privacy(self):
        """Test that followers privacy works independently of teams"""
        # Add user as follower
        self.project_followers_privacy.message_subscribe(
            partner_ids=[self.user_team_member.partner_id.id]
        )
        
        # User should see the project even though not in team2
        projects = self.env['project.project'].with_user(self.user_team_member).search([])
        self.assertIn(self.project_followers_privacy, projects)
    
    def test_05_task_visibility_team_member(self):
        """Test task visibility for team members"""
        # Create task in team project
        task = self.env['project.task'].create({
            'name': 'Team Task',
            'project_id': self.project_team_privacy.id,
            'user_ids': [(6, 0, [self.user_team_member.id])]
        })
        
        # Team member should see the task
        tasks = self.env['project.task'].with_user(self.user_team_member).search([])
        self.assertIn(task, tasks)
        
        # Other user should not see the task (because not in team and not assigned)
        tasks = self.env['project.task'].with_user(self.user_other).search([])
        self.assertNotIn(task, tasks)
        
        # But if we create the task with user_other as creator, they should see it
        task_created_by_other = self.env['project.task'].with_user(self.user_other).create({
            'name': 'Task Created by Other',
            'project_id': self.project_team_privacy.id
        })
        
        # Other user should see their own created task
        tasks = self.env['project.task'].with_user(self.user_other).search([])
        self.assertIn(task_created_by_other, tasks)
        # But still not see the first task
        self.assertNotIn(task, tasks)
    
    def test_06_task_visibility_assigned_user(self):
        """Test that assigned users can see tasks even if not team members"""
        # Create task and assign to non-team member
        task = self.env['project.task'].create({
            'name': 'Assigned Task',
            'project_id': self.project_team_privacy.id,
            'user_ids': [(6, 0, [self.user_other.id])]
        })
        
        # Assigned user should see the task
        tasks = self.env['project.task'].with_user(self.user_other).search([])
        self.assertIn(task, tasks)
    
    def test_07_project_create_update_followers(self):
        """Test that team members are added as followers on project creation"""
        # Check that team members are followers
        follower_partners = self.project_team_privacy.message_partner_ids
        self.assertIn(self.user_team_member.partner_id, follower_partners)
        
        # Update team
        self.project_team_privacy.team_id = self.team2
        
        # Check that new team members are followers
        follower_partners = self.project_team_privacy.message_partner_ids
        self.assertIn(self.user_other.partner_id, follower_partners)