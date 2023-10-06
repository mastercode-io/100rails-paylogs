from AnvilFusion.components.FormBase import FormBase
from AnvilFusion.components.FormInputs import *


class EmployeeForm(FormBase):
    def __init__(self, **kwargs):
        print('EmployeeForm')
        kwargs['model'] = 'Employee'


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
