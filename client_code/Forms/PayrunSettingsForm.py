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
        self.frequency = DropdownInput(name='frequency', label='Frequency',
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
        self.connection_button = Button(content='Create Connection', action=self.create_connection)
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
                        self.connection_button,
                        self.message,
                    ],
                    [],
                    []
                ]
            }
        ]

        super().__init__(header='Payrun Settings', sections=sections, **kwargs)
        self.fullscreen = True
        app_list = AppIntegration.search(tenant_uid=SYSTEM_TENANT_UID)
        self.integration.data = app_list

        payrun_config = next(iter(PayrunConfig.search()), None)
        if payrun_config:
            self.data = payrun_config


    def form_open(self, args, **kwargs):
        super().form_open(args)
        self.connection_button.hide()


    def integration_selected(self, args):
        if not args.get('value') or not self.integration.value:
            self.message.message_type = ''
            self.message.content = ''
        else:
            payroll_integration = AppIntegration.get(self.integration.value['uid'])
            payroll_connection = AppOutApiCredential.get_by('integration', payroll_integration)
            if not payroll_connection:
                self.message.message_type = 'e-warning'
                self.message.content = (f"No connection found for this integration: "
                                        f"<b>{self.integration.value['name']}</b>")
                self.connection_button.show()


    def create_connection(self, args):
        print('create_connection', args)
        self.message.message_type = 'e-info'
        self.message.content = 'Creating connection...'
