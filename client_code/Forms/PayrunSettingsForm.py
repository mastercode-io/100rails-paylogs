from AnvilFusion.components.FormBase import FormBase
from AnvilFusion.components.FormInputs import *
from ..app.models import PayrunConfig, AppIntegration, AppOutApiCredential, SYSTEM_TENANT_UID


PAYRUN_FREQUENCY = ['Weekly', 'Fortnightly', 'Monthly']
WEEK_DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']


class PayrunSettingsForm(FormBase):
    def __init__(self, **kwargs):
        print('PayrunSettingsForm')
        kwargs['model'] = 'PayrunConfig'

        self.integration = LookupInput(name='integration', label='Integration',
                                       model='AppIntegration', get_data=False,
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
        self.message = InlineMessage()

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
        app_list = AppIntegration.search(tenant_uid=SYSTEM_TENANT_UID)
        print('integrations', app_list, len(app_list))
        # for app in app_list:
        #     print('app', app)
        self.integration.data = app_list

        payrun_config = next(iter(PayrunConfig.search()), None)
        print('payrun_config', payrun_config)
        if payrun_config:
            self.data = payrun_config


    def form_open(self, args, **kwargs):
        super().form_open(args)
        # self.info.hide()


    def integration_selected(self, args):
        print('integration_selected', args)
        if not args.get('value') or not self.integration.value:
            print('No integration selected')
            self.message.content = ''
        else:
            payroll_integration = AppIntegration.get(self.integration.value['uid'])
            print('payroll_integration', payroll_integration)
            payroll_connection = AppOutApiCredential.get_by('integration', payroll_integration)
            if not payroll_connection:
                self.message.content = 'No connection found for this integration'
