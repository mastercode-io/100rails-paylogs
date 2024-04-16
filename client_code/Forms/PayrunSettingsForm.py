from AnvilFusion.components.FormBase import FormBase
from AnvilFusion.components.FormInputs import *
from ..app.models import PayrunConfig


PAYRUN_FREQUENCY = ['Weekly', 'Fortnightly', 'Monthly']
WEEK_DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']


class PayrunSettingsForm(FormBase):
    def __init__(self, **kwargs):
        print('PayrunSettingsForm')
        kwargs['model'] = 'PayrunConfig'

        self.integration = LookupInput(name='integration', label='Integration',
                                       model='AppIntegration',
                                       required=True,
                                       on_change=self.integration_selected)
        self.frequency = DropdownInput(name='type', label='Frequency',
                                       options=PAYRUN_FREQUENCY, value='Weekly',
                                       required=True)
        self.pay_period_start_day = DropdownInput(name='pay_period_start_day', label='Pay Period Start Day',
                                                  options=WEEK_DAYS, value='Monday',
                                                  required=True)
        self.pay_period_end_day = DropdownInput(name='pay_period_end_day', label='Pay Period End Day',
                                                options=WEEK_DAYS, value='Sunday',
                                                required=True)
        self.pay_day = DropdownInput(name='pay_day', label='Pay Day',
                                     options=WEEK_DAYS, value='Friday',
                                     required=True)
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

        super().__init__(header='Payrun Settings', sections=sections, **kwargs)
        self.fullscreen = True

        payrun_config = next(iter(PayrunConfig.search()))
        print('payrun_config', payrun_config)
        if payrun_config:
            self.data = payrun_config


    def integration_selected(self, args):
        print('integration_selected', args)
        if not args.get('value') or not self.integration.value:
            pass
        else:
            print('value', self.integration.value)
