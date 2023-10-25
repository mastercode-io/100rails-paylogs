from AnvilFusion.components.FormBase import FormBase
from AnvilFusion.components.FormInputs import *


class PayRunForm(FormBase):
    def __init__(self, **kwargs):
        print('PayRunForm')
        kwargs['model'] = 'PayRun'

        # name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
        # type = Attribute(field_type=types.FieldTypes.ENUM_SINGLE)
        # pay_period_start_day = Attribute(field_type=types.FieldTypes.ENUM_SINGLE)
        # pay_period_end_day = Attribute(field_type=types.FieldTypes.ENUM_SINGLE)
        # pay_day = Attribute(field_type=types.FieldTypes.ENUM_SINGLE)
        # scopes = Relationship("Scope", with_many=True)
        # status = Attribute(field_type=types.FieldTypes.ENUM_SINGLE)

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
