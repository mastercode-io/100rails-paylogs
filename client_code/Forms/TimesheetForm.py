from AnvilFusion.components.FormBase import FormBase, POPUP_WIDTH_COL2
from AnvilFusion.components.FormInputs import *
import anvil.tables.query as q
from ..app.models import EmployeeRole


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
        approved_by_roles = EmployeeRole.search(name=q.any_of(q.ilike('%manager%'), q.ilike('%supervisor%')))
        # print('approved_by_roles', len([*approved_by_roles]))
        approved_by_filters = {
            'employee_role': q.any_of(*approved_by_roles),
        }

        self.employee = LookupInput(name='employee', label='Employee', model='Employee', text_field='full_name')
        self.date = DateInput(name='date', label='Date')
        self.job = LookupInput(name='job', label='Job Name', model='Job')
        self.start_time = TimeInput(name='start_time', label='Start Time')
        self.end_time = TimeInput(name='end_time', label='End Time')
        self.status = DropdownInput(name='status', label='Status', options=['Draft', 'Approved', 'Processed'])
        self.approved_by = LookupInput(name='approved_by', label='Approved By', model='Employee', text_field='full_name',
                                       filters=approved_by_filters)
        self.notes = MultiLineInput(name='notes', label='Notes')
        self.total_pay = NumberInput(name='total_pay', label='Total Pay')

        sections = [
            {
                'name': '_', 'cols': [
                    [self.employee, self.job, self.approved_by, self.status],
                    [self.date, self.start_time, self.end_time, self.total_pay],
                ]
            }
        ]

        super().__init__(sections=sections, width=POPUP_WIDTH_COL2, **kwargs)
        # self.fullscreen = True
