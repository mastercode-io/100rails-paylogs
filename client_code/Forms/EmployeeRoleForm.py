from AnvilFusion.components.FormBase import FormBase
from AnvilFusion.components.FormInputs import *


class EmployeeRoleForm(FormBase):
    def __init__(self, **kwargs):
        print('EmployeeRoleForm')
        kwargs['model'] = 'EmployeeRole'


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
