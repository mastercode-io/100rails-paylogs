from AnvilFusion.components.FormBase import FormBase
from AnvilFusion.components.FormInputs import *
from ..app.models import PayrunConfig


PAYRUN_FREQUENCY = ['Weekly', 'Fortnightly', 'Monthly']
WEEK_DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']


class PayrunSettingsForm(FormBase):
    def __init__(self, **kwargs):
        print('PayrunSettingsForm')
        kwargs['model'] = 'PayrunConfig'

        self.integration = LookupInput(name='integration', label='Integration', model='AppIntegration')
        self.frequency = DropdownInput(name='type', label='Type', options=PAYRUN_FREQUENCY, value='Weekly')
        self.pay_period_start_day = DropdownInput(name='pay_period_start_day', label='Pay Period Start Day',
                                                  options=WEEK_DAYS, value='Monday')
        self.pay_period_end_day = DropdownInput(name='pay_period_end_day', label='Pay Period End Day',
                                                options=WEEK_DAYS, value='Sunday')
        self.pay_day = DropdownInput(name='pay_day', label='Pay Day', options=WEEK_DAYS, value='Friday')
        self.scopes = LookupInput(name='scopes', label='Scopes', model='Scope', select='multi')

        sections = [
            {
                'name': '_', 'cols': [
                    [
                        self.integration,
                        self.frequency,
                        self.pay_period_start_day,
                        self.pay_period_end_day,
                        self.pay_day,
                        self.scopes,
                    ],
                    [],
                    []
                ]
            }
        ]

        super().__init__(sections=sections, **kwargs)
        self.fullscreen = True

        payrun_config = next(PayrunConfig.search())
        print('payrun_config', payrun_config)
        if payrun_config:
            self.data = payrun_config
