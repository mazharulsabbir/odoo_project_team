# Project Team Rules

A comprehensive Odoo 16 module for managing project teams and implementing team-based access control with an advanced task dashboard.

## Overview

The Project Team Rules module enhances Odoo's project management capabilities by introducing a new privacy visibility option "Assigned Team Only" and a powerful task analytics dashboard. This module seamlessly integrates with Odoo's existing privacy model, adding team-based access control alongside the standard privacy options.

## Features

### 1. Enhanced Privacy Visibility
- Adds "Assigned Team Only" option to project privacy settings
- Integrates with existing privacy options (Followers, All Internal Users, etc.)
- Team-based access only applies when privacy is set to "Assigned Team Only"
- Automatic fallback to default privacy if team mode is removed

### 2. Team Management
- Create and manage project teams with multiple members
- Assign teams to projects for access control
- Teams are required only when privacy is set to "Assigned Team Only"
- Filter teams to show only internal users (non-portal users)

### 3. Flexible Security Model
- Projects with "Assigned Team Only" privacy are visible only to team members
- Other privacy modes work as standard Odoo behavior
- Tasks inherit project visibility rules
- Project managers retain full access regardless of privacy settings

### 4. Advanced Task Dashboard (Project Managers Only)
- Real-time task statistics with visual cards
- Dual filtering system:
  - Time-based: All Time, This Week, Previous Week, This Month, Previous Month
  - User-based: Filter by specific team members or view all
- Interactive statistics showing Total, Done, In Progress, and To Do tasks
- Assignee table with "View Tasks" action for detailed task lists
- Centered filter controls for better UI

### 5. Smart Task Assignment
- When privacy is "Assigned Team Only", assignees are restricted to team members
- Automatic validation when changing projects
- Invalid assignees are removed when project team changes
- Domain restrictions ensure data integrity

## Installation

### Prerequisites
- Odoo 16.0
- Project module installed and configured
- Administrator access for module installation

### Installation Steps

1. **Copy Module to Addons Directory**
   ```bash
   cp -r project_team_rules /path/to/odoo/custom-addons/
   ```

2. **Update Module List**
   - Navigate to Apps menu in Odoo
   - Click "Update Apps List" (Developer mode must be enabled)
   - Confirm the action

3. **Install the Module**
   - Search for "Project Team Rules" in the Apps menu
   - Click "Install" on the module card
   - Wait for installation to complete

4. **Configure User Permissions**
   - Ensure users have appropriate project permissions
   - Project managers have full access
   - Regular users see only their team's projects

## Menu Navigation

### Project Teams Management
**Location:** Project → Configuration → Project Teams

- **List View:** View all project teams with member count
- **Form View:** Create/edit teams and manage members
- **Features:**
  - Add/remove team members
  - View associated projects
  - Archive inactive teams

### Task Dashboard
**Location:** Project → Reporting → Task Dashboard  
**Access:** Project Managers only

- **Dashboard Features:**
  - **Filter Controls (Centered):**
    - Time Period Dropdown: All Time, This Week, Previous Week, This Month, Previous Month
    - User Filter Dropdown: All Users or specific team members
  
  - **Statistics Cards:**
    - Total Tasks (clickable to view task list)
    - Done Tasks
    - In Progress Tasks
    - To Do Tasks
  
  - **Assignee Table:**
    - Shows all active team members with their task counts
    - "View Tasks" button opens filtered task list for that user
    - Always displays all users, even with zero tasks

## Usage Guide

### Creating a Project Team

1. Navigate to Project → Configuration → Project Teams
2. Click "New" to create a team
3. Enter team name
4. Add team members (only internal users)
5. Save the team

### Configuring Project Privacy and Teams

1. Open any project in form view
2. Set "Privacy Visibility" to "Assigned Team Only"
3. The "Project Team" field becomes required
4. Select the appropriate team from the dropdown
5. Save the project

**Note:** The team field is only required when privacy is set to "Assigned Team Only"

### Using the Task Dashboard

1. Navigate to Project → Reporting → Task Dashboard
2. Select time period from the dropdown
3. Optionally filter by specific user
4. View statistics and click on cards for details
5. Use "View Tasks" button to see individual user tasks

### Task Assignment

1. When creating or editing a task
2. The assignee dropdown only shows team members
3. If project changes, invalid assignees are automatically removed

## Security Model

### Access Rules

1. **Projects:** 
   - When privacy is "Assigned Team Only": Visible only to team members
   - Other privacy modes: Standard Odoo behavior applies
   - Project managers always have full access

2. **Tasks:** Visible to:
   - Team members of the project (when project privacy is "Assigned Team Only")
   - Users assigned to the task
   - Task creators
   - Project managers (full access)

### User Groups

- **Project User:** Standard access with team restrictions
- **Project Manager:** Full access to all projects and teams

## Testing

### Test Coverage

The module includes comprehensive unit tests covering all major functionality:

#### Test Files
1. **`test_project_team.py`** - Project Team Model Tests
   - Team creation and member management
   - Member count computation
   - Team archiving functionality
   - Team-project relationships

2. **`test_project_security.py`** - Security Rules Tests
   - Team member project visibility
   - Non-member access restrictions
   - Manager override permissions
   - Privacy mode integration (followers vs team)
   - Task visibility rules
   - Follower management automation

3. **`test_task_assignment.py`** - Task Assignment Tests
   - Assignee domain restrictions
   - Valid team member assignments
   - Project change validation
   - Cross-team user scenarios
   - Privacy mode bypass testing

4. **`test_task_dashboard.py`** - Dashboard Functionality Tests
   - Statistics calculation accuracy
   - Time-based filtering (week/month)
   - User-specific filtering
   - Security compliance for non-managers
   - User visibility in dropdowns

### Running Tests

#### Prerequisites
- Odoo 16 development environment
- Test database (separate from production)
- Module dependencies installed

#### Command Line Testing

**Install Module and Run All Tests:**
```bash
python3 odoo-bin \
  --addons-path=/path/to/addons \
  -d test_database \
  -i project_team_rules \
  --test-enable \
  --stop-after-init \
  --log-level=test
```

**Run Tests for Existing Installation:**
```bash
python3 odoo-bin \
  --addons-path=/path/to/addons \
  -d your_database \
  --test-tags=project_team_rules \
  --test-enable \
  --stop-after-init
```

**Run Specific Test Files:**
```bash
# Test only security functionality
python3 odoo-bin -d test_db --test-tags=project_team_rules.TestProjectSecurity --test-enable --stop-after-init

# Test only dashboard functionality
python3 odoo-bin -d test_db --test-tags=project_team_rules.TestTaskDashboard --test-enable --stop-after-init

# Test only team management
python3 odoo-bin -d test_db --test-tags=project_team_rules.TestProjectTeam --test-enable --stop-after-init

# Test only task assignment
python3 odoo-bin -d test_db --test-tags=project_team_rules.TestTaskAssignment --test-enable --stop-after-init
```

**Verbose Test Output:**
```bash
# Detailed test output
python3 odoo-bin -d test_db -i project_team_rules --test-enable --stop-after-init --log-level=debug

# Test-specific logging
python3 odoo-bin -d test_db --test-tags=project_team_rules --test-enable --stop-after-init --log-handler=odoo.addons.project_team_rules:DEBUG
```

#### Test with Coverage (Optional)
```bash
# Install coverage first
pip3 install coverage

# Run tests with coverage
coverage run --source=addons/project_team_rules odoo-bin -d test_db -i project_team_rules --test-enable --stop-after-init

# Generate coverage report
coverage report -m
coverage html  # Creates htmlcov/index.html
```

### Test Configuration

**Example test configuration file (`test.conf`):**
```ini
[options]
addons_path = /path/to/custom-addons,/path/to/odoo/addons,/path/to/enterprise
db_host = localhost
db_port = 5432
db_user = odoo
db_password = odoo
log_level = test
test_enable = True
```

**Run with configuration:**
```bash
python3 odoo-bin -c test.conf -d test_database -i project_team_rules --stop-after-init
```

### Development Testing Workflow

**1. During Development:**
```bash
# Quick test after changes
python3 odoo-bin -d dev_db -u project_team_rules --test-tags=project_team_rules --test-enable --stop-after-init
```

**2. Pre-commit Testing:**
```bash
# Full test suite
python3 odoo-bin -d clean_test_db -i project_team_rules --test-enable --stop-after-init
```

**3. Continuous Integration:**
```bash
# Automated testing script
#!/bin/bash
createdb test_project_team_rules
python3 odoo-bin \
  --addons-path=/ci/addons \
  -d test_project_team_rules \
  -i project_team_rules \
  --test-enable \
  --stop-after-init \
  --log-level=error
exit_code=$?
dropdb test_project_team_rules
exit $exit_code
```

### Test Results Interpretation

**Successful Output:**
```
2025-01-XX XX:XX:XX,XXX INFO test_db odoo.modules.loading: loading 1 modules...
2025-01-XX XX:XX:XX,XXX INFO test_db odoo.addons.project_team_rules.tests.test_project_team: test_01_team_creation ... ok
2025-01-XX XX:XX:XX,XXX INFO test_db odoo.addons.project_team_rules.tests.test_project_team: test_02_member_count ... ok
...
Ran XX tests in X.XXXs
OK
```

**Failed Test Example:**
```
FAIL: test_05_task_visibility_team_member
AssertionError: <project.task(X,)> unexpectedly found in <project.task(X,Y,Z)>
```

### Test Environment Setup

**Docker Testing (Optional):**
```dockerfile
FROM odoo:16

COPY ./project_team_rules /mnt/extra-addons/project_team_rules

ENV ODOO_RC /etc/odoo/odoo.conf
RUN echo "test_enable = True" >> /etc/odoo/odoo.conf
```

```bash
docker run --rm -e POSTGRES_PASSWORD=odoo -d --name db postgres:13
docker run --rm --link db:db -v $(pwd):/mnt/extra-addons odoo:16 \
  -d test_db -i project_team_rules --test-enable --stop-after-init
```

## Technical Details

### Models

1. **project.team**
   - Stores team information and members
   - Many2many relationship with users

2. **project.project** (inherited)
   - Added team_id field and privacy_visibility extension
   - Automatic follower management

3. **project.task** (inherited)
   - Domain restrictions on user_ids field
   - Automatic assignee validation

4. **project.task.dashboard**
   - SQL view for performance
   - Real-time statistics calculation

### Security Rules Updated

The module updates several existing Odoo security rules to handle the new 'team' privacy option:
- `project.project_public_members_rule`
- `project.report_project_task_user_rule`
- `project.burndown_chart_project_user_rule`
- `project.task_visibility_rule`
- `project.ir_rule_private_task`

### Dependencies

- base
- project

### License

LGPL-3

## Author

**Md Mazharul Islam**  
Website: https://mazharul.odoo.com

## Support

For issues, questions, or contributions, please contact the author through the website above.

---

© 2025 Md Mazharul Islam. All rights reserved.