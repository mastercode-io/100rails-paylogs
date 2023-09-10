from AnvilFusion.components.FormBase import FormBase, POPUP_WIDTH_COL2
from AnvilFusion.components.FormInputs import *
from AnvilFusion.components.MultiFieldInput import MultiFieldInput


class BusinessForm(FormBase):
    def __init__(self, **kwargs):
        print('BusinessForm')
        kwargs['model'] = 'Business'

        self.name = TextInput(name='name', label='Company Name', required=True)
        self.address= MultiFieldInput(name='address', model='Business')
        self.phone = TextInput(name='phone', label='Phone')
        self.email = TextInput(name='email', label='Email')
        self.website = TextInput(name='website', label='Website')
        self.logo = InlineMessage(name='logo', label='Logo')

        sections = [
            {
              'name': '_', 'rows': [
                {self.logo}
            ]
            },
            {
                'name': '_', 'cols': [
                    [self.name, self.phone, self.email, self.website],
                    [self.address],
                ]
            }
        ]

        super().__init__(sections=sections, width=POPUP_WIDTH_COL2, **kwargs)
        self.fullscreen = True
