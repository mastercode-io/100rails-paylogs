from AnvilFusion.components.FormBase import FormBase, POPUP_WIDTH_COL2
from AnvilFusion.components.FormInputs import *
from AnvilFusion.components.MultiFieldInput import MultiFieldInput
from AnvilFusion.components.SubformGrid import SubformGrid


class CreateTenantForm(FormBase):
    def __init__(self, **kwargs):
        print('CreateTenantForm')
        kwargs['model'] = 'Business'

        self.name = TextInput(name='name', label='Account Name', required=True)
        self.business_name = TextInput(name='business_name', label='Business Name', required=True)
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
                    {self.name, None}
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

        super().__init__(tabs=tabs, header='Create Business Account', **kwargs)
        self.fullscreen = True


    def form_open(self, args):
        super().form_open(args)
        print('CreateTenantForm.form_open')
        for button in self.form.buttons:
            if 'cssClass' in button.buttonModel and button.buttonModel['cssClass'] == 'da-save-button':
                print('save button', button.buttonModel['content'])
                button.buttonModel['content'] = 'Create Account'
                for k in button.keys():
                    print(k, button[k])
                button.finalUpdate()
        if self.data.uid is None:
            for i in range(1, 4):
                self.tabs.enableTab(i, False)
        else:
            self.form.header = 'Update Business Account'
