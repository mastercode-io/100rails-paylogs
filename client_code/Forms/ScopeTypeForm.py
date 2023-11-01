from AnvilFusion.components.FormBase import FormBase
from AnvilFusion.components.FormInputs import *


class ScopeTypeForm(FormBase):
    def __init__(self, **kwargs):
        print('ScopeTypeForm')
        kwargs['model'] = 'ScopeType'

        # name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
        # description = Attribute(field_type=types.FieldTypes.MULTI_LINE)
        # pay_rate_template = Relationship("PayRateTemplate")
        # status = Attribute(field_type=types.FieldTypes.ENUM_SINGLE)
        self.name = TextInput(name='name', label='Name')
        self.description = MultiLineInput(name='description', label='Description', rows=4)
        self.pay_rate_template = LookupInput(name='pay_rate_template', label='Pay Rate Template', model='PayRateTemplate')
        self.status = RadioButtonInput(name='status', label='Status', options=['Active', 'Inactive'], value='Active')

        fields = [
            self.name,
            self.description,
            self.pay_rate_template,
            self.status,
        ]

        super().__init__(fields=fields, **kwargs)
        # self.fullscreen = True
