from AnvilFusion.components.FormBase import FormBase
from AnvilFusion.components.FormInputs import *
from AnvilFusion.components.MultiFieldInput import MultiFieldInput
from AnvilFusion.components.SubformGrid import SubformGrid
from AnvilFusion.components.GridView import GRID_TOOLBAR_COMMAND_SEARCH, GRID_TOOLBAR_COMMAND_SEARCH_TOGGLE
from AnvilFusion.tools.utils import AppEnv
from ..app.models import Tenant, Account, User
from ..Pages.PayrollSettingsPage import PayrollSettingsPage
import anvil.tables.query as q


class AccountForm(FormBase):
    def __init__(self, **kwargs):
        print('AccountForm')
        kwargs['model'] = 'Account'

        self.account = None

        self.subtitle = SectionSubtitle(name='company_info', value='Company Info')
        self.account_name = TextInput(name='name', label='Account Name', required=True)
        self.business_name = TextInput(name='business_name', label='Business Name', required=True)
        self.address = MultiFieldInput(name='address', model='Account')
        self.phone = TextInput(name='phone', label='Phone')
        self.email = TextInput(name='email', label='Email')
        self.website = TextInput(name='website', label='Website')
        self.logo = InlineMessage(name='logo', label='Logo')
        self.subscription = MultiFieldInput(name='subscription', model='Account', label='_', cols=2)

        self.user_view_config = {
            'model': 'User',
            'columns': [
                {'name': 'tenant_name', 'label': 'Data File'},
                {'name': 'full_name', 'label': 'User Name'},
                {'name': 'email', 'label': 'Email'},
                {'name': 'enabled', 'label': 'Enabled'},
                {'name': 'permissions', 'label': 'Permissions'},
            ]
        }
        self.users = SubformGrid(name='users', label='User List', model='User', is_dependent=True,
                                 # link_model='Tenant', link_field='case_workflow',
                                 form_container_id=kwargs.get('target'),
                                 view_config=self.user_view_config,
                                 )

        self.data_files = SubformGrid(name='data_files', label='Data Files', model='Timesheet', is_dependent=False,
                                      form_container_id=kwargs.get('target'))

        incoming_links_view = {
            'model': 'AppInApiCredential',
            'columns': [
                {'name': 'api_secret', 'label': 'API Secret'},
                {'name': 'api_key', 'label': 'API Key'},
                {'name': 'api_user.tenant_name', 'label': 'Tenant'},
                {'name': 'status', 'label': 'Status'},
            ],
            'toolbar': [
                GRID_TOOLBAR_COMMAND_SEARCH,
                GRID_TOOLBAR_COMMAND_SEARCH_TOGGLE,
            ],
            'content_wrap': False,
        }
        self.incoming_links = SubformGrid(
            name='incoming_links', label='Incoming', model='AppInApiCredential',
            link_model='AppIntegration', link_field='integration',
            form_container_id=kwargs.get('target'),
            view_config=incoming_links_view,
        )

        outgoing_links_view = {
            'model': 'AppOutApiCredential',
            'columns': [
                {'name': 'auth_type', 'label': 'Auth Type'},
                {'name': 'api_credentials', 'label': 'API Credentials'},
                {'name': 'status', 'label': 'Status'},
            ],
            'toolbar': [
                GRID_TOOLBAR_COMMAND_SEARCH,
                GRID_TOOLBAR_COMMAND_SEARCH_TOGGLE,
            ],
            'content_wrap': False,
        }
        self.outgoing_links = SubformGrid(
            name='outgoing_links', label='Outgoing', model='AppOutApiCredential',
            link_model='AppIntegration', link_field='integration',
            form_container_id=kwargs.get('target'),
            view_config=outgoing_links_view,
        )

        self.payroll_settings_frame = ContentFrame(name='payroll_settings')
        self.payroll_settings_page = PayrollSettingsPage(container_id=self.payroll_settings_frame.container_id,
                                                         account=self.account)

        tabs = [
            {
                'name': 'account', 'label': 'Account Info', 'sections':
                [
                    {
                        'name': '_', 'label': '', 'cols': [
                            [
                                self.subtitle,
                                self.account_name,
                                self.business_name,
                                self.phone,
                                self.email,
                                self.website
                            ],
                            [self.address],
                            []
                        ]
                    },
                ],
            },
            {
                'name': 'subscription', 'label': 'Subscription', 'sections':
                [
                    {
                        'name': '_', 'cols': [
                            [self.subscription],
                            [],
                        ]
                    }
                ],
            },
            {
                'name': 'billing', 'label': 'Billing', 'sections':
                [
                    {
                        'name': '_', 'rows': [
                            # []
                        ]
                    }
                ],
            },
            {
                'name': 'users', 'label': 'Users', 'sections':
                [
                    {
                        'name': '_', 'rows': [
                            [self.users]
                        ]
                    }
                ],
            },
            {
                'name': 'data_files', 'label': 'Data Files', 'sections':
                [
                    {
                        'name': '_', 'rows': [
                            [self.data_files]
                        ]
                    }
                ],
            },
            {
                'name': 'payroll_settings', 'label': 'Payroll', 'sections':
                [
                    {
                        'name': '_', 'rows': [
                            [self.payroll_settings_frame]
                        ]
                    }
                ],
            },
            {
                'name': 'integrations', 'label': 'Integrations', 'sections':
                [
                    {
                        'name': '_', 'cols': [
                            [self.incoming_links],
                            [self.outgoing_links]
                        ]
                    }
                ],
            },
        ]

        super().__init__(tabs=tabs,
                         header='Account Settings',
                         buttons_mode='off',
                         **kwargs)
        self.fullscreen = True


    def form_open(self, args, **kwargs):
        print('AccountForm.form_open')
        # super().form_open(args)
        print(self.data)
        if self.data['uid']:
            # AppEnv.set_tenant(tenant_uid=self.data.tenant_uid)
            print(self.data['uid'], self.data['tenant_uid'])
            self.account = Account.get_by('tenant_uid', self.data['uid'])
            print('business', self.account)
            self.business_name.value = self.account['name']
            self.phone.value = self.account['phone']
            self.email.value = self.account['email']
            self.website.value = self.account['website']
            self.address.value = self.account['address']
            self.subscription.value = self.account['subscription']
            super().form_open(args)

            user_list = []
            for tenant in self.account['data_files']:
                print('tenant', tenant['uid'])
                user_list += User.get_grid_view(
                    view_config=self.user_view_config,
                    filters={'tenant_uid': tenant['uid']}
                )
            print('user_list', user_list)
            self.users.value = user_list
            # data_files = []
            # for tenant in self.account['data_files']:
            #     data_files.append(Tenant.get_row_view(tenant))
            # print('data_files', self.account['data_files'])
            # self.data_files.value = [tenant.to_json_dict() for tenant in self.account['data_files']]

            self.payroll_settings_page.form_show()

        else:
            super().form_open(args)
            self.form.header = 'Create Account'
            buttons = self.form.getButtons()
            for button in buttons:
                if button.cssClass == 'da-save-button':
                    button.content = 'Create Account'
        # super().form_open(args)


    def form_cancel(self, args):
        # AppEnv.reset_tenant()
        super().form_cancel(args)


    def form_save(self, args, **kwargs):

        if not self.data['uid']:
            add_new = True
            tenant = Tenant(name=self.account_name.value).save()
            print('a) tenant', tenant['uid'], tenant['tenant_uid'])
            tenant['tenant_uid'] = tenant['uid']
            tenant.save()
            print('b) tenant', tenant['uid'], tenant['tenant_uid'])
            # AppEnv.set_tenant(tenant_uid=tenant.uid)
            self.account = Account(
                tenant_uid=tenant['uid'],
                name=self.business_name.value,
                phone=self.phone.value,
                email=self.email.value,
                website=self.website.value,
                address=self.address.value,
            ).save()
            self.form.header = 'Update Business Account'
            buttons = self.form.getButtons()
            for button in buttons:
                if button.cssClass == 'da-save-button':
                    button.content = 'Save'
                for i in range(1, 4):
                    self.tabs.enableTab(i, True)
            self.users.filters = {'tenant_uid': tenant['uid']}
            self.users.value = tenant
            self.data = tenant

        else:
            add_new = False
            self.account['name'] = self.business_name.value
            self.account['phone'] = self.phone.value
            self.account['email'] = self.email.value
            self.account['website'] = self.website.value
            self.account['address'] = self.address.value
            self.account['subscription'] = self.subscription.value
            self.account.save()

        self.update_source(self.data, add_new)
