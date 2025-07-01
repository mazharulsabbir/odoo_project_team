# Project Team Rules - User Manual

**Module Version:** 16.0.1.0.0  
**Author:** Md Mazharul Islam  
**Date:** January 2025

---

## Table of Contents

1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Managing Project Teams](#managing-project-teams)
4. [Configuring Projects with Teams](#configuring-projects-with-teams)
5. [Working with Tasks](#working-with-tasks)
6. [Using the Task Dashboard](#using-the-task-dashboard)
7. [User Roles and Permissions](#user-roles-and-permissions)
8. [Frequently Asked Questions](#frequently-asked-questions)
9. [Troubleshooting](#troubleshooting)
10. [Contact Support](#contact-support)

---

## 1. Introduction

The Project Team Rules module enhances Odoo's project management by introducing team-based access control. This manual will guide you through using all features of the module effectively.

### Key Benefits:
- **Enhanced Security**: Control project visibility based on team membership
- **Organized Workflow**: Assign projects to specific teams
- **Better Collaboration**: Team members work together on shared projects
- **Comprehensive Analytics**: Track team performance with the task dashboard

---

## 2. Getting Started

### Prerequisites
Before using this module, ensure:
- You have appropriate user permissions (Project User or Project Manager)
- The module is properly installed by your system administrator
- You understand basic Odoo project management concepts

### Module Access Points
The module adds features in two main areas:
1. **Project Configuration**: Team management
2. **Project Reporting**: Task dashboard (Project Managers only)

---

## 3. Managing Project Teams

### Accessing Project Teams
Navigate to: **Project → Configuration → Project Teams**

### Creating a New Team

1. Click the **"New"** button
2. Fill in the required information:
   - **Team Name**: Enter a descriptive name (e.g., "Development Team", "Marketing Team")
   - **Team Members**: Click "Add a line" and select internal users
3. Click **"Save"**

![Team Creation Tip]
> 💡 **Tip**: Only internal users (non-portal users) can be added as team members. Portal users should be managed through different access methods.

### Editing Existing Teams

1. Click on any team name from the list
2. Modify team details as needed:
   - Add new members by clicking "Add a line"
   - Remove members by clicking the trash icon
   - Update the team name
3. Click **"Save"** to apply changes

### Archiving Teams

To deactivate a team without deleting it:
1. Open the team form
2. Click **Action → Archive**
3. The team will be hidden from active lists but can be restored later

---

## 4. Configuring Projects with Teams

### Understanding Privacy Visibility

The module adds a new privacy option: **"Assigned Team Only"**

Privacy options include:
- **Followers**: Only followers can see the project
- **All Internal Users**: All employees can see the project
- **Assigned Team Only**: Only team members can see the project (NEW)

### Assigning Teams to Projects

1. Navigate to **Project → Projects**
2. Open a project or create a new one
3. In the project form:
   - Set **Privacy Visibility** to "Assigned Team Only"
   - The **Project Team** field will become visible and required
   - Select the appropriate team from the dropdown
4. Click **"Save"**

![Important Note]
> ⚠️ **Important**: The Project Team field is only required when Privacy Visibility is set to "Assigned Team Only". For other privacy modes, team assignment is optional.

### Changing Project Teams

1. Open the project form
2. Change the team selection in the Project Team field
3. Save the project
4. Team members will automatically gain/lose access based on the change

---

## 5. Working with Tasks

### Task Assignment Rules

When a project has "Assigned Team Only" privacy:
- **Assignees must be team members**: The system restricts task assignment to team members only
- **Automatic validation**: If you change a task's project, invalid assignees are automatically removed
- **Smart filtering**: The assignee dropdown only shows valid team members

### Creating Tasks with Team Restrictions

1. Navigate to a project with team-based privacy
2. Click **"Create"** to add a new task
3. In the task form:
   - The **Assignees** field will only show team members
   - Select one or more team members
4. Complete other task details and save

### Managing Task Assignments

If a project's team changes:
1. Tasks automatically update their assignee restrictions
2. Previously assigned users who are not in the new team are removed
3. You'll need to reassign tasks to new team members if needed

---

## 6. Using the Task Dashboard

> 📌 **Access Required**: This feature is only available to users with Project Manager permissions.

### Accessing the Dashboard
Navigate to: **Project → Reporting → Task Dashboard**

### Dashboard Components

#### 1. Filter Controls (Centered at top)

**Time Period Filter:**
- All Time (default)
- This Week
- Previous Week
- This Month
- Previous Month

**User Filter:**
- All Users (default)
- Individual team members

#### 2. Statistics Cards

The dashboard displays dynamic statistics based on your actual project stages:
- **Total Tasks**: Click to view the complete task list
- **Stage-based Cards**: Automatically shows cards for each stage in your projects
  - Cards are color-coded: Green for Done/Completed, Yellow for In Progress/Doing, Blue for others
  - Adapts to your workflow - no fixed statuses
  - Shows real-time count for each stage

#### 3. Assignee Performance Table

View detailed statistics per user:
- **User name**: All active team members are listed
- **Total Tasks**: Shows the total number of tasks assigned to each user
- **Task Status**: Displays stage-wise breakdown as colored pills
  - Example: "To Do: 5" (blue), "In Progress: 3" (yellow), "Done: 2" (green)
  - Pills are color-coded to match the stage cards above
  - Users with no tasks show "No tasks"
- **"View Tasks"** button - Opens filtered task list for that user

### Using Dashboard Filters

1. **Time-based Analysis:**
   - Click the time period dropdown
   - Select desired period
   - All statistics update automatically

2. **User-specific Analysis:**
   - Click the user filter dropdown
   - Select a specific user or "All Users"
   - View personalized statistics

3. **Combined Filtering:**
   - Use both filters together
   - Example: View John's tasks for this month

### Viewing Detailed Task Lists

1. Click on any statistic card to see all related tasks
2. Click "View Tasks" next to any user to see their specific tasks
3. The task list respects current filter selections

---

## 7. User Roles and Permissions

### Project User
- Can view projects where they are team members
- Can be assigned to tasks within their team's projects
- Cannot access the task dashboard
- Can manage their own tasks

### Project Manager
- Full access to all projects and teams
- Can create and manage teams
- Access to task dashboard with all statistics
- Can override team restrictions

### Access Rules Summary

| Feature | Project User | Project Manager |
|---------|-------------|-----------------|
| View team projects | ✓ (if member) | ✓ (all) |
| Create teams | ✗ | ✓ |
| Task dashboard | ✗ | ✓ |
| Assign tasks | ✓ (team members only) | ✓ (anyone) |

---

## 8. Frequently Asked Questions

**Q: Why can't I see a project that I know exists?**
A: Check if the project's privacy is set to "Assigned Team Only" and verify you're a member of the assigned team.

**Q: Why is the Project Team field not showing?**
A: The Project Team field only appears when Privacy Visibility is set to "Assigned Team Only".

**Q: Can I assign tasks to users outside the team?**
A: No, when a project uses team-based privacy, only team members can be assigned to tasks.

**Q: Why can't I access the Task Dashboard?**
A: The Task Dashboard is restricted to users with Project Manager permissions.

**Q: What happens to tasks when I change a project's team?**
A: Task assignees who are not members of the new team are automatically removed. You'll need to reassign these tasks.

**Q: Can one person be in multiple teams?**
A: Yes, users can be members of multiple teams and will have access to all associated projects.

---

## 9. Troubleshooting

### Common Issues and Solutions

**Issue: Cannot create a team**
- **Solution**: Verify you have Project Manager permissions

**Issue: Team member cannot see project**
- **Check**: Project privacy is set to "Assigned Team Only"
- **Check**: User is actually added to the team
- **Check**: User has Project User permissions

**Issue: Cannot assign task to a user**
- **Check**: User is a member of the project's team
- **Check**: Project privacy settings
- **Try**: Refresh the page to update the assignee list

**Issue: Dashboard shows incorrect statistics**
- **Try**: Clear browser cache and reload
- **Check**: Filter settings are correct
- **Verify**: User permissions haven't changed

**Issue: Project Team field is required but empty**
- **Solution**: Create a team first, then assign it to the project
- **Check**: Teams exist in the system

---

## 10. Contact Support

For additional assistance or to report issues:

**Author**: Md Mazharul Islam  
**Website**: https://mazharul.odoo.com  
**Module Version**: 16.0.1.0.0  

When contacting support, please provide:
- Your Odoo version
- Module version
- Description of the issue
- Steps to reproduce the problem
- Screenshots if applicable

---

## Quick Reference Card

### Navigation Shortcuts
- **Teams**: Project → Configuration → Project Teams
- **Dashboard**: Project → Reporting → Task Dashboard
- **Projects**: Project → Projects

### Key Features at a Glance
- ✓ Team-based project visibility
- ✓ Restricted task assignments
- ✓ Comprehensive task analytics
- ✓ Time and user filtering
- ✓ Performance tracking

---

*This user manual is part of the Project Team Rules module for Odoo 16. Keep this document for reference and training purposes.*

© 2025 Md Mazharul Islam. All rights reserved.