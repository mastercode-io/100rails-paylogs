from AnvilFusion.components.FormBase import FormBase, POPUP_WIDTH_COL2
from AnvilFusion.components.FormInputs import *
from AnvilFusion.components.MultiFieldInput import MultiFieldInput


class CreateTenantForm(FormBase):
    def __init__(self, **kwargs):
        print('CreateTenantForm')
        kwargs['model'] = 'Business'

        self.name = TextInput(name='name', label='Account Name', required=True)
        self.address= MultiFieldInput(name='address', model='Business')
        self.phone = TextInput(name='phone', label='Phone')
        self.email = TextInput(name='email', label='Email')
        self.website = TextInput(name='website', label='Website')
        self.logo = InlineMessage(name='logo', label='Logo')
        self.subscription = MultiFieldInput(name='subscription', model='Business', cols=2)

        tabs = [
            {
                'name':'account', 'label': 'Account Details', 'sections': [
                {
                    'name': '_', 'rows': [
                    {self.name, None}
                ]
                },
                {
                    'name': '_', 'cols': [
                    ['Company Information', self.name, self.phone, self.email, self.website],
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
        ]

        super().__init__(tabs=tabs, header='Create Account', width=POPUP_WIDTH_COL2, **kwargs)
        self.fullscreen = True
