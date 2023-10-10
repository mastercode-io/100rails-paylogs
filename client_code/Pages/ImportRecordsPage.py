from AnvilFusion.components.PageBase import PageBase
from AnvilFusion.components.FormInputs import *
from anvil.js.window import ej
from ..app.models import Employee, EmployeeRole, Job, Location, Timesheet, TimesheetType
from datetime import datetime
import uuid
import json


MODELS_LIST = [
    'Employee',
    'Job',
    'Timesheet'
]

EMPLOYEE_FIELDS = {
    'first_name': lambda rec, _: rec['Full_Name'].strip().split(' ')[0],
    'last_name': lambda rec, _: rec['Full_Name'].strip().split(' ')[-1],
    'email': 'Work_Email',
    'mobile': 'Work_Phone',
    'role': lambda rec, roles: [roles[rec['Position_or_Title'].strip()]] if rec.get('Position_or_Title').strip() else None,
}

JOB_FIELDS = {
    'number': 'Quote_Job_Number',
    'name': 'Job_Reference',
    'location': lambda rec, locations: locations[rec['Service_Location'].strip()]
}

# timesheet_type = Relationship("TimesheetType")
# employee = Relationship("Employee")
# payrun = Relationship("PayRun")
# job = Relationship("Job")
# date = Attribute(field_type=types.FieldTypes.DATE)
# start_time = Attribute(field_type=types.FieldTypes.DATETIME)
# end_time = Attribute(field_type=types.FieldTypes.DATETIME)
# status = Attribute(field_type=types.FieldTypes.ENUM_SINGLE)
TIMESHEET_FIELDS = {
    'timesheet_type': lambda rec, timesheet_types: timesheet_types[rec['Related_Time_Type']],
    'employee': lambda rec, employees: employees[rec['Related_Staff.Full_Name'].strip()],
    'job': lambda rec, jobs: [jobs[rec['Job_Number'].strip()]] if rec.get('Job_Number') else None,
    'date': 'Date',
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
        self.record_count = InlineMessage(name='record_count')

        self.content = f'<br><div id="{self.select_model.container_id}" style="width:300px;"></div>'
        self.content += f'<div id="{self.upload_file.container_id}" style="width:300px;"></div>'
        self.content += f'<br><div id="{self.import_button_id}"></div><br><br>'
        self.content += f'<div id="{self.execution_log.container_id}" style="overflow-y: scroll; height: 100%;"></div>'
        self.content += f'<div id="{self.record_count.container_id}" style="overflow-y: scroll; height: 100%;"></div>'

        super().__init__(page_title=title, content=self.content, overflow='auto', **kwargs)

        self.file_content = None


    def form_show(self, **args):
        # print('MigratePage.form_show')
        super().form_show(**args)
        self.select_model.show()
        self.upload_file.show()
        self.import_button.appendTo(f'#{self.import_button_id}')
        self.import_button.element.onclick = self.import_button_action
        self.execution_log.show()
        self.execution_log.message = 'Click <b>Import Records</b> to start import<br><br>'
        self.record_count.show()


    def import_button_action(self, args):
        print('import_button_action')
        if self.select_model.value:
            self.execution_log.message = f'Importing {self.select_model.value} records<br><br>'
            if self.select_model.value == 'Employee':
                self.import_employees(self.file_content)
            elif self.select_model.value == 'Job':
                self.import_jobs(self.file_content)
            elif self.select_model.value == 'Timesheet':
                self.import_timesheets(self.file_content)

        self.execution_log.message += '<br>Import completed'


    def log_message(self, message):
        self.execution_log.message += str(message) + '<br>'


    def file_selected(self, args):
        # print('file_selected', self.upload_file.value)
        file_obj = self.upload_file.value
        self.file_content = json.loads(file_obj.rawFile.text())
        if self.select_model.value == 'Employee':
            self.log_message(f'Uploaded {len(self.file_content["Employees"])} {self.select_model.value} records')


    def import_employees(self, file_content):
        print('import_employees')
        self.log_message(f'Importing {len(file_content["Employees"])} employees')

        # import employee roles
        uploaded_employee_roles = set(record['Position_or_Title'].strip() for record in file_content['Employees']
                                      if record['Position_or_Title'].strip())
        existing_employee_roles = set([role.name for role in EmployeeRole.search()])
        new_employee_roles = uploaded_employee_roles - existing_employee_roles
        if new_employee_roles:
            self.log_message(f'Adding {len(new_employee_roles)} employee roles')
            for role_name in new_employee_roles:
                EmployeeRole(name=role_name, status='Draft').save()
        employee_roles = {role.name: role for role in EmployeeRole.search()}

        count = 0
        for record in file_content['Employees']:
            employee_data = {k: v(record, employee_roles) if callable(v) else record[v] for k, v in EMPLOYEE_FIELDS.items()}
            employee_data['status'] = 'Active'
            # print('employee_data', employee_data)
            employee = Employee(**employee_data).save()
            count += 1
            self.record_count.message = f'Imported {count} employee records'


    def import_jobs(self, file_content):
        print('import_jobs')
        self.log_message(f'Importing {len(file_content["Jobs"])} jobs')

        # import job types
        locations = {location.name: location for location in Location.search()}
        jobs = [job.number for job in Job.search()]

        count = 0
        for record in file_content['Jobs']:
            if record['Quote_Job_Number'] in jobs:
                continue
            job_data = {k: v(record, locations) if callable(v) else record[v] for k, v in JOB_FIELDS.items()}
            job_data['status'] = 'Active'
            job = Job(**job_data).save()
            count += 1
            self.record_count.message = f'Imported {count} job records'


    def import_timesheets(self, file_content):
        print('import_timesheets')
        self.log_message(f'Importing {len(file_content["Timesheets"])} timesheets')

        # import timesheet types
        uploaded_timesheet_types = set(record['Related_Time_Type'] for record in file_content['Timesheets'])
        existing_timesheet_types = set([timesheet_type.name for timesheet_type in TimesheetType.search()])
        new_timesheet_types = uploaded_timesheet_types - existing_timesheet_types
        if new_timesheet_types:
            self.log_message(f'Adding {len(new_timesheet_types)} timesheet types')
            for timesheet_type_name in new_timesheet_types:
                TimesheetType(name=timesheet_type_name, status='Draft').save()
        timesheet_types = {timesheet_type.name: timesheet_type for timesheet_type in TimesheetType.search()}
        employees = {employee.full_name: employee for employee in Employee.search()}
        jobs = {job.number: job for job in Job.search()}

        count = 0
        for record in file_content['Timesheets']:
            timesheet_data = {
                'timesheet_type': timesheet_types[record['Related_Time_Type']],
                'employee': employees[record['Related_Staff.Full_Name']],
                'job': jobs[record['Related_Job.Quote_Job_Number']],
                'date': datetime.strptime(record['Timesheet_Date'], '%d-%b-%Y').date(),
                'status': 'Approved',
            }
            timesheet = Timesheet(**timesheet_data).save()
            count += 1
            self.record_count.message = f'Imported {count} timesheet records'