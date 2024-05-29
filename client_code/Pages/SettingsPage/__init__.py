from AnvilFusion.components.PageBase import PageBase
from AnvilFusion.components.FormInputs import *
from AnvilFusion.components.Inputs import InplaceEditor
from AnvilFusion.components.Layouts import Tabs
from AnvilFusion.tools.utils import AppEnv
from ...app.models import Account, Tenant, PayrollConfig
import datetime
import time


class SettingsPage(PageBase):
    def __init__(self, account=None, **kwargs):
        print('SettingsPage')
        title = ''
        self.account = account
        if self.account is None:
            self.tenant = Tenant.get(AppEnv.logged_user.tenant_uid)
            self.account = Account.get(self.tenant['account_uid'])

        if self.account is None:
            self.error_message = InlineMessage(content='No account found', accent='warning', css_class='pl-message-bar')
            self.content = f'<div id="{self.error_message.container_id}"></div>'

        else:
            tabs_config = [
                {'name': 'account', 'label': 'Account Info', 'content': 'Payroll Settings'},
                {'name': 'timesheets', 'label': 'Timesheets', 'content': 'Timesheets Settings'},
                {'name': 'leave', 'label': 'Leave', 'content': 'Leave Settings'},
                {'name': 'expenses', 'label': 'Expenses', 'content': 'Expenses Settings'},
            ]
            self.settings_tabs = Tabs(tabs_config=tabs_config)
            self.content = f'<div id="{self.settings_tabs.container_id}"></div>'

        super().__init__(page_title=title, content=self.content, overflow='auto', **kwargs)


    def form_show(self, **args):
        print('SettingsPage form_show')
        super().form_show(**args)
        print('super show end')
        if self.account is None:
            self.error_message.show()
        else:
            self.settings_tabs.form_show()
            print(self.settings_tabs.tabs.items)
