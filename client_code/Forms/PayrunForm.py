from AnvilFusion.components.FormBase import FormBase
from AnvilFusion.components.FormInputs import *
from AnvilFusion.components.SubformGrid import SubformGrid
from AnvilFusion.components.GridView import GRID_TOOLBAR_COMMAND_SEARCH, GRID_TOOLBAR_COMMAND_SEARCH_TOGGLE
from ..app.models import Payrun, PayrunConfig
import datetime


class PayrunForm(FormBase):
    def __init__(self, **kwargs):
        print('PayrunForm')
        kwargs['model'] = 'Payrun'

        self.message = InlineMessage()
        self.select_pay_period = DropdownInput(name='select_pay_period', label='Select Pay Period',
                                               save=False
                                               )
        self.pay_period_start = DateInput(name='pay_period_start', label='Pay Period Start',
                                          enabled=False)
        self.pay_period_end = DateInput(name='pay_period_end', label='Pay Period End',
                                        enabled=False)
        self.pay_date = DateInput(name='pay_date', label='Pay Date')
        self.status = RadioButtonInput(name='status', label='Status', options=['Draft', 'Posted'], value='Draft')
        self.notes = MultiLineInput(name='notes', label='Notes', rows=4)

        payrun_items_view = {
            'model': 'PayrunItem',
            'columns': [
                {'name': 'employee.full_name', 'label': 'Employee'},
                {'name': 'timesheet.date', 'label': 'Timesheet Date'},
                {'name': 'pay_category.name', 'label': 'Category'},
                {'name': 'pay_rate', 'label': 'Rate'},
                {'name': 'units', 'label': 'Units'},
                {'name': 'amount', 'label': 'Amount'},
                {'name': 'status', 'label': 'Status'},
            ],
            'toolbar': [
                GRID_TOOLBAR_COMMAND_SEARCH,
                GRID_TOOLBAR_COMMAND_SEARCH_TOGGLE,
            ]
        }
        self.payrun_items = SubformGrid(name='payrun_items', label='Payrun Items', model='PayrunItem',
                                        link_model='PayRun', link_field='payrun',
                                        form_container_id=kwargs.get('target'),
                                        view_config=payrun_items_view,
                                        )

        sections = [
            {
                'name': '_', 'cols': [
                    [self.message],
                    []
                ]
            },
            {
                'name': '_', 'cols': [
                    [self.pay_period_start, self.pay_period_end, self.pay_date],
                    [self.notes, self.status],
                    [],
                ]
            },
            {
                'name': '_', 'rows': [
                    [self.payrun_items],
                ]
            }
        ]

        super().__init__(sections=sections, **kwargs)
        self.fullscreen = True
        if self.action == 'add':
            self.form.header = 'Create Payrun'
        self.payrun_config = next(iter(PayrunConfig.search()), None)
        if not self.payrun_config:
            self.action = 'view'
        else:
            pay_period_dates = []
            today= datetime.datetime.today()
            current_monday = start_of_week = today - datetime.timedelta(days=today.weekday())
            last_monday = current_monday - datetime.timedelta(days=7)


    def form_open(self, args, **kwargs):
        super().form_open(args, **kwargs)
        if not self.payrun_config:
            self.message.message_type = 'e-warning'
            self.message.content = 'Payrun settings not configured'
