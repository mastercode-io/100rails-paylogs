from AnvilFusion.components.PageBase import PageBase
from AnvilFusion.components.FormInputs import *
from AnvilFusion.tools.utils import AppEnv
from ..app.models import Account, Tenant, PayrollConfig


class PayrollSettingsPage(PageBase):
    def __init__(self, account=None, **kwargs):
        print('PayrollSettingsPage')
        title = ''
        if account is None:
            tenant = Tenant.get_row(AppEnv.logged_user.tenant_uid)
            account = next(iter(Account.search(data_files=[tenant])), None)
            print(account, tenant)
        if account is not None:
            options = account['data_files']
        else:
            options = []

        self.data_file = DropdownInput(name='data_file',
                                       label='Select Data File',
                                       text_field='integration.service_name',
                                       options=options)
        # self.import_button = Button(content='Import Timesheets',
        #                             action=self.import_button_action)
        self.content = f'<br><div id="{self.data_file.container_id}" style="width:300px;"></div>'

        super().__init__(page_title=title, content=self.content, overflow='auto', **kwargs)


    def form_show(self, **args):
        super().form_show(**args)
        self.data_file.show()
