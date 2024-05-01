from AnvilFusion.components.FormBase import FormBase
from AnvilFusion.components.FormInputs import *
from AnvilFusion.components.MultiFieldInput import MultiFieldInput
from ..app.models import PayrunConfig, AppIntegration, AppOutApiCredential, SYSTEM_TENANT_UID
from ..Pages.widgets import StepperWidget

PAYRUN_FREQUENCY = ['Weekly', 'Fortnightly', 'Monthly']
WEEK_DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
PAY_CATEGORY_TYPES = {
    'single': 'Single category for each pay rule',
    'role': 'Pay category for each pay rule/employee role',
}


class PayrollSettingsForm(FormBase):
    def __init__(self, **kwargs):
        print('PayrollSettingsForm')
        kwargs['model'] = 'PayrollConfig'

        self.use_integration = CheckboxInput(name='use_integration', label='Use Integration to Payroll',
                                             value=False,
                                             on_change=self.use_integration_changed)
        self.integration = LookupInput(name='integration', label='Integration',
                                       model='AppIntegration', get_data=False,
                                       on_change=self.integration_selected)
        self.connection_message = InlineMessage(css_class='pl-message-bar')
        self.connection_button = Button(content='Create Connection', action=self.create_connection)

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
        self.pay_category_type = DropdownInput(name='pay_category_type', label='Pay Category Type',
                                               options=PAY_CATEGORY_TYPES.keys(), value='single',
                                               on_change=self.pay_category_type_selected)
        self.payrun_initial_date = DateInput(name='payrun_initial_date', label='Initial Payrun Date')

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

        # Header
        self.form_header = f'\
            <div class="pl-form-header">\
                <div class="pl-form-header-title" style="float: left">Payroll Settings</div>\
                <div id="payrun-settings-action-button" style="float: right">{self.action_button}</div>\
            </div>'

        sections = [
            {
                'name': 'Pay Period', 'cols': [
                    [
                        self.frequency,
                        self.pay_period_start_day,
                        self.pay_period_end_day,
                        self.pay_day,
                        self.payrun_initial_date,

                        # self.view_integration,
                        # self.view_frequency,
                        # self.view_pay_period_start_day,
                        # self.view_pay_period_end_day,
                        # self.view_pay_day,
                    ],
                    [],
                    []
                ]
            },
            {
                'name': 'Pay Calculation', 'cols': [
                    [
                        self.pay_category_type,
                    ],
                    [],
                    []
                ]
            },
            {
                'name': 'Payroll Integration', 'cols': [
                    [
                        self.use_integration,
                        self.integration,
                        self.connection_message,
                        self.connection_button,
                    ],
                    [],
                    []
                ]
            },
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
        # if not self.opened:
        #     self.payrun_flow_steps_view.show()
        #     self.payrun_flow_steps_widget.form_show(height=self.form.element.offsetHeight - 100)
        #     self.opened = True
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
            self.connection_message.accent = None
            self.connection_message.content = ''
            self.connection_button.hide()
        else:
            payroll_integration = AppIntegration.get(self.integration.value['uid'])
            payroll_connection = AppOutApiCredential.get_by('integration', payroll_integration)
            if not payroll_connection:
                self.connection_message.accent = 'warning'
                self.connection_message.content = (f"No connection found for this integration: "
                                                   f"<b>{self.integration.value['name']}</b>")
                self.connection_button.show()

    def use_integration_changed(self, args):
        print('use_integration_changed', args)
        if self.use_integration.value is True:
            self.integration.show()
        else:
            self.integration.hide()

    def pay_category_type_selected(self, args):
        print('pay_category_type_selected', args)
        if not args.get('value') or not self.pay_category_type.value:
            self.pay_category_type.value = 'single'
        if self.pay_category_type.value == 'single':
            self.pay_category_type.label = PAY_CATEGORY_TYPES['single']
        elif self.pay_category_type.value == 'role':
            self.pay_category_type.label = PAY_CATEGORY_TYPES['role']

    def create_connection(self, args):
        print('create_connection', args)
        self.connection_message.accent = 'info'
        self.connection_message.content = 'Creating connection...'
