from AnvilFusion.components.GridView import GridView
from AnvilFusion.tools.utils import AppEnv
import anvil.js
import anvil.tables as tables
import anvil.tables.query as q
from ..app.models import Employee, Timesheet, PayRateRule, PayRateTemplate, PayRateTemplateItem, Scope, ScopeType
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


    @staticmethod
    def calculate_awards(args):
        print('calculate_awards', args.rowInfo.rowData)
        ts = Timesheet.get(args.rowInfo.rowData['uid'])
        employee = ts['employee']
        ts_date = ts['date']
        start_of_week = ts_date - datetime.timedelta(days=ts_date.weekday())
        end_of_week = start_of_week + datetime.timedelta(days=6)
        print('week dates', start_of_week, end_of_week)
        stime = datetime.datetime.now()
        job_type_scopes = [*Scope.search(type=ScopeType.get_by('name', 'Job Type'))]
        # get start and end of week
        # get all timesheets for the week
        timesheets = [*Timesheet.search(
            date=q.all_of(q.greater_than_or_equal_to(start_of_week), q.less_than_or_equal_to(end_of_week)),
            employee=employee,
            search_query=tables.order_by('date', ascending=True)
        )]
        print('timesheets', len(timesheets))
        week_pay_lines = []
        for ts in timesheets:
            scope = next((s for s in job_type_scopes if s['short_code'] == ts['job']['job_type']['short_code']), None)
            pay_rate_template = PayRateTemplate.get_by('scope', scope)
            pay_rate_template_items = PayRateTemplateItem.search(
                pay_rate_template=pay_rate_template,
                search_query=tables.order_by('order_number', ascending=True)
            )
            ts_time_frames = [(ts['start_time'], ts['end_time'])]
            ts_pay_lines = []
            for pay_item in pay_rate_template_items:
                if pay_item['pay_rate_rule']['time_scope'] not in ts['day_type']:
                    continue
                ts_time_frames, pay_lines = TimesheetListView.calculate_pay_lines(
                    time_frames=ts_time_frames,
                    pay_item=pay_item,
                    employee=employee,
                )
                if pay_lines:
                    ts_pay_lines.extend(pay_lines)
                if not ts_time_frames:
                    break
            if ts_pay_lines:
                week_pay_lines.extend(ts_pay_lines)
        etime = datetime.datetime.now()
        print('calc time', etime - stime)
        print('pay_lines')
        for pl in week_pay_lines:
            print(pl)


    @staticmethod
    def calculate_pay_lines(
        time_frames=None,
        pay_item=None,
        employee=None,
    ):
        pay_rule = pay_item['pay_rate_rule']
        rule_start_time = pay_rule['start_time'].time()
        rule_end_time = pay_rule['end_time'].time()
        overtime_limit = pay_rule['overtime_limit'] or -1
        unallocated_time_frames = []
        pay_lines = []
        for frame in time_frames:
            start_time, end_time = frame
            if end_time.time() <= rule_start_time or start_time.time() >= rule_end_time:
                unallocated_time_frames.append(frame)
                continue
            if start_time.time() < rule_start_time:
                unallocated_time_frames.append((start_time, datetime.datetime.combine(start_time.date(), rule_start_time)))
                do_start_time = datetime.datetime.combine(start_time.date(), rule_start_time)
            else:
                do_start_time = start_time
            if end_time.time() > rule_end_time:
                unallocated_time_frames.append((datetime.datetime.combine(end_time.date(), rule_end_time), end_time))
                do_end_time = datetime.datetime.combine(end_time.date(), rule_end_time)
            else:
                do_end_time = end_time
            do_hours = (do_end_time - do_start_time).total_seconds() / 3600
            if 0 <= overtime_limit < do_hours:
                overtime_hours = do_hours - overtime_limit
                do_hours = overtime_limit
                unallocated_time_frames.append((do_end_time, end_time))
            elif overtime_limit != -1:
                overtime_limit -= do_hours
            pay_rate = pay_item['pay_rate'] or employee['pay_rate'] or pay_rule['pay_rate']
            if pay_rule['pay_rate_type'] == 'Rate Per Unit':
                pay_amount = pay_rate * do_hours
            elif pay_rule['pay_rate_type'] == 'Multiplier':
                pay_rate = pay_rate * (pay_item['pay_rate_multiplier'] or pay_rule['pay_rate_multiplier'])
                pay_amount = pay_rate * do_hours
            elif pay_rule['pay_rate_type'] == 'Fixed Amount':
                pay_amount = pay_item['pay_rate'] or pay_rule['pay_rate']
            else:
                pay_amount = 0
            if pay_amount:
                pay_line = {
                    'pay_rate_title': pay_item['pay_rate_title'],
                    'pay_category': pay_item['pay_category'],
                    'date': do_start_time.date(),
                    'start_time': do_start_time,
                    'end_time': do_end_time,
                    'pay_rate': pay_rate,
                    'hours': do_hours,
                    'pay_amount': pay_amount,
                }
                pay_lines.append(pay_line)
        return unallocated_time_frames, pay_lines
