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

## Technical Details

### Models

1. **project.team**
   - Stores team information and members
   - Many2many relationship with users

2. **project.project** (inherited)
   - Added team_id field
   - Automatic follower management

3. **project.task** (inherited)
   - Domain restrictions on user_ids field
   - Automatic assignee validation

4. **project.task.dashboard**
   - SQL view for performance
   - Real-time statistics calculation

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