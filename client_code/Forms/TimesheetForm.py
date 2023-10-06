from AnvilFusion.components.FormBase import FormBase
from AnvilFusion.components.FormInputs import *


class TimesheetForm(FormBase):
    def __init__(self, **kwargs):
        print('TimesheetForm')
        kwargs['model'] = 'Timesheet'


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
