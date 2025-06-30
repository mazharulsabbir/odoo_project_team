from odoo.tests import common, tagged
from odoo.exceptions import ValidationError, AccessError


@tagged('post_install', '-at_install')
class TestProjectTeam(common.TransactionCase):
    
    def setUp(self):
        super(TestProjectTeam, self).setUp()
        
        # Create test users
        self.user_manager = self.env['res.users'].create({
            'name': 'Project Manager',
            'login': 'manager_test',
            'email': 'manager@test.com',
            'groups_id': [(6, 0, [self.env.ref('project.group_project_manager').id])]
        })
        
        self.user_member1 = self.env['res.users'].create({
            'name': 'Team Member 1',
            'login': 'member1_test',
            'email': 'member1@test.com',
            'groups_id': [(6, 0, [self.env.ref('project.group_project_user').id])]
        })
        
        self.user_member2 = self.env['res.users'].create({
            'name': 'Team Member 2',
            'login': 'member2_test',
            'email': 'member2@test.com',
            'groups_id': [(6, 0, [self.env.ref('project.group_project_user').id])]
        })
        
        self.user_non_member = self.env['res.users'].create({
            'name': 'Non Team Member',
            'login': 'non_member_test',
            'email': 'non_member@test.com',
            'groups_id': [(6, 0, [self.env.ref('project.group_project_user').id])]
        })
        
        # Create test team
        self.project_team = self.env['project.team'].create({
            'name': 'Test Team',
            'member_ids': [(6, 0, [self.user_member1.id, self.user_member2.id])]
        })
    
    def test_01_team_creation(self):
        """Test team creation with members"""
        self.assertEqual(self.project_team.name, 'Test Team')
        self.assertEqual(len(self.project_team.member_ids), 2)
        self.assertIn(self.user_member1, self.project_team.member_ids)
        self.assertIn(self.user_member2, self.project_team.member_ids)
        self.assertEqual(self.project_team.member_count, 2)
    
    def test_02_team_member_count(self):
        """Test member count computation"""
        # Add a member
        self.project_team.member_ids = [(4, self.user_manager.id)]
        self.assertEqual(self.project_team.member_count, 3)
        
        # Remove a member
        self.project_team.member_ids = [(3, self.user_member1.id)]
        self.assertEqual(self.project_team.member_count, 2)
    
    def test_03_team_archive(self):
        """Test team archiving functionality"""
        self.assertTrue(self.project_team.active)
        
        # Archive the team
        self.project_team.active = False
        self.assertFalse(self.project_team.active)
        
        # Search should not find archived teams by default
        teams = self.env['project.team'].search([])
        self.assertNotIn(self.project_team, teams)
        
        # Search with active=False should find it
        teams = self.env['project.team'].with_context(active_test=False).search([])
        self.assertIn(self.project_team, teams)
    
    def test_04_team_with_projects(self):
        """Test team relationship with projects"""
        # Create project with team
        project = self.env['project.project'].create({
            'name': 'Test Project',
            'privacy_visibility': 'team',
            'team_id': self.project_team.id
        })
        
        self.assertEqual(len(self.project_team.project_ids), 1)
        self.assertEqual(self.project_team.project_ids[0], project)
        
        # Create another project
        project2 = self.env['project.project'].create({
            'name': 'Test Project 2',
            'privacy_visibility': 'team',
            'team_id': self.project_team.id
        })
        
        self.assertEqual(len(self.project_team.project_ids), 2)