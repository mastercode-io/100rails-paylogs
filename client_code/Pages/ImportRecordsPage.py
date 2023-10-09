from AnvilFusion.components.PageBase import PageBase
from AnvilFusion.components.FormInputs import *
from anvil.js.window import ej
import uuid
import json


MODELS_LIST = [
    'Employee',
    'Job',
    'Timesheet'
]


class ImportRecordsPage(PageBase):
    def __init__(self, **kwargs):
        print('ImportRecordsPage')
        title = 'Import Records'
        self.select_model = DropdownInput(name='select_model', label='Select Model', options=MODELS_LIST)
        self.upload_file = FileUploadInput(name='upload_file', label='Upload File', on_change=self.file_selected)
        self.import_button = ej.buttons.Button({
            'content': 'Import Records',
            'isPrimary': True,
            'size': 'large',
        })
        self.import_button_id = f'migrate-button-{uuid.uuid4()}'
        self.execution_log = InlineMessage(name='execution_log')

        self.content = f'<br><div id="{self.select_model.container_id}" style="width:300px;"></div>'
        self.content += f'<div id="{self.upload_file.container_id}" style="width:300px;"></div>'
        self.content += f'<br><div id="{self.import_button_id}"></div><br><br>'
        self.content += f'<div id="{self.execution_log.container_id}" style="overflow-y: scroll; height: 100%;"></div>'

        super().__init__(page_title=title, content=self.content, overflow='auto', **kwargs)


    def form_show(self, **args):
        # print('MigratePage.form_show')
        super().form_show(**args)
        self.select_model.show()
        self.upload_file.show()
        self.import_button.appendTo(f'#{self.import_button_id}')
        self.import_button.element.onclick = self.import_button_action
        self.execution_log.show()
        self.execution_log.message = 'Click <b>Import Records</b> to start import'


    def import_button_action(self, args):
        print('import_button_action')
        self.execution_log.message = f'Importing {self.select_model.value} records<br><br>'

        self.execution_log.message += '<br>Import complete.'


    def log_message(self, message):
        self.execution_log.message += str(message) + '<br>'


    def file_selected(self, args):
        print('file_selected', self.upload_file.value)
        uploaded = self.upload_file.value
        file_content = json.loads(uploaded.rawFile.read())
        print(uploaded.name, file_content.keys())
