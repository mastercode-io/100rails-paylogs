from AnvilFusion.components.PageBase import PageBase
from AnvilFusion.components.FormInputs import *
from anvil.js.window import ej
from ..app.models import Employee, EmployeeRole, Job, Timesheet
import uuid
import json


MODELS_LIST = [
    'Employee',
    'Job',
    'Timesheet'
]
EMPLOYEE_FIELDS = {
    'first_name': lambda rec: rec['Full_Name'].strip().split(' ')[0],
    'last_name': lambda rec: rec['Full_Name'].strip().split(' ')[-1],
    'email': 'Work_Email',
    'mobile': 'Work_Phone',
    'role': lambda rec, roles: roles.get(rec['Position_or_Title'].strip(), None),
}


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

        self.file_content = None
        self.employee_roles = {}
        self.timesheet_types = {}
        self.job_types = {}
        self.jobs = {}


    def form_show(self, **args):
        # print('MigratePage.form_show')
        super().form_show(**args)
        self.select_model.show()
        self.upload_file.show()
        self.import_button.appendTo(f'#{self.import_button_id}')
        self.import_button.element.onclick = self.import_button_action
        self.execution_log.show()
        self.execution_log.message = 'Click <b>Import Records</b> to start import<br><br>'


    def import_button_action(self, args):
        print('import_button_action')

        self.execution_log.message = f'Importing {self.select_model.value} records<br><br>'
        if self.select_model.value == 'Employee':
            self.import_employees(self.file_content)

        self.execution_log.message += '<br>Import complete.'


    def log_message(self, message):
        self.execution_log.message += str(message) + '<br>'


    def file_selected(self, args):
        print('file_selected', self.upload_file.value)
        file_obj = self.upload_file.value
        self.file_content = json.loads(file_obj.rawFile.text())
        if self.select_model.value == 'Employee':
            self.log_message(f'Uploaded {len(self.file_content["Employees"])} employee records')


    def import_employees(self, file_content):
        print('import_employees')
        self.log_message(f'Importing {len(file_content["Employees"])} employees')

        # import employee roles
        uploaded_employee_roles = set(record['Position_or_Title'].strip() for record in file_content['Employees']
                                      if record['Position_or_Title'].strip())
        existing_employee_roles = set([role.name for role in EmployeeRole.search()])
        new_employee_roles = uploaded_employee_roles - existing_employee_roles
        for role_name in new_employee_roles:
            EmployeeRole(name=role_name, status='Draft').save()
            self.log_message(f'Imported {role_name}')
        self.employee_roles = {role.name: role for role in EmployeeRole.search()}

        for record in file_content['Employees']:
            employee_data = {k: v(record, self.employee_roles) if callable(v) else record[v] for k, v in EMPLOYEE_FIELDS.items()}
            employee_data['status'] = 'Active'
            employee = Employee(**employee_data).save()
            self.log_message(f'Imported {employee.first_name} {employee.last_name}')
