from AnvilFusion.components.FormBase import FormBase
from AnvilFusion.components.FormInputs import *
from AnvilFusion.components.MultiFieldInput import MultiFieldInput


class EmployeeForm(FormBase):
    def __init__(self, **kwargs):
        print('EmployeeForm')
        kwargs['model'] = 'Employee'

        # create input fields based on Employee model:
        '''
    first_name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    last_name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    email = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    mobile = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    role = Relationship("EmployeeRole", with_many=True)
    status = Attribute(field_type=types.FieldTypes.ENUM_SINGLE)
    address_schema = {
        "address_line_1": Attribute(field_type=types.FieldTypes.SINGLE_LINE),
        "address_line_2": Attribute(field_type=types.FieldTypes.SINGLE_LINE),
        "city_district": Attribute(field_type=types.FieldTypes.SINGLE_LINE),
        "state_province": Attribute(field_type=types.FieldTypes.SINGLE_LINE),
        "country": Attribute(field_type=types.FieldTypes.SINGLE_LINE),
        "postal_code": Attribute(field_type=types.FieldTypes.SINGLE_LINE),
    }
    address = Attribute(field_type=types.FieldTypes.OBJECT, schema=address_schema)
    custom_fields = Attribute(field_type=types.FieldTypes.OBJECT)
        '''
        self.first_name = TextInput(name='first_name', label='First Name')
        self.last_name = TextInput(name='last_name', label='Last Name')
        self.email = TextInput(name='email', label='Email')
        self.mobile = TextInput(name='mobile', label='Mobile')
        self.role = LookupInput(name='role', label='Role', model='EmployeeRole')
        self.status = DropdownInput(name='status', label='Status', options=['Active', 'Inactive'])
        self.address = MultiFieldInput(name='address', label='Address', model='Employee')
        # self.custom_fields = MultiFieldInput(name='custom_fields', label='Custom Fields', model='Employee')

        sections = [
            {
                'name': '_', 'cols': [
                    [' ', self.first_name, self.last_name, self.email, self.mobile, self.role, self.status],
                    [self.address],
                ]
            }
        ]

        super().__init__(sections=sections, **kwargs)
        self.fullscreen = True
