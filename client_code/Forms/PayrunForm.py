from AnvilFusion.components.FormBase import FormBase, POPUP_WIDTH_COL3
from AnvilFusion.components.FormInputs import *
from AnvilFusion.components.SubformGrid import SubformGrid
from AnvilFusion.components.GridView import GRID_TOOLBAR_COMMAND_SEARCH, GRID_TOOLBAR_COMMAND_SEARCH_TOGGLE
from ..app.models import Payrun, PayrollConfig
import datetime


PAYRUN_STATUSES = [
    'Created',
    'Preview',
    'Approved',
    'Submitted',
    'Paid'
]


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
        self.status = DropdownInput(name='status', label='Status', options=PAYRUN_STATUSES, value='Created',
                                    enabled=False)
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
        self.show_payrun_items = CheckboxInput(name='show_payrun_items', label='Show Payrun Items',
                                               value=False, save=False)
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
                    [self.pay_period_start, self.pay_period_end, self.pay_date,
                     self.show_payrun_items],
                    [self.notes, self.status],
                ]
            },
            {
                'name': '_', 'rows': [
                    [self.payrun_items],
                ]
            }
        ]

        if kwargs.get('data') is None or kwargs['data']['uid'] is None:
            super().__init__(sections=sections,
                             width=POPUP_WIDTH_COL3,
                             header='Create Payrun',
                             button_save_label='Create',
                             **kwargs)
            self.create = True
        else:
            super().__init__(sections=sections,
                             header='View Payrun',
                             **kwargs)
            self.create = False

        # super().__init__(sections=sections, **kwargs)
        self.payrun_config = next(iter(PayrollConfig.search()), None)


    def form_open(self, args, **kwargs):
        if not self.payrun_config:
            self.message.message_type = 'e-warning'
            self.message.content = 'Payrun settings not configured'
            self.action = 'view'
        super().form_open(args, **kwargs)
        if self.action == 'add':
            self.show_payrun_items.hide()
            pay_period_dates = []
            today = datetime.datetime.today()
            current_monday = start_of_week = today - datetime.timedelta(days=today.weekday())
            last_monday = current_monday - datetime.timedelta(days=7)
        self.payrun_items.hide()

