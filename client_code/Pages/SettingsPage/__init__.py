from AnvilFusion.components.PageBase import PageBase
from AnvilFusion.components.FormInputs import *
from AnvilFusion.components.Inputs import InplaceEditor
from AnvilFusion.components.Layouts import Tabs
from AnvilFusion.tools.utils import AppEnv
from ...app.models import Account, Tenant, PayrollConfig
import datetime


class SettingsPage(PageBase):
    def __init__(self, account=None, **kwargs):
        print('SettingsPage')
        title = ''
        self.account = account
        if self.account is None:
            tenant = Tenant.get_row(AppEnv.logged_user.tenant_uid)
            self.account = next(iter(Account.search(data_files=[tenant])), None)

        if self.account is None:
            self.error_message = InlineMessage(content='No account found', accent='warning', css_class='pl-message-bar')
            self.content = f'<div id="{self.error_message.container_id}"></div>'

        elif len(self.account['data_files']) > 1:
            options = [df.to_json_dict() for df in self.account['data_files']]
            current_data_file = None
            for data_file in options:
                if data_file['uid'] == AppEnv.logged_user.tenant_uid:
                    current_data_file = {'uid': data_file['uid'], 'name': data_file['name']}
                    current_data_file = data_file
                    break
            self.data_file = LookupInput(name='data_file',
                                         label='Select Data File',
                                         # options=options,
                                         data=self.account['data_files'],
                                         value=current_data_file,
                                         on_change=self.data_file_selected)
            self.data_fil2 = LookupInput(name='data_file',
                                         label='Select Data File',
                                         # options=options,
                                         data=self.account['data_files'],
                                         inplace_mode='Inline',
                                         value=current_data_file,
                                         on_change=self.data_file_selected)
            self.text_input = TextInput(name='text_input',
                                        label='Text Input',
                                        value='Text Input Value',
                                        inplace_mode='Inline')
            self.number_input = NumberInput(name='number_input',
                                            label='Number Input',
                                            value='123',
                                            inplace_mode='Inline')
            self.multiline_input = MultiLineInput(name='multiline_input',
                                                  label='Multiline',
                                                  value='Some text',
                                                  inplace_mode='Inline')
            self.date_input = DateInput(name='date_input',
                                        label='Date Input',
                                        value=datetime.date.today(),
                                        inplace_mode='Inline')

            tabs_config = [
                {'name': 'payroll', 'label': 'Payroll', 'content': 'Payroll Settings'},
                {'name': 'timesheets', 'label': 'Timesheets', 'content': 'Timesheets Settings'},
                {'name': 'leave', 'label': 'Leave', 'content': 'Leave Settings'},
                {'name': 'expenses', 'label': 'Expenses', 'content': 'Expenses Settings'},
            ]
            self.tabs = Tabs(tabs_config=tabs_config)

            self.content = f'<div id="{self.data_file.container_id}" style="width: 300px;"></div>'
            self.content += f'<div id="{self.data_fil2.container_id}"></div>'
            self.content += f'<div id="{self.text_input.container_id}"></div>'
            self.content += f'<div id="{self.number_input.container_id}"></div>'
            self.content += f'<div id="{self.multiline_input.container_id}"></div>'
            self.content += f'<div id="{self.date_input.container_id}"></div>'
            self.content += f"<div id='{self.tabs.container_id}'></div>"

        super().__init__(page_title=title, content=self.content, overflow='auto', **kwargs)


    def form_show(self, **args):
        super().form_show(**args)
        if self.account is None:
            self.error_message.show()
        elif len(self.account['data_files']) > 1:
            self.data_file.show()
            self.data_fil2.show()
            self.text_input.show()
            self.number_input.show()
            self.multiline_input.show()
            self.date_input.show()
            self.tabs.form_show()
            print('1', self.data_file.options)
            print('2', self.data_fil2.options)
            control = self.data_fil2.control
            for k in control.model.keys():
                print(k, control.model[k])

    def data_file_selected(self, args):
        print('data_file_selected', args)
        print('1', self.data_file.value)
        # print('2', self.data_fil2.value)
