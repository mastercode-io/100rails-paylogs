from AnvilFusion.components.FormBase import FormBase
from AnvilFusion.components.FormInputs import *
from AnvilFusion.components.MultiFieldInput import MultiFieldInput


class ScopeForm(FormBase):
    def __init__(self, **kwargs):
        print('ScopeForm')
        kwargs['model'] = 'Scope'

        self.name = TextInput(name='name', label='Name')
        self.description = MultiLineInput(name='description', label='Description', rows=4)
        self.type = LookupInput(name='type', label='Scope Type', model='ScopeType')
        self.status = RadioButtonInput(name='status', label='Status', options=['Active', 'Inactive'], value='Active')
        # self.custom_fields = MultiFieldInput(name='custom_fields', label='Custom Fields', model='Scope', cols=2)

        fields = [
            self.name,
            self.description,
            self.type,
            self.status,
        ]

        super().__init__(fields=fields, **kwargs)
        # self.fullscreen = True
