# Application navigation
from anvil.js.window import jQuery, ej, Event
import anvil.js
import time
from AnvilFusion.tools.utils import AppEnv
from AnvilFusion.datamodel import migrate
from AnvilFusion.components.GridView import GridView
from AnvilFusion.components.FormBase import FormBase
from AnvilFusion.features.developer.MigratePage import MigratePage
from ...Pages.CopilotChat import AssistantChat


# Sidebar control CSS
PL_SIDEBAR_CSS = 'e-inherit e-caret-hide pm-sidebar-menu'
PL_SIDEBAR_WIDTH = 200
PL_SIDEBAR_POPUP_OFFSET = 1
PL_ASSISTANT_WIDTH = 300


# Appbar menu item list
PL_APPBAR_MENU = [
    {'id': 'timesheet_menu', 'text': 'Timesheet', 'items': []},
    {'id': 'payroll_menu', 'text': 'Payroll', 'items': []},
    {'id': 'business_menu', 'text': 'Business', 'items': []},
]
PL_APPBAR_MENU_ADMIN = [
    {'separator': True},
    {'id': 'admin_menu', 'text': 'Admin', 'items': []},
]
PL_APPBAR_MENU_DEVELOPER = [
    {'id': 'developer_menu', 'text': 'Developer', 'items': []},
]


# Sidebar menu item list
PL_SIDEBAR_MENUS = {
    'timesheet_menu': [
        {'nodeId': 'timesheet_manage', 'nodeText': 'Manage Timesheets', 'nodeChild': []},
        {'nodeId': 'timesheet_payroll', 'nodeText': 'Payroll Timesheets', 'nodeChild': []},
    ],
    'payroll_menu': [
        {'nodeId': 'payroll_payrun_report', 'nodeText': 'Payrun Report', 'nodeChild': []},
        {'nodeId': 'payroll_payrun_list', 'nodeText': 'Payruns', 'nodeChild': []},
        {'nodeId': 'payroll_payrun_config', 'nodeText': 'Payrun Config', 'nodeChild': []},
        # {'nodeId': 'views_', 'nodeText': '', 'nodeChild': []},
        # {'nodeId': 'views_', 'nodeText': '', 'nodeChild': []},
    ],
    'business_menu': [
        {'nodeId': 'business_company', 'nodeText': 'Company Info', 'nodeChild': []},
        {'nodeId': 'business_employees', 'nodeText': 'Employees', 'nodeChild': []},
        {'nodeId': 'business_jobs', 'nodeText': 'Jobs', 'nodeChild': []},
    ],
    'settings_menu': [
        {'nodeId': 'settings_users', 'nodeText': 'Users', 'nodeChild': []},
        {'nodeId': 'settings_locations', 'nodeText': 'Locations', 'nodeChild': []},
        {'nodeId': 'settings_employee_roles', 'nodeText': 'Employee Roles', 'nodeChild': []},
        {'nodeId': 'settings_job_types', 'nodeText': 'Job Types', 'nodeChild': []},
        {'nodeId': 'settings_timesheet_types', 'nodeText': 'Timesheet Types', 'nodeChild': []},
        {'nodeId': 'settings_pay_categories', 'nodeText': 'Pay Categories', 'nodeChild': []},
        {'nodeId': 'settings_pay_rate_rules', 'nodeText': 'Pay Rate Rules', 'nodeChild': []},
        {'nodeId': 'settings_pay_rate_scopes', 'nodeText': 'Pay Rate Scopes', 'nodeChild': []},
        {'nodeId': 'settings_pay_rate_templates', 'nodeText': 'Pay Rate Templates', 'nodeChild': []},
        {'nodeId': 'settings_calendar', 'nodeText': 'Calendar', 'nodeChild': []},
        {'nodeId': 'settings_import_records', 'nodeText': 'Import Records', 'nodeChild': []},
    ],
    'admin_menu': [
        {'nodeId': 'admin_tenants', 'nodeText': 'Tenants', 'nodeChild': []},
        {'nodeId': 'admin_user_roles', 'nodeText': 'User Roles', 'nodeChild': []},
        {'nodeId': 'admin_permissions', 'nodeText': 'Permissions', 'nodeChild': []},
        {'nodeId': 'admin_settings', 'nodeText': 'Settings', 'nodeChild': [
            {'nodeId': 'admin_settings_scope_types', 'nodeText': 'Scope Types', 'nodeChild': []},
        ]},

    ],
    'developer_menu': [
        {'nodeId': 'developer_components', 'nodeText': 'Components', 'nodeChild': [
            {'nodeId': 'developer_views', 'nodeText': 'Views', 'nodeChild': []},
            {'nodeId': 'developer_pages', 'nodeText': 'Pages', 'nodeChild': []},
            {'nodeId': 'developer_forms', 'nodeText': 'Forms', 'nodeChild': []},
        ]},
        {'nodeId': 'developer_schema', 'nodeText': 'App Schema', 'nodeChild': [
            {'nodeId': 'developer_models', 'nodeText': 'Models', 'nodeChild': []},
            {'nodeId': 'developer_migrate', 'nodeText': 'Migrate DB', 'nodeChild': []},
        ]},
        {'nodeId': 'developer_tools', 'nodeText': 'Tools', 'nodeChild': [
            {'nodeId': 'developer_import', 'nodeText': 'Import Data', 'nodeChild': []},
            {'nodeId': 'developer_export', 'nodeText': 'Export Data', 'nodeChild': []},
        ]},
        {'nodeId': 'developer_preview', 'nodeText': 'Developer Preview', 'nodeChild': [
            {'nodeId': 'developer_form_preview', 'nodeText': 'Form Preview', 'nodeChild': []},
            {'nodeId': 'developer_grid_preview', 'nodeText': 'Grid View Preview', 'nodeChild': []},
            {'nodeId': 'developer_page_preview', 'nodeText': 'Page Preview', 'nodeChild': []},
        ]},
    ]
}


# Navigation items/actions
PL_NAV_ITEMS = {
    'timesheet_manage': {'class': 'TimesheetListView', 'type': 'custom', 'action': 'open', 'props': {}},
    'timesheet_payroll': {'model': 'Timesheet', 'type': 'view', 'action': 'open', 'props': {}},

    'payroll_payrun_report': {'model': 'Payrun', 'type': 'view', 'action': 'open', 'props': {}},
    'payroll_payrun_list': {'model': 'Payrun', 'type': 'view', 'action': 'open', 'props': {}},
    'payroll_payrun_config': {'model': 'PayrunConfig', 'type': 'form', 'action': 'open', 'props': {}},

    'business_company': {'name': 'CompanyDashboardPage', 'type': 'page', 'action': 'open', 'props': {}},
    'business_employees': {'model': 'Employee', 'type': 'view', 'action': 'open', 'props': {}},
    'business_jobs': {'model': 'Job', 'type': 'view', 'action': 'open', 'props': {}},

    'settings_users': {'model': 'User', 'type': 'view', 'action': 'open', 'props': {}},
    'settings_locations': {'model': 'Location', 'type': 'view', 'action': 'open', 'props': {}},
    'settings_employee_roles': {'model': 'EmployeeRole', 'type': 'view', 'action': 'open', 'props': {}},
    'settings_job_types': {'model': 'JobType', 'type': 'view', 'action': 'open', 'props': {}},
    'settings_timesheet_types': {'model': 'TimesheetType', 'type': 'view', 'action': 'open', 'props': {}},
    'settings_pay_categories': {'model': 'PayCategory', 'type': 'view', 'action': 'open', 'props': {}},
    'settings_pay_rate_rules': {'model': 'PayRateRule', 'type': 'view', 'action': 'open', 'props': {}},
    'settings_pay_rate_scopes': {'model': 'Scope', 'type': 'view', 'action': 'open', 'props': {}},
    'settings_pay_rate_templates': {'model': 'PayRateTemplate', 'type': 'view', 'action': 'open', 'props': {}},
    'settings_calendar': {'type': 'page', 'name': 'CalendarPage', 'action': 'open', 'props': {}},
    'settings_import_records': {'type': 'page', 'name': 'ImportRecordsPage', 'action': 'open', 'props': {}},

    'admin_tenants': {'class': 'TenantsView', 'type': 'custom', 'action': 'open', 'props': {}},
    'admin_users': {'model': 'User', 'type': 'view', 'action': 'open', 'props': {}},
    'admin_settings_scope_types': {'model': 'ScopeType', 'type': 'view', 'action': 'open', 'props': {}},
    # 'admin_user_roles': {'model': 'UserRole', 'type': 'view', 'action': 'open', 'props': {}},
    # 'admin_permissions': {'model': 'Permission', 'type': 'view', 'action': 'open', 'props': {}},
    # 'admin_settings': {'model': 'Setting', 'type': 'view', 'action': 'open', 'props': {}},

    'developer_views': {'model': 'AppGridView', 'type': 'view', 'action': 'open', 'props': {}},
    # 'developer_pages': {'model': 'Page', 'type': 'view', 'action': 'open', 'props': {}},
    # 'developer_forms': {'model': 'Form', 'type': 'view', 'action': 'open', 'props': {}},
    # 'developer_models': {'model': 'Model', 'type': 'view', 'action': 'open', 'props': {}},
    # 'developer_migrate': {'type': 'function', 'function': migrate.migrate_db_schema, 'props': {}},
    'developer_migrate': {'type': 'page', 'page': MigratePage, 'props': {}},
    'developer_form_preview': {'type': 'form', 'class': 'TenantForm', 'props': {}},
    # 'developer_grid_preview': {'type': 'page', 'page': MigratePage, 'props': {}},
    # 'developer_page_preview': {'type': 'page', 'page': MigratePage, 'props': {}},
}

PL_DEFAULT_NAV_ITEMS = {
    'timesheet_menu': 'timesheet_manage',
    'payroll_menu': 'payroll_payrun_report',
    'business_menu': 'business_company',
    'settings_menu': 'settings_users',
    'admin_menu': 'admin_tenants',
    'developer_menu': 'developer_views',
}


# Appbar navigation class
class AppbarMenu:
    def __init__(self, container_el, sidebar, menu_items):
        self.container_el = container_el
        self.sidebar = sidebar
        self.menu_items = menu_items
        self.selected_el = None
        self.menu = None


    def show(self):
        print('AppBar Show')
        if self.menu:
            self.menu.items = self.menu_items
        else:
            self.menu = ej.navigations.Menu({
                'cssClass': 'e-inherit',
                'items': self.menu_items,
                'select': self.menu_select
            })
            self.menu.appendTo(jQuery(f"#{self.container_el}")[0])


    def menu_select(self, args):
        if self.selected_el is not None:
            self.selected_el.classList.remove('pl-appbar-menu-selected')
        self.selected_el = args.element
        self.selected_el.classList.add('pl-appbar-menu-selected')
        menu_id = args.item.properties.id
        print(menu_id)
        self.sidebar.show_menu(menu_id)


class Assistant:
    def __init__(self,
                 target_el,
                 container_id,
                 content_id,
                 sidebar_width=PL_ASSISTANT_WIDTH,
                 **properties):

        self.target_el = target_el
        self.container_id = container_id
        self.content_id = content_id
        self.nav_target_id = None
        self.sidebar_width = sidebar_width
        self.content_control = None
        self.control = None
        self.chat = None
        self.open = False
        self.toggled = False


    # Show sidebar menu
    def show(self):
        print('show assistant')
        if not self.control:
            self.control = ej.navigations.Sidebar({
                'width': self.sidebar_width,
                'target': self.target_el,
                # 'mediaQuery': '(min-width: 600px)',
                'isOpen': False,
                'animate': False,
                'position': 'Right',
                'type': 'Push',
                # 'open': self.sidebar_event,
                # 'close': self.sidebar_event,
            })
            self.control.appendTo(f"#{self.container_id}")
            self.chat = CopilotChat(container_id=self.container_id)
            # container_el = anvil.js.window.document.getElementById(self.container_id)
            # container_el.innerHTML = f'''
            #     <div id="pl-assistant-container" style="margin: 5px; height: 100%;">
            #         <h5 id="pl-assistant-header" style="margin-top: 15px;">PayLogs Assistant</h5>
            #         <div id="pl-assistant-chat" style="height: 90%;"><div>
            #     </div>
            # '''
            # self.chat = jQuery(f"#pl-assistant-chat").kendoChat({
            #     'post': self.chat_post,
            #     'height': '85%',
            # }).data('kendoChat')
            # self.chat = AssistantChat(container_id='pl-assistant-chat')
            # self.chat.form_show()
            self.control.hide()



    # Sidebar toggle
    def toggle(self, args):
        # print('toggle assistant')
        self.toggled = True
        if self.open:
            self.control.hide()
            self.open = False
        else:
            self.control.show()
            self.open = True
        # AppEnv.navigation.refresh_content()
        # time.sleep(0.5)
        # resize_event = anvil.js.new(Event, 'resize')
        # anvil.js.window.dispatchEvent(resize_event)
        # if not self.open:
        #     self.control.hide()


    def sidebar_event(self, args):
        if self.toggled:
            self.toggled = False
            args.cancel = True
            print('assistant toggled', args)
        else:
            print('assistant event', args)
        # if self.open:
        #     self.control.show()
        # else:
        #     self.control.hide()



# Sidebar navigation class
class Sidebar:
    def __init__(self,
                 target_el,
                 container_id,
                 content_id,
                 sidebar_width=PL_SIDEBAR_WIDTH,
                 sections=None,
                 nav_items=None,
                 **properties):

        if sections is None:
            sections = PL_SIDEBAR_MENUS
        if nav_items is None:
            nav_items = PL_NAV_ITEMS
        self.target_el = target_el
        self.container_id = container_id
        self.content_id = content_id
        self.nav_target_id = None
        self.sidebar_width = sidebar_width
        self.content_control = None
        self.nav_items = nav_items
        self.control = None
        self.menu = None
        self.open = True


    # Show sidebar menu
    def show(self, menu_id):
        print('show', menu_id)
        if not self.menu:
            self.menu = ej.navigations.TreeView({
                'fields': {
                    'cssClass': PL_SIDEBAR_CSS,
                    'dataSource': '',
                    'id': 'nodeId',
                    'text': 'nodeText',
                    'child': 'nodeChild'
                },
                'expandOn': 'Click',
                'nodeSelected': self.menu_select,
            })
            self.menu.appendTo(jQuery(f"#{self.container_id}-menu")[0])

        if not self.control:
            self.control = ej.navigations.Sidebar({
                'width': self.sidebar_width,
                'target': self.target_el,
                # 'mediaQuery': '(min-width: 600px)',
                'isOpen': True,
                'animate': False,
                'type': 'Push',
                # 'open': self.sidebar_event,
                # 'close': self.sidebar_event,
            })
            self.control.appendTo(f"#{self.container_id}")

        self.show_menu(menu_id)


    # Sidebar toggle
    def toggle(self, args):
        if self.open:
            self.open = False
            self.control.hide()
        else:
            self.open = True
            self.control.show()
        # self.refresh_content()
        # time.sleep(0.5)
        # resize_event = anvil.js.new(Event, 'resize')
        # anvil.js.window.dispatchEvent(resize_event)
        # if not self.open:
        #     self.control.hide()


    def sidebar_event(self, args):
        print('sidebar event', args)
        if args.name == 'open' and self.open:
            args.cancel = True
        elif args.name == 'close' and not self.open:
            args.cancel = True


    def show_menu(self, menu_id):
        # self.menu.fields.dataSource = PL_SIDEBAR_MENUS.get(menu_id, list(PL_SIDEBAR_MENUS.keys())[0])
        if menu_id in PL_SIDEBAR_MENUS:
            subcomponent = PL_DEFAULT_NAV_ITEMS.get(menu_id)
            if not subcomponent:
                subcomponent = PL_SIDEBAR_MENUS[menu_id][0]['nodeId']
            menu_items = PL_SIDEBAR_MENUS[menu_id]
            for item in menu_items:
                if item['nodeId'] == subcomponent:
                    item['selected'] = True
                    item['expanded'] = True
            self.menu.fields.dataSource = menu_items
            self.menu_select(None, subcomponent=subcomponent)


    def menu_select(self, args, subcomponent=None):
        if subcomponent is None:
            if 'e-level-1' in list(args.node.classList):
                # print('Accordion')
                self.menu.collapseAll()
                self.menu.expandAll([args.node])
                self.nav_target_id = None

            menu_item_id = args.nodeData.id
            component = PL_NAV_ITEMS[menu_item_id] if menu_item_id in PL_NAV_ITEMS else None
        else:
            component = PL_NAV_ITEMS.get(subcomponent)
        if component is None:
            return

        if self.content_control is not None and self.nav_target_id is None:
            self.content_control.destroy()

        nav_container_id = self.content_id if self.nav_target_id is None else self.nav_target_id
        if component['type'] == 'custom':
            try:
                view_class = getattr(AppEnv.views, component['class'])
                self.content_control = view_class(container_id=nav_container_id,**component.get('props', {}))
            except Exception as e:
                print(e)

        if component['type'] == 'view':
            if 'config' in component:
                self.content_control = GridView(view_name=component['config'],
                                                container_id=nav_container_id,
                                                **component.get('props', {}))
            elif hasattr(AppEnv.views, f"{component['model']}View"):
                view_class = getattr(AppEnv.views, f"{component['model']}View")
                self.content_control = view_class(container_id=nav_container_id,
                                                  **component.get('props', {}))
            else:
                self.content_control = GridView(model=component['model'],
                                                container_id=nav_container_id,
                                                **component.get('props', {}))

        elif component['type'] == 'form':
            print('form', component)
            # try:
            form_class = getattr(AppEnv.forms, component.get('class', f"{component.get('model')}Form"))
            self.content_control = form_class(target=nav_container_id)
            # except Exception as e:
            #     print(e.args)
            #     self.content_control = FormBase(model=component.get('model'), target=nav_container_id)

        elif component['type'] == 'page':
            print('page', component)
            try:
                if component.get('page', None):
                    page_class = component['page']
                else:
                    page_class = getattr(AppEnv.pages, f"{component['name']}")
                self.content_control = page_class(container_id=nav_container_id, **component.get('props', {}))
            except Exception as e:
                print('Exception', e.args)
                # self.content_control = Pages.BaseForm(model=component['model'], target=self.content_id)
        elif component['type'] == 'function':
            try:
                func_name = component['function']
                if callable(func_name):
                    func_name(**component.get('props', {}))
            except Exception as e:
                print(e.args)
            return

        if hasattr(self.content_control, 'target_id'):
            self.nav_target_id = self.content_control.target_id

        # try:
        self.content_control.form_show()
        # except Exception as e:
        #     print(e)
        if self.control.isOpen:
            self.control.toggle()
            self.control.toggle()

        if 'subcomponent' in component:
            time.sleep(0.5)
            self.menu_select(None, subcomponent=component['subcomponent'])


    def refresh_content(self):
        if self.content_control:
            try:
                self.content_control.refresh()
            except Exception as e:
                pass
