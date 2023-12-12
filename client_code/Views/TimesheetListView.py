from AnvilFusion.components.GridView import GridView
from AnvilFusion.tools.utils import AppEnv
import anvil.js
import anvil.tables as tables
import anvil.tables.query as q
from ..app.models import Employee, Timesheet, PayRateRule, PayRateTemplate, PayRateTemplateItem, Scope, ScopeType
from ..payroll.pay_awards import PayItemAward, PayLine
import datetime
import json


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
                {'name': 'pay_lines', 'visible': False},
                {'name': 'pay_lines_view', 'label': 'Pay Lines', 'width': 300, 'disable_html_encode': False},
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
        # print('\n\ngrouping_total_hours\n\n', data, column)
        if isinstance(data, list):
            return
        week_total = sum(day['total_hours'] for day in data.items)
        hours = int(week_total)
        minutes = int((week_total - hours) * 60)
        return f"{hours}:{minutes:02d} week"


    def calculate_awards(self, args):
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
            pay_item_list = [*PayRateTemplateItem.search(
                pay_rate_template=pay_rate_template,
                search_query=tables.order_by('order_number', ascending=True)
            )]
            unallocated_time = [(ts['start_time'], ts['end_time'])]
            ts_pay_lines = []
            total_pay = 0
            for pay_item in pay_item_list:
                if unallocated_time:
                    start_time, end_time = unallocated_time.pop(0)
                else:
                    start_time = end_time = None
                pay_line, unallocated_time = PayItemAward(pay_item).calculate_award(
                    date=ts['date'],
                    start_time=start_time,
                    end_time=end_time,
                    total_hours=ts['total_hours'],
                    employee_base_rate=employee['pay_rate'],
                )
                if pay_line:
                    ts_pay_lines.append(pay_line)
                    total_pay += pay_line.pay_amount
            if ts_pay_lines:
                week_pay_lines.extend(ts_pay_lines)
                ts['total_pay'] = total_pay
                ts['pay_lines'] = [str(pl) for pl in ts_pay_lines]
                ts.save()
                self.update_grid(ts, False)

            # ts_time_frames = [(ts['start_time'], ts['end_time'])]
            # ts_pay_lines = []
            # for pay_item in pay_rate_template_items:
            #     if pay_item['pay_rate_rule']['time_scope'] not in ts['day_type']:
            #         continue
            #     ts_time_frames, pay_lines = TimesheetListView.calculate_pay_lines(
            #         time_frames=ts_time_frames,
            #         pay_item=pay_item,
            #         employee=employee,
            #     )
            #     if pay_lines:
            #         ts_pay_lines.extend(pay_lines)
            #     if not ts_time_frames:
            #         break
            # if ts_pay_lines:
            #     week_pay_lines.extend(ts_pay_lines)
        etime = datetime.datetime.now()
        print('calc time', etime - stime)
        # print('pay_lines')
        # for pl in week_pay_lines:
        #     print(pl)


    @staticmethod
    def calculate_pay_lines(
        time_frames=None,
        pay_item=None,
        employee=None,
    ):
        pay_rule = pay_item['pay_rate_rule']
        rule_start_time = pay_rule['start_time'].time()
        rule_end_time = pay_rule['end_time'].time()
        max_hours = pay_rule['max_time'] or -1
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
            units = (do_end_time - do_start_time).total_seconds() / 3600
            if 0 <= max_hours < units:
                overtime_hours = units - max_hours
                units = max_hours
                unallocated_time_frames.append((do_end_time, end_time))
            elif max_hours != -1:
                max_hours -= units
            pay_rate = pay_item['pay_rate'] or employee['pay_rate']
            if pay_rule['pay_rate_type'] == 'Rate Per Unit':
                pay_amount = pay_rate * units
            elif pay_rule['pay_rate_type'] == 'Multiplier':
                pay_rate = pay_rate * pay_item['pay_rate_multiplier']
                pay_amount = pay_rate * units
            elif pay_rule['pay_rate_type'] == 'Fixed Amount':
                pay_amount = pay_item['pay_rate']
                units = 1
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
                    'units': units,
                    'pay_amount': pay_amount,
                }
                pay_lines.append(pay_line)
        return unallocated_time_frames, pay_lines


    @staticmethod
    def calculate_week_overtime(pay_lines=None, pay_items=None):
        for pay_item in pay_items:
            pay_rule = pay_item['pay_rule']
            if pay_rule['time_scope'] != 'Week':
                continue
            overtime_start = pay_rule['overtime_start']
            max_hours = pay_rule['max_hours'] or 0
            if not overtime_start or not max_hours:
                continue
            week_hours = 0
            overtime_hours = 0
            week_pay_lines = []
            for pl in pay_lines:
                if overtime_hours:
                    week_pay_lines.append(pl)
                    continue
                if pl['hours'] and  'earnings' in pay_rule['earnings_type'].lower():
                    week_hours += pl['hours']
                else:
                    week_pay_lines.append(pl)
                    continue
                if week_hours > overtime_start:
                    overtime_hours = week_hours - overtime_start
                    pl['hours'] -= overtime_hours
                    pl['pay_amount'] -= overtime_hours * pl['pay_rate']
                    week_pay_lines.append(pl)
                    if max_hours and overtime_hours > max_hours:
                        rule_hours = max_hours
                        overtime_hours -= max_hours
                    else:
                        rule_hours = overtime_hours
                    overtime_pl = {
                        'pay_rate_title': pay_item['pay_rate_title'],
                        'pay_category': pay_item['pay_category'],
                        'date': pl['date'],
                        'start_time': pl['end_time'],
                        'end_time': pl['end_time'] + datetime.timedelta(hours=overtime_hours),
                        'pay_rate': pl['pay_rate'],
                        'hours': rule_hours,
                        'pay_amount': rule_hours * pl['pay_rate'],
                    }
                    week_pay_lines.append(overtime_pl)
                    if overtime_hours:
                        pl_tail = pl.copy()
                        pl_tail['hours'] = overtime_hours
                        pl_tail['pay_amount'] = overtime_hours * pl['pay_rate']
                        pl_tail['start_time'] = pl['end_time'] + datetime.timedelta(hours=overtime_hours)
                        pl_tail['end_time'] = pl['end_time'] + datetime.timedelta(hours=overtime_hours)
                        week_pay_lines.append(pl_tail)
                else:
                    week_pay_lines.append(pl)
