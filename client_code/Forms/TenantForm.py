from AnvilFusion.components.FormBase import FormBase
from AnvilFusion.components.FormInputs import *
from AnvilFusion.components.MultiFieldInput import MultiFieldInput
from AnvilFusion.components.SubformGrid import SubformGrid
from AnvilFusion.tools.utils import AppEnv
from ..app.models import Tenant, Business, User


class TenantForm(FormBase):
    def __init__(self, **kwargs):
        print('CreateTenantForm')
        kwargs['model'] = 'Business'

        self.tenant = TextInput(name='name', label='Account Name', required=True)
        self.business_name = TextInput(name='name', label='Business Name', required=True)
        self.address= MultiFieldInput(name='address', model='Business')
        self.phone = TextInput(name='phone', label='Phone')
        self.email = TextInput(name='email', label='Email')
        self.website = TextInput(name='website', label='Website')
        self.logo = InlineMessage(name='logo', label='Logo')
        self.subscription = MultiFieldInput(name='subscription', model='Business', label='_', cols=2)

        self.users = SubformGrid(name='users', label='User List', model='User',
                                 # link_model='Tenant', link_field='case_workflow',
                                 form_container_id=kwargs.get('target'),
                                 # view_config=workflow_items_view,
                                 )

        tabs = [
            {
                'name':'account', 'label': 'Account', 'sections': [
                {
                    'name': '_', 'rows': [
                    {self.tenant, None}
                ]
                },
                {
                    'name': '_', 'label': 'Company Information', 'cols': [
                    [self.business_name, self.phone, self.email, self.website],
                    [self.address],
                ]
                },
            ],
            },
            {
                'name':'subscription', 'label': 'Subscription', 'sections': [
                {
                    'name': '_', 'rows': [
                    [self.subscription]
                ]
                }
            ],
            },
            {
                'name':'billing', 'label': 'Billing', 'sections': [
                {
                    'name': '_', 'rows': [
                    # []
                ]
                }
            ],
            },
            {
                'name':'users', 'label': 'Users', 'sections': [
                {
                    'name': '_', 'rows': [
                    [self.users]
                ]
                }
            ],
            },
        ]

        super().__init__(tabs=tabs, header='Update Business Account', **kwargs)
        self.fullscreen = True


    def form_open(self, args):
        super().form_open(args)
        print('TenantForm.form_open')
        if self.data and hasattr(self.data, 'uid'):
            AppEnv.set_tenant(tenant_uid=self.data.uid)
            business = Business.search()
            self.business_name.value = business.name
            self.phone.value = business.phone
            self.email.value = business.email
            self.website.value = business.website
            self.address.value = business.address
        else:
            self.form.header = 'Create Business Account'
            buttons = self.form.getButtons()
            for button in buttons:
                if button.cssClass == 'da-save-button':
                    button.content = 'Create Account'
                for i in range(1, 3):
                    self.tabs.enableTab(i, False)


    def form_cancel(self, args):
        AppEnv.reset_tenant()
        super().form_cancel(args)


    def form_save(self, args):
        if not self.data or not hasattr(self.data, 'uid'):
            self.data = Tenant(name=self.tenant.value).save()
            AppEnv.set_tenant(tenant_uid=self.data.uid)
            self.form.header = 'Update Business Account'
            buttons = self.form.getButtons()
            for button in buttons:
                if button.cssClass == 'da-save-button':
                    button.content = 'Save'
                for i in range(1, 3):
                    self.tabs.enableTab(i, True)
