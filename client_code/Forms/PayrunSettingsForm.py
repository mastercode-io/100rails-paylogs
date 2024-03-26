from AnvilFusion.components.FormBase import FormBase
from AnvilFusion.components.FormInputs import *


PAYRUN_CONFIG_TYPE = ['Weekly', 'Fortnightly', 'Monthly']
WEEK_DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']


class PayrunSettingsForm(FormBase):
    def __init__(self, **kwargs):
        print('PayrunSettingsForm')
        kwargs['model'] = 'PayrunConfig'

        self.name = TextInput(name='name', label='Name')
        self.type = DropdownInput(name='type', label='Type', options=PAYRUN_CONFIG_TYPE, value='Weekly')
        self.pay_period_start_day = DropdownInput(name='pay_period_start_day', label='Pay Period Start Day',
                                                  options=WEEK_DAYS, value='Monday')
        self.pay_period_end_day = DropdownInput(name='pay_period_end_day', label='Pay Period End Day',
                                                options=WEEK_DAYS, value='Sunday')
        self.pay_day = DropdownInput(name='pay_day', label='Pay Day', options=WEEK_DAYS, value='Friday')
        self.scopes = LookupInput(name='scopes', label='Scopes', model='Scope', select='multi')

        fields = [
            self.name,
            self.type,
            self.pay_period_start_day,
            self.pay_period_end_day,
            self.pay_day,
            self.scopes,
        ]

        super().__init__(fields=fields, **kwargs)
        self.fullscreen = True
