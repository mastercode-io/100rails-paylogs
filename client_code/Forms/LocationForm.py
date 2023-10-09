from AnvilFusion.components.FormBase import FormBase, POPUP_WIDTH_COL3
from AnvilFusion.components.FormInputs import *
from AnvilFusion.components.MultiFieldInput import MultiFieldInput


class LocationForm(FormBase):
    def __init__(self, **kwargs):
        print('LocationForm')
        kwargs['model'] = 'Location'

        '''
    name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    description = Attribute(field_type=types.FieldTypes.MULTI_LINE)
    address_schema = {
        "address_line_1": Attribute(field_type=types.FieldTypes.SINGLE_LINE),
        "address_line_2": Attribute(field_type=types.FieldTypes.SINGLE_LINE),
        "city_district": Attribute(field_type=types.FieldTypes.SINGLE_LINE),
        "state_province": Attribute(field_type=types.FieldTypes.SINGLE_LINE),
        "country": Attribute(field_type=types.FieldTypes.SINGLE_LINE),
        "postal_code": Attribute(field_type=types.FieldTypes.SINGLE_LINE),
    }
    address = Attribute(field_type=types.FieldTypes.OBJECT, schema=address_schema)
    pay_rate_template = Relationship("PayRateTemplate")
    status = Attribute(field_type=types.FieldTypes.ENUM_SINGLE)
'''
        self.name = TextInput(name='name', label='Name')
        self.description = MultiLineInput(name='description', label='Description')
        self.address = MultiFieldInput(name='address', model='Location')
        self.pay_rate_template = LookupInput(name='pay_rate_template', label='Pay Rate Template', model='PayRateTemplate')
        self.status = RadioButtonInput(name='status', label='Status', options=['Active', 'Inactive'])


        sections = [
            {
                'name': '_', 'cols': [
                    [self.name, self.description, self.pay_rate_template, self.status],
                    [self.address],
                ]
            }
        ]

        super().__init__(sections=sections, width=POPUP_WIDTH_COL3, **kwargs)
