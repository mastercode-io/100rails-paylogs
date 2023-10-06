from AnvilFusion.components.FormBase import FormBase
from AnvilFusion.components.FormInputs import *


class UserForm(FormBase):
    def __init__(self, **kwargs):
        print('UserForm')
        kwargs['model'] = 'User'


        sections = [
            {
              'name': '_', 'rows': [
                {}
            ]
            },
            {
                'name': '_', 'cols': [
                    [],
                    [],
                ]
            }
        ]

        super().__init__(sections=sections, **kwargs)
        # self.fullscreen = True
