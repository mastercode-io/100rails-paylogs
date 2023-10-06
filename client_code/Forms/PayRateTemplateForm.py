from AnvilFusion.components.FormBase import FormBase
from AnvilFusion.components.FormInputs import *


class PayRateTemplateForm(FormBase):
    def __init__(self, **kwargs):
        print('PayRateTemplateForm')
        kwargs['model'] = 'PayRateTemplate'


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
