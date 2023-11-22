from AnvilFusion.components.GridView import GridView
from AnvilFusion.tools.utils import AppEnv
import anvil.js


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
        self.grid.allowGrouping = True
        self.grid.groupSettings = {
            'columns': ['employee__full_name'],
            'showDropArea': False,
            # 'captionTemplate': '<div>${key} - ${data}</div>',
            'captionTemplate': '<div>${captionTimesheetListView(data)}</div>',
        }
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
        # return args['due_date']


    def calculate_awards(self, args):
        print('calculate_awards', args.rowData)
