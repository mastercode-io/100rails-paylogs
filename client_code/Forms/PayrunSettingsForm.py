from AnvilFusion.components.FormBase import FormBase
from AnvilFusion.components.FormInputs import *
from AnvilFusion.components.MultiFieldInput import MultiFieldInput
from ..app.models import PayrunConfig, AppIntegration, AppOutApiCredential, SYSTEM_TENANT_UID
from ..Pages.widgets import StepperWidget

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
        self.pay_period_start_day = DropdownInput(name='pay_period_start_day', label='Pay Period Start Day',
                                                  options=WEEK_DAYS, value='Monday',
                                                  required=True)
        self.pay_period_end_day = DropdownInput(name='pay_period_end_day', label='Pay Period End Day',
                                                options=WEEK_DAYS, value='Sunday',
                                                required=True)
        self.pay_day = DropdownInput(name='pay_day', label='Pay Day',
                                     options=WEEK_DAYS, value='Friday')
        self.payrun_initial_date = DateInput(name='payrun_initial_date', label='Initial Payrun Date')
        self.message = InlineMessage(css_class='pl-message-bar')

        self.payrun_flow_steps_schema = [
            CheckboxInput(name='created', label='Created', value=True, enabled=False,
                          on_change=self.payrun_flow_changed),
            CheckboxInput(name='ts_entered', label='Timesheets Entered', value=False, enabled=True,
                          on_change=self.payrun_flow_changed),
            CheckboxInput(name='ts_approve3d', label='Timesheets Approved', value=False, enabled=True,
                          on_change=self.payrun_flow_changed),
            CheckboxInput(name='review', label='Review', value=False, enabled=True,
                          on_change=self.payrun_flow_changed),
            CheckboxInput(name='pay_calculated', label='Pay Calculated', value=False, enabled=True,
                          on_change=self.payrun_flow_changed),
            CheckboxInput(name='pay_approved', label='Pay Approved', value=False, enabled=True,
                          on_change=self.payrun_flow_changed),
            CheckboxInput(name='sent', label='Sent to Payroll', value=False, enabled=True,
                          on_change=self.payrun_flow_changed),
            CheckboxInput(name='paid', label='Paid', value=False, enabled=True,
                          on_change=self.payrun_flow_changed),
        ]
        self.payrun_flow_steps_field = MultiFieldInput(name='payrun_steps', label='Payrun Flow Steps<br><br>',
                                                       fields=self.payrun_flow_steps_schema)

        self.payrun_flow_steps_widget = StepperWidget(title='Payrun Flow',
                                                      steps=[{'label': 'Created', 'iconCss': 'fa-solid fa-circle-1'}],
                                                      direction='vertical',
                                                      label_position='right', )
        self.payrun_flow_steps_view = InlineMessage(content=self.payrun_flow_steps_widget.html)

        # Buttons
        self.action_button = Button(content='Edit',
                                    container_id='payrun-settings-action-button',
                                    action=self.action_handler)
        self.connection_button = Button(content='Create Connection', action=self.create_connection)

        # Header
        self.form_header = f'\
            <div class="pl-form-header">\
                <div class="pl-form-header-title" style="float: left">Payrun Settings</div>\
                <div id="payrun-settings-action-button" style="float: right">{self.action_button}</div>\
            </div>'

        sections = [
            {
                'name': '_', 'cols': [
                [
                    self.integration,
                    self.frequency,
                    self.pay_period_start_day,
                    self.pay_period_end_day,
                    self.pay_day,

                    # self.view_integration,
                    # self.view_frequency,
                    # self.view_pay_period_start_day,
                    # self.view_pay_period_end_day,
                    # self.view_pay_day,
                ],
                [self.payrun_flow_steps_field],
                [self.payrun_flow_steps_view]
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
            action = 'view'
        else:
            action = 'edit'

        super().__init__(header=self.form_header,
                         sections=sections,
                         action=action,
                         buttons_mode='off',
                         **kwargs)
        self.fullscreen = True
        self.opened = False

    def form_open(self, args, **kwargs):
        super().form_open(args)
        self.action_button.content = 'Edit' if self.action == 'view' else 'Save'
        self.action_button.show()
        self.connection_button.hide()
        if not self.opened:
            self.payrun_flow_steps_view.show()
            self.payrun_flow_steps_widget.form_show(height=self.form.element.offsetHeight - 100)
            self.opened = True
        # self.payrun_flow_changed(args)

    def action_handler(self, args):
        if self.action == 'view':
            self.action = 'edit'
            self.integration.enabled = True
            self.frequency.enabled = True
            self.pay_period_start_day.enabled = True
            self.pay_period_end_day.enabled = True
            self.pay_day.enabled = True
            self.payrun_flow_steps_field.enabled = True
            self.payrun_flow_steps_field.fields[0].enabled = False
        else:
            self.action = 'view'
        self.form_open(args)


    def payrun_flow_changed(self, args):
        print('payrun_flow_changed', args)
        flow_steps = []
        step_num = 0
        for field in self.payrun_flow_steps_field.fields:
            if field.value is True:
                step_num += 1
                flow_steps.append({'label': field.label, 'iconCss': f'fa-solid fa-circle-{step_num}'})
        self.payrun_flow_steps_widget.steps = flow_steps

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
