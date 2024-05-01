from AnvilFusion.components.GridView import GridView
from AnvilFusion.components.FormInputs import Button, DropdownInput
from AnvilFusion.tools.utils import AppEnv
import anvil.js
import anvil.tables as tables
import anvil.tables.query as q
from ..app.models import Payrun, Timesheet, PayRateRule, PayRateTemplate, PayRateTemplateItem, Scope, ScopeType
from ..payroll.pay_awards import PayItemAward, PayLine
import datetime
import json


class TimesheetSubmittedView(GridView):
    def __init__(self, **kwargs):
        print('TimesheetSubmittedView')

        view_config = {
            'model': 'Timesheet',
            'columns': [
                {'name': 'payrun.payrun_week', 'label': 'Payrun Week'},
                {'name': 'employee.full_name', 'label': 'Employee Name'},
                {'name': 'job.name', 'label': 'Job Name'},
                {'name': 'job.job_type.short_code', 'label': 'Job Type'},
                {'name': 'date', 'label': 'Date', 'format': 'E dd MMM, yyyy'},
                {'name': 'start_time', 'label': 'Start Time', 'format': 'HH:mm'},
                {'name': 'end_time', 'label': 'End Time', 'format': 'HH:mm'},
                {'name': 'total_hours_view', 'label': 'Total Hours'},
                {'name': 'total_hours', 'visible': False},
                {'name': 'total_pay', 'label': 'Total Pay'},
                {'name': 'pay_lines', 'visible': False},
                {'name': 'pay_lines_view', 'label': 'Pay Lines', 'width': 300, 'disable_html_encode': False},
                {'name': 'status', 'label': 'Status'},
            ],
        }

        toolbar_actions = [
            # {
            #     'name': 'calculate_awards',
            #     'input': Button(
            #         content='CALC Awards',
            #         css_class='e-outline pl-grid-toolbar-action-button',
            #         action=self.calculate_awards_action,
            #     ),
            #     'selected_records': True,
            #     'toolbar_click': True,
            # },
            {
                'name': 'assign_payrun',
                'input': Button(
                    content='ASSIGN to Payrun',
                    css_class='e-outline pl-grid-toolbar-action-button',
                    action=self.assign_payrun_action,
                ),
                'selected_records': True,
                'toolbar_click': True,
            },
        ]

        context_menu_items = [
            {'id': 'assign_payrun', 'label': 'ASSIGN to Payrun', 'action': self.assign_payrun},
        ]

        super().__init__(
            model='Timesheet',
            title='Unassigned Timesheets',
            view_config=view_config,
            filters={'payrun': None},
            context_menu_items=context_menu_items,
            toolbar_actions=toolbar_actions,
            **kwargs)

        anvil.js.window['captionTimesheetListView'] = self.grouping_caption
        # anvil.js.window['timesheetListGroupingTotalHours'] = self.grouping_total_hours
        self.grid.allowGrouping = True
        self.grid.groupSettings = {
            'columns': ['employee__full_name'],
            'showDropArea': False,
            # 'captionTemplate': '<div>${key} - ${data}</div>',
            # 'captionTemplate': '<div>${captionTimesheetListView(data)}</div>',
        }
        self.grid.aggregates = [{
            'columns': [
                {
                    'type': 'Custom',
                    'field': 'total_hours_view',
                    'columnName': 'total_hours_view',
                    'groupCaptionTemplate': '${Custom}',
                    'customAggregate': self.grouping_total_hours,
                },
            ],
        }]
        self.grid.allowSorting = True
        self.grid.sortSettings = {
            'columns': [
                {'field': 'employee__full_name', 'direction': 'Ascending'},
                {'field': 'start_time', 'direction': 'Ascending'}
            ]
        }
        self.first_load = True

    def grouping_caption(self, args):
        # print('due_date_caption', args)
        # caption_color = 'color:#a63333;' if args['key'] == -100 else ''
        caption_color = 'color:#6750A4;'
        return (f'<div class="template" style="{caption_color}">'
                f'{args.items[0].employee__full_name}</div>')

    def grouping_total_hours(self, data, column):
        if isinstance(data, list):
            return
        week_total = sum(ts['total_hours'] for ts in data.items if ts['total_hours'])
        hours = int(week_total)
        minutes = int((week_total - hours) * 60)
        return f"{hours}:{minutes:02d} hrs per week"

    def query_cell_info(self, args):
        if 'field' in args.column.keys() and args.column['field'] == 'end_time':
            if args.data['start_time'] is not None and args.data['end_time'] is not None:
                # print(args.data['start_time'], args.data['end_time'])
                if isinstance(args.data['start_time'], str):
                    start_date = datetime.datetime.fromisoformat(args.data['start_time']).date()
                else:
                    start_date = datetime.datetime.fromtimestamp(args.data['start_time'].getTime() / 1000).date()
                if isinstance(args.data['end_time'], str):
                    end_date = datetime.datetime.fromisoformat(args.data['end_time']).date()
                else:
                    end_date = datetime.datetime.fromtimestamp(args.data['end_time'].getTime() / 1000).date()
                plus_days = (end_date - start_date).days
                if plus_days > 0:
                    args.cell.innerHTML = f'{args.cell.innerHTML} +{plus_days} day(s)'
        super().query_cell_info(args)

    def assign_payrun_action(self, args):
        if 'rowInfo' in args:
            timesheet_uids = [args['rowInfo']['rowData']['uid']]
        else:
            timesheet_uids = [rec['uid'] for rec in self.grid.getSelectedRecords()]
        print('assign_payrun_action', timesheet_uids)
        self.assign_payrun(timesheet_uids)

    def assign_payrun(self, timesheet_uids):
        print('assign_payrun', timesheet_uids)
        payrun = Payrun.get_by('name', 'Current Payrun')
        for ts_uid in timesheet_uids:
            ts = Timesheet.get(ts_uid)
            ts['payrun'] = payrun
            ts.save()
            self.update_grid(ts, False)
