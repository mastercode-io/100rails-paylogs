from AnvilFusion.components.PageBase import PageBase
from AnvilFusion.components.FormInputs import *
from AnvilFusion.tools.utils import AppEnv
from ...app.models import Account, Tenant, PayrollConfig


class SettingsPage(PageBase):
    def __init__(self, account=None, **kwargs):
        print('SettingsPage')
        title = ''
        if account is None:
            tenant = Tenant.get_row(AppEnv.logged_user.tenant_uid)
            account = next(iter(Account.search(data_files=[tenant])), None)
        print(account, account['data_files'])
        for data_file in account['data_files']:
            print(data_file['uid'], data_file['name'])

        if account is not None:
            self.error_message = InlineMessage(content='No account found', message_type='error')
            self.content = f'<div id="{self.error_message.container_id}"></div>'

        elif len(account['data_files']) > 1:
            options = account['data_files']
            self.data_file = DropdownInput(name='data_file',
                                           label='Select Data File',
                                           text_field='integration.service_name',
                                           options=options)
            self.content = f'<div id="{self.data_file.container_id}" style="width:300px;"></div>'

        super().__init__(page_title=title, content=self.content, overflow='auto', **kwargs)


    def form_show(self, **args):
        super().form_show(**args)
        self.data_file.show()
