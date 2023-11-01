from AnvilFusion.components.FormBase import FormBase
from AnvilFusion.components.FormInputs import *
from AnvilFusion.components.SubformGrid import SubformGrid


class PayrunForm(FormBase):
    def __init__(self, **kwargs):
        print('PayrunForm')
        kwargs['model'] = 'Payrun'

        self.pay_period_start = DateInput(name='pay_period_start', label='Pay Period Start')
        self.pay_period_end = DateInput(name='pay_period_end', label='Pay Period End')
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
        }
        self.payrun_items = SubformGrid(name='payrun_items', label='Payrun Items', model='PayrunItem',
                                        link_model='PayRun', link_field='pay_run',
                                        form_container_id=kwargs.get('target'),
                                        view_config=payrun_items_view,
                                        )

        sections = [
            {
                'name': '_', 'cols': [
                    [self.pay_period_start, self.pay_period_end, self.pay_date],
                    [self.notes, self.status],
                ]
            },
            {
                'name': '_', 'rows': [
                    [self.payrun_items],
                ]
            }
        ]

        super().__init__(sections=sections, **kwargs)
        # self.fullscreen = True
