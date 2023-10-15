from AnvilFusion.components.FormBase import FormBase, POPUP_WIDTH_COL2
from AnvilFusion.components.FormInputs import *
from AnvilFusion.components.MultiFieldInput import MultiFieldInput


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

        tabs = [
            {
                'name':'account', 'label': 'Account Details', 'sections': [
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
                'name':'billing', 'label': 'Billing Details', 'sections': [
                {
                    'name': '_', 'rows': [
                    []
                ]
                }
            ],
            },
            {
                'name':'users', 'label': 'Users', 'sections': [
                {
                    'name': '_', 'rows': [
                    []
                ]
                }
            ],
            },
        ]

        super().__init__(tabs=tabs, header='Create Business Account', **kwargs)
        self.fullscreen = True
