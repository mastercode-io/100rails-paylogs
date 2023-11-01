from AnvilFusion.components.FormBase import FormBase
from AnvilFusion.components.FormInputs import *


class PayrunForm(FormBase):
    def __init__(self, **kwargs):
        print('PayrunForm')
        kwargs['model'] = 'PayRun'

        # pay_run_type = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
        # pay_period_start = Attribute(field_type=types.FieldTypes.DATE)
        # pay_period_end = Attribute(field_type=types.FieldTypes.DATE)
        # pay_date = Attribute(field_type=types.FieldTypes.DATE)
        # status = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
        # notes = Attribute(field_type=types.FieldTypes.MULTI_LINE)
        #
        # @staticmethod
        # def get_payrun_reference(args):
        #     return f"{args['pay_run_type']}: ({args['pay_period_start']} - {args['pay_period_end']})"
        # reference = Computed(
        #     ("pay_run_type", "pay_period_start", "pay_period_end"), "get_payrun_reference"
        # )


        # pay_run = Relationship("PayRun")
        # employee = Relationship("Employee")
        # timesheet = Relationship("Timesheet")
        # pay_category = Relationship("PayCategory")
        # title = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
        # pay_rate = Attribute(field_type=types.FieldTypes.CURRENCY)
        # units = Attribute(field_type=types.FieldTypes.NUMBER)
        # amount = Attribute(field_type=types.FieldTypes.CURRENCY)
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
