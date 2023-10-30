from AnvilFusion.components.FormBase import FormBase, POPUP_WIDTH_COL2
from AnvilFusion.components.FormInputs import *
from AnvilFusion.components.MultiFieldInput import MultiFieldInput


TIME_SCOPE_OPTIONS = [
    'Weekday',
    'Weekend',
    'Saturday',
    'Sunday',
    'Public Holiday',
    'Week',
]
UNIT_TYPE_OPTIONS = [
    'Hours',
    'Days',
]
EARNINGS_TYPE_OPTIONS = [
    'Ordinary Earnings',
    'Overtime Earnings',
    'Lump Sum Earnings',
    'Allowance',
    'Deduction',
    'Leave',
]
PAY_RATE_TYPE_OPTIONS = [
    'Rate Per Unit',
    'Multiplier',
    'Fixed Amount'
]


class PayRateRuleForm(FormBase):
    def __init__(self, **kwargs):
        print('PayRateRuleForm')
        kwargs['model'] = 'PayRateRule'

        self.name = TextInput(name='name', label='Name')
        self.description = MultiLineInput(name='description', label='Description', rows=4)
        self.scope = LookupInput(name='scope', label='Scope', model='Scope')
        self.time_scope = DropdownInput(name='time_scope', label='Time Scope',
                                        options=TIME_SCOPE_OPTIONS, value='Weekday')
        self.time_limits = CheckboxInput(name='time_limits', label='Time Limits', value=True, on_change=self.toggle_time_limits)
        self.start_time = TimeInput(name='start_time', label='Start Time')
        self.end_time = TimeInput(name='end_time', label='End Time')
        self.max_time = NumberInput(name='max_time', label='Max Time')
        self.unit_type = DropdownInput(name='unit_type', label='Unit Type', options=UNIT_TYPE_OPTIONS, value='Hours')
        self.earnings_type = DropdownInput(name='earnings_type', label='Earnings Type',
                                           options=EARNINGS_TYPE_OPTIONS, value='Ordinary Earnings')
        self.pay_rate = NumberInput(name='pay_rate', label='Pay Rate')
        self.pay_rate_type = DropdownInput(name='pay_rate_type', label='Pay Rate Type',
                                           options=PAY_RATE_TYPE_OPTIONS, value='Rate Per Unit')
        self.pay_rate_multiplier = NumberInput(name='pay_rate_multiplier', label='Pay Rate Multiplier')
        self.pay_category = LookupInput(name='pay_category', label='Pay Category', model='PayCategory')
        self.status = RadioButtonInput(name='status', label='Status', options=['Active', 'Inactive'], value='Active')
        self.calculation_settings = MultiFieldInput(name='calculation_settings', label='Calculation Settings',
                                                    model='PayRateRule', cols=2)

        sections = [
            {
              'name': '_', 'cols': [
                [
                    self.name,
                    self.pay_category,
                    self.scope,
                    self.time_scope,
                ],
                [
                    self.description,
                    self.status,
                ],
            ]
            },
            {
                'name': '_', 'cols': [
                    [
                        self.earnings_type,
                        self.pay_rate_type,
                        self.unit_type,
                        self.pay_rate,
                        self.pay_rate_multiplier,
                    ],
                    [
                        self.time_limits,
                        self.start_time,
                        self.end_time,
                        self.max_time,
                    ],
                ]
            }
        ]

        super().__init__(sections=sections, width=POPUP_WIDTH_COL2, **kwargs)
        # self.fullscreen = True


    def form_open(self, args):
        super().form_open(args)
        self.toggle_time_limits(args)


    def toggle_time_limits(self, args):
        print('toggle_time_limits', args)
        if self.time_limits.value:
            self.start_time.show()
            self.end_time.show()
            self.max_time.show()
        else:
            self.start_time.hide()
            self.end_time.hide()
            self.max_time.hide()
