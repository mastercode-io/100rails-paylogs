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
                                       on_change=self.integration_selected)
        self.frequency = DropdownInput(name='frequency', label='Frequency',
                                       options=PAYRUN_FREQUENCY, value='Weekly',
                                       required=False)
        self.frequency_view = InlineMessage(label='Frequency',
                                            label_css='pl-form-field-label',
                                            content='Weekly',
                                            css_class='pl-message-field')
        self.pay_period_start_day = DropdownInput(name='pay_period_start_day', label='Pay Period Start Day',
                                                  options=WEEK_DAYS, value='Monday',
                                                  required=True)
        self.pay_period_end_day = DropdownInput(name='pay_period_end_day', label='Pay Period End Day',
                                                options=WEEK_DAYS, value='Sunday',
                                                required=True)
        self.pay_day = DropdownInput(name='pay_day', label='Pay Day',
                                     options=WEEK_DAYS, value='Friday')
        self.scopes = LookupInput(name='scopes', label='Scopes', model='Scope', select='multi',
                                  on_change=self.scope_selected)
        self.connection_button = Button(content='Create Connection', action=self.create_connection)
        self.message = InlineMessage(css_class='pl-message-bar')

        sections = [
            {
                'name': '_', 'cols': [
                    [
                        self.integration,
                        self.frequency,
                        self.frequency_view,
                        self.pay_period_start_day,
                        self.pay_period_end_day,
                        self.pay_day,
                        self.scopes,
                        self.message,
                        self.connection_button,
                    ],
                    [],
                    []
                ]
            }
        ]

        super().__init__(header='Payrun Settings',
                         sections=sections,
                         action='edit',
                         buttons_mode='off',
                         **kwargs)
        self.fullscreen = True
        app_list = AppIntegration.search(tenant_uid=SYSTEM_TENANT_UID)
        self.integration.data = app_list

        payrun_config = next(iter(PayrunConfig.search()), None)
        if payrun_config:
            self.data = payrun_config


    def form_open(self, args, **kwargs):
        super().form_open(args)
        self.connection_button.hide()
        self.frequency.hide()


    def integration_selected(self, args):
        if not args.get('value') or not self.integration.value:
            self.message.accent = None
            self.message.content = ''
            self.connection_button.hide()
        else:
            payroll_integration = AppIntegration.get(self.integration.value['uid'])
            payroll_connection = AppOutApiCredential.get_by('integration', payroll_integration)
            if not payroll_connection:
                self.message.accent = 'warning'
                self.message.content = (f"No connection found for this integration: "
                                        f"<b>{self.integration.value['name']}</b>")
                self.connection_button.show()

    def scope_selected(self, args):
        print('scope_selected', args)
        if self.frequency.visible:
            print('A')
            self.frequency.hide()
            self.frequency_view.show()
        else:
            print('B')
            self.frequency.show()
            self.frequency_view.hide()

    def create_connection(self, args):
        print('create_connection', args)
        self.message.accent = 'info'
        self.message.content = 'Creating connection...'
