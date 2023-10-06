from AnvilFusion.components.FormBase import FormBase
from AnvilFusion.components.FormInputs import *


class PayRunForm(FormBase):
    def __init__(self, **kwargs):
        print('PayRunForm')
        kwargs['model'] = 'PayRun'


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
