from odoo.tests import common, tagged
from odoo.exceptions import ValidationError


@tagged('post_install', '-at_install')
class TestTaskAssignment(common.TransactionCase):
    
    def setUp(self):
        super(TestTaskAssignment, self).setUp()
        
        # Create test users
        self.user_member1 = self.env['res.users'].create({
            'name': 'Member 1',
            'login': 'member1_assignment',
            'email': 'member1_assignment@test.com',
            'groups_id': [(6, 0, [self.env.ref('project.group_project_user').id])]
        })
        
        self.user_member2 = self.env['res.users'].create({
            'name': 'Member 2',
            'login': 'member2_assignment',
            'email': 'member2_assignment@test.com',
            'groups_id': [(6, 0, [self.env.ref('project.group_project_user').id])]
        })
        
        self.user_non_member = self.env['res.users'].create({
            'name': 'Non Member',
            'login': 'non_member_assignment',
            'email': 'non_member_assignment@test.com',
            'groups_id': [(6, 0, [self.env.ref('project.group_project_user').id])]
        })
        
        # Create teams
        self.team1 = self.env['project.team'].create({
            'name': 'Assignment Team 1',
            'member_ids': [(6, 0, [self.user_member1.id, self.user_member2.id])]
        })
        
        self.team2 = self.env['project.team'].create({
            'name': 'Assignment Team 2',
            'member_ids': [(6, 0, [self.user_non_member.id])]
        })
        
        # Create projects
        self.project1 = self.env['project.project'].create({
            'name': 'Project Team 1',
            'privacy_visibility': 'team',
            'team_id': self.team1.id
        })
        
        self.project2 = self.env['project.project'].create({
            'name': 'Project Team 2',
            'privacy_visibility': 'team',
            'team_id': self.team2.id
        })
    
    def test_01_task_assignment_domain(self):
        """Test that task assignment domain restricts to team members"""
        # Create task in project1
        task = self.env['project.task'].create({
            'name': 'Test Task',
            'project_id': self.project1.id
        })
        
        # Check computed field
        self.assertEqual(
            set(task.project_team_member_ids.ids),
            set([self.user_member1.id, self.user_member2.id])
        )
    
    def test_02_task_assignment_valid_members(self):
        """Test assigning tasks to valid team members"""
        # Create task with valid assignees
        task = self.env['project.task'].create({
            'name': 'Valid Assignment Task',
            'project_id': self.project1.id,
            'user_ids': [(6, 0, [self.user_member1.id, self.user_member2.id])]
        })
        
        self.assertEqual(len(task.user_ids), 2)
        self.assertIn(self.user_member1, task.user_ids)
        self.assertIn(self.user_member2, task.user_ids)
    
    def test_03_task_project_change_removes_invalid_assignees(self):
        """Test that changing project removes invalid assignees"""
        # Create task with assignees in project1
        task = self.env['project.task'].create({
            'name': 'Project Change Task',
            'project_id': self.project1.id,
            'user_ids': [(6, 0, [self.user_member1.id, self.user_member2.id])]
        })
        
        self.assertEqual(len(task.user_ids), 2)
        
        # Change to project2 (different team)
        task.project_id = self.project2
        task._onchange_project_id_team_filter()
        
        # Previous assignees should be removed as they're not in team2
        self.assertEqual(len(task.user_ids), 0)
    
    def test_04_task_project_change_keeps_valid_assignees(self):
        """Test that changing project keeps valid assignees"""
        # Add user to both teams
        self.team2.member_ids = [(4, self.user_member1.id)]
        
        # Create task with assignee
        task = self.env['project.task'].create({
            'name': 'Keep Assignee Task',
            'project_id': self.project1.id,
            'user_ids': [(6, 0, [self.user_member1.id])]
        })
        
        # Change to project2
        task.project_id = self.project2
        task._onchange_project_id_team_filter()
        
        # Member1 should remain as they're in both teams
        self.assertIn(self.user_member1, task.user_ids)
    
    def test_05_task_no_project_clears_assignees(self):
        """Test that removing project clears assignees"""
        # Create task with assignees
        task = self.env['project.task'].create({
            'name': 'No Project Task',
            'project_id': self.project1.id,
            'user_ids': [(6, 0, [self.user_member1.id])]
        })
        
        # Remove project
        task.project_id = False
        task._onchange_project_id_team_filter()
        
        # Assignees should be cleared
        self.assertEqual(len(task.user_ids), 0)
    
    def test_06_task_assignment_non_team_privacy(self):
        """Test task assignment when project privacy is not 'team'"""
        # Create project with different privacy
        project_public = self.env['project.project'].create({
            'name': 'Public Project',
            'privacy_visibility': 'followers',
            'team_id': self.team1.id
        })
        
        # Create task - should allow any user assignment
        task = self.env['project.task'].create({
            'name': 'Public Task',
            'project_id': project_public.id,
            'user_ids': [(6, 0, [self.user_non_member.id])]
        })
        
        # Non-member can be assigned when privacy is not 'team'
        self.assertIn(self.user_non_member, task.user_ids)