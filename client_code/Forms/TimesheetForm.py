from AnvilFusion.components.FormBase import FormBase
from AnvilFusion.components.FormInputs import *


class TimesheetForm(FormBase):
    def __init__(self, **kwargs):
        print('TimesheetForm')
        kwargs['model'] = 'Timesheet'

        # timesheet_type = Relationship("TimesheetType")
        # employee = Relationship("Employee")
        # payrun = Relationship("Payrun")
        # job = Relationship("Job")
        # date = Attribute(field_type=types.FieldTypes.DATE)
        # start_time = Attribute(field_type=types.FieldTypes.DATETIME)
        # end_time = Attribute(field_type=types.FieldTypes.DATETIME)
        # status = Attribute(field_type=types.FieldTypes.ENUM_SINGLE)
        # approved_by = Relationship("Employee")
        # notes = Attribute(field_type=types.FieldTypes.MULTI_LINE)
        # total_pay = Attribute(field_type=types.FieldTypes.CURRENCY)

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
