from AnvilFusion.components.PageBase import PageBase
from AnvilFusion.components.FormInputs import *
from AnvilFusion.tools.utils import AppEnv
from ...app.models import Account, Tenant, PayrollConfig


class SettingsPage(PageBase):
    def __init__(self, account=None, **kwargs):
        print('SettingsPage')
        title = ''
        self.account = account
        if self.account is None:
            tenant = Tenant.get_row(AppEnv.logged_user.tenant_uid)
            self.account = next(iter(Account.search(data_files=[tenant])), None)
        print(self.account, self.account['data_files'])
        for data_file in self.account['data_files']:
            print(data_file['uid'], data_file['name'])

        if self.account is not None:
            self.error_message = InlineMessage(content='No account found', accent='error')
            self.content = f'<div id="{self.error_message.container_id}"></div>'

        elif len(self.account['data_files']) > 1:
            options = self.account['data_files']
            self.data_file = DropdownInput(name='data_file',
                                           label='Select Data File',
                                           text_field='integration.service_name',
                                           options=options)
            self.content = f'<div id="{self.data_file.container_id}" style="width:300px;"></div>'

        super().__init__(page_title=title, content=self.content, overflow='auto', **kwargs)


    def form_show(self, **args):
        super().form_show(**args)
        if self.account is not None:
            self.error_message.show()
        elif len(self.account['data_files']) > 1:
            self.data_file.show()
