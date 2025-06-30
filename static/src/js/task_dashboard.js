/** @odoo-module **/

import {registry} from "@web/core/registry";
import {useService} from "@web/core/utils/hooks";
import {Component, useState, onWillStart} from "@odoo/owl";

class TaskDashboard extends Component {
    setup() {
        this.rpc = useService("rpc");
        this.action = useService("action");

        this.state = useState({
            period: 'all',
            selectedUserId: false,
            selectedUserName: 'All Users',
            stats: {
                total_tasks: 0,
                done_tasks: 0,
                in_progress_tasks: 0,
                todo_tasks: 0,
                assignees: []
            }
        });

        onWillStart(async () => {
            await this.loadStatistics();
        });
    }

    async loadStatistics(period = null, assignee_id = null) {
        // Use current state values if not provided
        period = period !== null ? period : this.state.period;
        assignee_id = assignee_id !== null ? assignee_id : this.state.selectedUserId;

        const result = await this.rpc("/web/dataset/call_kw/project.task.dashboard/get_task_statistics", {
            model: "project.task.dashboard",
            method: "get_task_statistics",
            args: [period, assignee_id],
            kwargs: {}
        });

        this.state.stats = result;
        this.state.period = period;
        if (assignee_id !== null) {
            this.state.selectedUserId = assignee_id;
        }
    }

    async onPeriodClick(period) {
        await this.loadStatistics(period, this.state.selectedUserId);
    }

    async onUserFilterClick(userId, userName) {
        this.state.selectedUserId = userId;
        this.state.selectedUserName = userName;
        await this.loadStatistics(this.state.period, userId);
    }

    async onAssigneeClick(assignee_id) {
        const assignee = this.state.stats.assignees.find(a => a.id === assignee_id);
        if (assignee) {
            await this.onUserFilterClick(assignee_id, assignee.name);
        }
    }

    viewUserTasks(userId) {
        const domain = this._getDomain();
        // Add specific user filter
        domain.push(['user_ids', 'in', userId]);

        this.action.doAction({
            type: 'ir.actions.act_window',
            name: 'Tasks',
            res_model: 'project.task',
            view_mode: 'tree,form,kanban,calendar,pivot,graph',
            views: [[false, 'tree'], [false, 'form'], [false, 'kanban'], [false, 'calendar'], [false, 'pivot'], [false, 'graph']],
            domain: domain,
            context: {
                'create': false,
            },
        });
    }

    openTasks() {
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: 'Tasks',
            res_model: 'project.task',
            view_mode: 'tree,form',
            views: [[false, 'tree'], [false, 'form']],
            domain: this._getDomain(),
            context: {},
        });
    }

    _getDomain() {
        const domain = [];
        const today = new Date();

        switch (this.state.period) {
            case 'this_week':
                const weekStart = new Date(today);
                weekStart.setDate(today.getDate() - today.getDay());
                domain.push(['create_date', '>=', weekStart.toISOString().split('T')[0]]);
                break;
            case 'prev_week':
                const prevWeekEnd = new Date(today);
                prevWeekEnd.setDate(today.getDate() - today.getDay());
                const prevWeekStart = new Date(prevWeekEnd);
                prevWeekStart.setDate(prevWeekEnd.getDate() - 7);
                domain.push(['create_date', '>=', prevWeekStart.toISOString().split('T')[0]]);
                domain.push(['create_date', '<', prevWeekEnd.toISOString().split('T')[0]]);
                break;
            case 'this_month':
                const monthStart = new Date(today.getFullYear(), today.getMonth(), 1);
                domain.push(['create_date', '>=', monthStart.toISOString().split('T')[0]]);
                break;
            case 'prev_month':
                const prevMonthEnd = new Date(today.getFullYear(), today.getMonth(), 1);
                const prevMonthStart = new Date(today.getFullYear(), today.getMonth() - 1, 1);
                domain.push(['create_date', '>=', prevMonthStart.toISOString().split('T')[0]]);
                domain.push(['create_date', '<', prevMonthEnd.toISOString().split('T')[0]]);
                break;
        }

        // Add user filter to domain
        if (this.state.selectedUserId) {
            domain.push(['user_ids', 'in', this.state.selectedUserId]);
        }

        return domain;
    }
}

TaskDashboard.template = "project_team_rules.TaskDashboard";

registry.category("actions").add("project_task_dashboard", TaskDashboard);