from AnvilFusion.components.GridView import GridView
from AnvilFusion.tools.utils import AppEnv
import anvil.js
import anvil.tables as tables
import anvil.tables.query as q
from ..app.models import Employee, Timesheet, PayRateRule
import datetime


class TimesheetListView(GridView):
    def __init__(self, **kwargs):
        print('TimesheetListView')

        view_config = {
            'model': 'Timesheet',
            'columns': [
                {'name': 'employee.full_name', 'label': 'Employee Name'},
                {'name': 'date', 'label': 'Date'},
                {'name': 'start_time', 'label': 'Start Time', 'format': 'HH:mm'},
                {'name': 'end_time', 'label': 'End Time', 'format': 'HH:mm'},
                {'name': 'total_hours_view', 'label': 'Total Hours'},
                {'name': 'total_hours', 'visible': False},
                {'name': 'total_pay', 'label': 'Total Pay'},
                {'name': 'status', 'label': 'Status'},
                {'name': 'job.name', 'label': 'Job Name'},
                {'name': 'timesheet_type.short_code', 'label': 'Time Type'},
            ],
        }

        context_menu_items = [
            {'id': 'calculate_awards', 'label': 'Calculate Pay Awards', 'action': self.calculate_awards},
        ]

        super().__init__(
            model='Timesheet',
            view_config=view_config,
            context_menu_items=context_menu_items,
            **kwargs)

        anvil.js.window['captionTimesheetListView'] = self.grouping_caption
        anvil.js.window['timesheetListGroupingTotalHours'] = self.grouping_total_hours
        self.grid.allowGrouping = True
        self.grid.groupSettings = {
            'columns': ['employee__full_name'],
            'showDropArea': False,
            # 'captionTemplate': '<div>${key} - ${data}</div>',
            'captionTemplate': '<div>${captionTimesheetListView(data)}</div>',
        }
        self.grid.aggregates = [{
            'columns': [
                {
                    'type': 'Custom',
                    'field': 'total_hours_view',
                    'columnName': 'total_hours_view',
                    'groupCaptionTemplate': '${Custom}',
                    # 'customAggregate': 'timesheetListGroupingTotalHours',
                    'customAggregate': self.grouping_total_hours,
                    # 'customAggregate': anvil.js.window['timesheetListGroupingTotalHours'],
                },
            ],
        }]
        self.grid.allowSorting = True
        self.grid.sortSettings = {
            'columns': [
                {'field': 'employee__full_name', 'direction': 'Ascending'},
                {'field': 'date', 'direction': 'Ascending'}
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
        # print('grouping_total_hours', data, column)
        week_total = sum(day['total_hours'] for day in data.items)
        hours = int(week_total)
        minutes = int((week_total - hours) * 60)
        return f"{hours}:{minutes:02d} week"


    def calculate_awards(self, args):
        print('calculate_awards', args.rowInfo.rowData)
        ts = Timesheet.get(args.rowInfo.rowData['uid'])
        ts_date = ts['date']
        employee = ts['employee']
        # get start and end of week
        start_of_week = ts_date - datetime.timedelta(days=ts_date.weekday())
        end_of_week = start_of_week + datetime.timedelta(days=6)
        print('week dates', start_of_week, end_of_week)
        # get all timesheets for the week
        timesheets = Timesheet.search(
            date=q.all_of(q.greater_than_or_equal_to(start_of_week), q.less_than_or_equal_to(end_of_week)),
            employee=employee,
            search_query=tables.order_by('date', ascending=True)
        )
        print('timesheets', [t['date'] for t in timesheets])
        # pay_lines = []
        # for ts in timesheets:
        #     pay_rate_rules =- PayRateRule.search(
        #         time_scope=q.any_of(*ts.day_type()),
        #         search_query=tables.order_by('start_time', ascending=True)
        #     )
        #
        #     pay_lines.extend(ts.calculate_pay_lines())
        # rules = PayRateRule.search()

