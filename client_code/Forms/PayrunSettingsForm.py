from AnvilFusion.components.FormBase import FormBase
from AnvilFusion.components.FormInputs import *
from ..app.models import PayrunConfig, AppIntegration, AppOutApiCredential, SYSTEM_TENANT_UID

PAYRUN_FREQUENCY = ['Weekly', 'Fortnightly', 'Monthly']
WEEK_DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']


class PayrunSettingsForm(FormBase):
    def __init__(self, **kwargs):
        print('PayrunSettingsForm')
        kwargs['model'] = 'PayrunConfig'

        # Edit mode fields
        self.integration = LookupInput(name='integration', label='Integration',
                                       model='AppIntegration', get_data=False,
                                       on_change=self.integration_selected)
        self.frequency = DropdownInput(name='frequency', label='Frequency',
                                       options=PAYRUN_FREQUENCY, value='Weekly',
                                       required=False)
        self.pay_period_start_day = DropdownInput(name='pay_period_start_day', label='Pay Period Start Day',
                                                  options=WEEK_DAYS, value='Monday',
                                                  required=True)
        self.pay_period_end_day = DropdownInput(name='pay_period_end_day', label='Pay Period End Day',
                                                options=WEEK_DAYS, value='Sunday',
                                                required=True)
        self.pay_day = DropdownInput(name='pay_day', label='Pay Day',
                                     options=WEEK_DAYS, value='Friday')
        self.scopes = LookupInput(name='scopes', label='Scopes', model='Scope', select='multi')
        self.connection_button = Button(content='Create Connection', action=self.create_connection)
        self.message = InlineMessage(css_class='pl-message-bar')

        # View mode fields
        self.view_integration = InlineMessage(label='Integration',
                                              label_css='pl-form-field-label',
                                              css_class='pl-message')
        self.view_frequency = InlineMessage(label='Frequency',
                                            label_css='pl-form-field-label',
                                            css_class='pl-message-field')
        self.view_pay_period_start_day = InlineMessage(label='Pay Period Start Day',
                                                       label_css='pl-form-field-label',
                                                       css_class='pl-message-field')
        self.view_pay_period_end_day = InlineMessage(label='Pay Period End Day',
                                                     label_css='pl-form-field-label',
                                                     css_class='pl-message-field')
        self.view_pay_day = InlineMessage(label='Pay Day',
                                          label_css='pl-form-field-label',
                                          css_class='pl-message-field')

        sections = [
            {
                'name': '_', 'cols': [
                    [
                        self.integration,
                        self.frequency,
                        self.pay_period_start_day,
                        self.pay_period_end_day,
                        self.pay_day,

                        self.view_integration,
                        self.view_frequency,
                        self.view_pay_period_start_day,
                        self.view_pay_period_end_day,
                        self.view_pay_day,
                    ],
                    [],
                    []
                ]
            },
            {
                'name': '_', 'cols': [
                    [
                        self.message,
                        self.connection_button,
                    ],
                    [],
                    []
                ]
            }
        ]

        app_list = AppIntegration.search(tenant_uid=SYSTEM_TENANT_UID)
        self.integration.data = app_list
        payrun_config = next(iter(PayrunConfig.search()), None)
        if payrun_config:
            self.data = payrun_config
            self.action = 'view'
        else:
            self.action = 'edit'

        super().__init__(header='Payrun Settings',
                         sections=sections,
                         action='edit',
                         buttons_mode='off',
                         **kwargs)
        self.fullscreen = True

    def form_open(self, args, **kwargs):
        super().form_open(args)
        self.connection_button.hide()
        self.form_mode(self.action)

    def form_mode(self, action):
        if action == 'view':

            self.view_integration.content = self.integration.value['name']
            self.integration.hide()
            self.view_integration.show()

            self.view_frequency.content = self.frequency.value
            self.frequency.hide()
            self.view_frequency.show()

            self.view_pay_period_start_day.content = self.pay_period_start_day.value
            self.pay_period_start_day.hide()
            self.view_pay_period_start_day.show()

            self.view_pay_period_end_day.content = self.pay_period_end_day.value
            self.pay_period_end_day.hide()
            self.view_pay_period_end_day.show()

            self.view_pay_day.content = self.pay_day.value
            self.pay_day.hide()
            self.view_pay_day.show()

        else:
            self.view_integration.hide()
            self.view_frequency.hide()
            self.view_pay_period_start_day.hide()
            self.view_pay_period_end_day.hide()
            self.view_pay_day.hide()

            self.integration.show()
            self.frequency.show()
            self.pay_period_start_day.show()
            self.pay_period_end_day.show()
            self.pay_day.show()

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

    def create_connection(self, args):
        print('create_connection', args)
        self.message.accent = 'info'
        self.message.content = 'Creating connection...'
