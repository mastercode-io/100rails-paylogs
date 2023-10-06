from AnvilFusion.components.FormBase import FormBase
from AnvilFusion.components.FormInputs import *


class PayRateRuleForm(FormBase):
    def __init__(self, **kwargs):
        print('PayRateRuleForm')
        kwargs['model'] = 'PayRateRule'


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
