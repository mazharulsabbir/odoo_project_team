# Project Team Rules

A comprehensive Odoo 16 module for managing project teams and implementing team-based access control with an advanced task dashboard.

## Overview

The Project Team Rules module enhances Odoo's project management capabilities by introducing team-based project visibility and a powerful task analytics dashboard. Projects are restricted to team members only, ensuring data security and proper access control.

## Features

### 1. Team Management
- Create and manage project teams with multiple members
- Assign teams to projects for access control
- Only team members can view and access their assigned projects

### 2. Team-Based Security
- Projects are visible only to assigned team members
- Tasks are visible to team members, assignees, and project managers
- Automatic access control based on team membership

### 3. Task Dashboard
- Real-time task statistics with visual cards
- Time-based filtering (All Time, This Week, Previous Week, This Month, Previous Month)
- User-based filtering to view specific assignee's tasks
- Interactive assignee table with quick task viewing

### 4. Task Assignment Restrictions
- Task assignees can only be selected from project team members
- Automatic validation when changing projects
- Domain restrictions on user selection fields

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

- **Dashboard Features:**
  - **Filter Controls:**
    - Time Period Dropdown: All Time, This Week, Previous Week, This Month, Previous Month
    - User Filter Dropdown: All Users or specific team members
  
  - **Statistics Cards:**
    - Total Tasks (clickable to view task list)
    - Done Tasks
    - In Progress Tasks
    - To Do Tasks
  
  - **Assignee Table:**
    - Shows all team members with task counts
    - "View Tasks" button to see specific user's tasks

## Usage Guide

### Creating a Project Team

1. Navigate to Project → Configuration → Project Teams
2. Click "New" to create a team
3. Enter team name
4. Add team members (only internal users)
5. Save the team

### Assigning Teams to Projects

1. Open any project in form view
2. Find the "Project Team" field (below Project Manager)
3. Select the appropriate team
4. Save the project

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

1. **Projects:** Visible only to team members and project managers
2. **Tasks:** Visible to:
   - Team members of the project
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