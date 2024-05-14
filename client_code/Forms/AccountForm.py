from AnvilFusion.components.FormBase import FormBase
from AnvilFusion.components.FormInputs import *
from AnvilFusion.components.MultiFieldInput import MultiFieldInput
from AnvilFusion.components.SubformGrid import SubformGrid
from AnvilFusion.tools.utils import AppEnv
from ..app.models import Tenant, Account, User


class AccountForm(FormBase):
    def __init__(self, **kwargs):
        print('AccountForm')
        kwargs['model'] = 'Account'

        self.account = None

        self.account_name = TextInput(name='name', label='Account Name', required=True)
        self.business_name = TextInput(name='business_name', label='Business Name', required=True)
        self.address = MultiFieldInput(name='address', model='Account')
        self.phone = TextInput(name='phone', label='Phone')
        self.email = TextInput(name='email', label='Email')
        self.website = TextInput(name='website', label='Website')
        self.logo = InlineMessage(name='logo', label='Logo')
        self.subscription = MultiFieldInput(name='subscription', model='Account', label='_', cols=2)

        self.users = SubformGrid(name='users', label='User List', model='User', is_dependent=True,
                                 # link_model='Tenant', link_field='case_workflow',
                                 form_container_id=kwargs.get('target'),
                                 # view_config=workflow_items_view,
                                 )

        tabs = [
            {
                'name': 'account', 'label': 'Account Info', 'sections':
                [
                    {
                        'name': '_', 'label': '', 'cols': [
                            [self.account_name, self.business_name, self.phone, self.email, self.website],
                            [self.address],
                            [None]
                        ]
                    },
                ],
            },
            {
                'name': 'subscription', 'label': 'Subscription', 'sections':
                [
                    {
                        'name': '_', 'cols': [
                            [self.subscription]
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
        ]

        super().__init__(tabs=tabs,
                         header='Account Settings',
                         button_cancel_label='Close',
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
            print('business', self.business_instance)
            self.business_name.value = self.account['name']
            self.phone.value = self.account['phone']
            self.email.value = self.account['email']
            self.website.value = self.account['website']
            self.address.value = self.account['address']
            self.subscription.value = self.account['subscription']
            self.users.filters = {'tenant_uid': self.data['uid']}
            self.users.value = self.data
            super().form_open(args)
        else:
            super().form_open(args)
            self.form.header = 'Create Business Account'
            buttons = self.form.getButtons()
            for button in buttons:
                if button.cssClass == 'da-save-button':
                    button.content = 'Create Account'
                for i in range(1, 4):
                    self.tabs.enableTab(i, False)
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
