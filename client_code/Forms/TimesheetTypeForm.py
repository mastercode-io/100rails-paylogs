from AnvilFusion.components.FormBase import FormBase, POPUP_WIDTH_COL3
from AnvilFusion.components.FormInputs import *
from AnvilFusion.components.MultiFieldInput import MultiFieldInput


class TimesheetTypeForm(FormBase):
    def __init__(self, **kwargs):
        print('TimesheetTypeForm')
        kwargs['model'] = 'TimesheetType'

        self.name = TextInput(name='name', label='Name')
        self.short_code = TextInput(name='short_code', label='Short Code')
        self.description = MultiLineInput(name='description', label='Description')
        self.configuration= MultiFieldInput(name='configuration', model='TimesheetType',cols=2)
        self.test = TextInput(name='test', label='Test', save=False)

        sections = [
            {
              'name': '_', 'rows': [
                {self.name, self.short_code},
                {self.description, self.test},
                {self.configuration}
            ]
            },
        ]

        super().__init__(sections=sections, width=POPUP_WIDTH_COL3, **kwargs)
