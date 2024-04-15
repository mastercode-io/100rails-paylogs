from AnvilFusion.components.FormBase import FormBase, POPUP_WIDTH_COL2
from AnvilFusion.components.FormInputs import *
from AnvilFusion.components.MultiFieldInput import MultiFieldInput


SERVICE_TYPES = [
    'BPA',
    'Accounting',
    'Time Tracking',
    'CRM',
    'HR',
    'Payroll',
    'Project Management',
    'Other',
]
CONNECTION_TYPES = [
    'OAuth',
    'API Key',
    'Username/Password',
]


class AppIntegrationForm(FormBase):
    def __init__(self, **kwargs):
        print('AppIntegrationForm')
        kwargs['model'] = 'AppIntegration'

        self.service_name = TextInput(name='service_name', label='Service Name', required=True)
        self.type = DropdownInput(name='type', label='Service Type',
                                  options=SERVICE_TYPES, required=True)
        self.url = TextInput(name='url', label='URL')
        self.connection_type = DropdownInput(name='connection_type', label='Connection Type',
                                             options=CONNECTION_TYPES,
                                             required=True)
        self.description = MultiLineInput(name='description', label='Description', rows=4)
        self.status = DropdownInput(name='status', label='Status',
                                    options=['Active', 'Inactive'], required=True)

        fields = [
            self.service_name,
            self.type,
            self.url,
            self.connection_type,
            self.description,
            self.status,
        ]

        super().__init__(fields=fields, width=POPUP_WIDTH_COL2, **kwargs)
