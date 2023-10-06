from AnvilFusion.components.FormBase import FormBase
from AnvilFusion.components.FormInputs import *


class LocationForm(FormBase):
    def __init__(self, **kwargs):
        print('LocationForm')
        kwargs['model'] = 'Location'


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
