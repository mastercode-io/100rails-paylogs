# Application navigation
from anvil.js.window import jQuery, ej
import time
from AnvilFusion.tools.utils import AppEnv
from AnvilFusion.datamodel import migrate
from AnvilFusion.components.GridView import GridView
from AnvilFusion.components.FormBase import FormBase
from AnvilFusion.features.developer.MigratePage import MigratePage


# Sidebar control CSS
PL_SIDEBAR_CSS = 'e-inherit e-caret-hide pm-sidebar-menu'
PL_SIDEBAR_WIDTH = 200
PL_SIDEBAR_POPUP_OFFSET = 1


# Appbar menu item list
PL_APPBAR_MENU = [
    {'id': 'timesheet_menu', 'text': 'Timesheet', 'items': []},
    {'id': 'payroll_menu', 'text': 'Payroll', 'items': []},
    {'id': 'business_menu', 'text': 'Business', 'items': []},
]
PL_APPBAR_MENU_ADMIN = [
    {'separator': True},
    {'id': 'admin_menu', 'text': 'Admin', 'items': []},
    {'id': 'developer_menu', 'text': 'Developer', 'items': []},
]


# Sidebar menu item list
PL_SIDEBAR_MENUS = {
    'timesheet_menu': [
        {'nodeId': 'timesheet_manage', 'nodeText': 'Manage Timesheet', 'nodeChild': []},
        {'nodeId': 'timesheet_payroll', 'nodeText': 'Payroll Timesheet', 'nodeChild': []},
    ],
    'payroll_menu': [
        {'nodeId': 'payroll_payrun_report', 'nodeText': 'Payrun Report', 'nodeChild': []},
        # {'nodeId': 'views_', 'nodeText': '', 'nodeChild': []},
        # {'nodeId': 'views_', 'nodeText': '', 'nodeChild': []},
    ],
    'business_menu': [
        {'nodeId': 'business_company', 'nodeText': 'Company Info', 'nodeChild': []},
        {'nodeId': 'business_locations', 'nodeText': 'Locations', 'nodeChild': []},
        {'nodeId': 'business_employees', 'nodeText': 'Employees', 'nodeChild': []},
        # {'nodeId': 'tools_', 'nodeText': '', 'nodeChild': []},
    ],
    'settings_menu': [
        {'nodeId': 'settings_job_types', 'nodeText': 'Job Types', 'nodeChild': []},
        {'nodeId': 'settings_job_settings', 'nodeText': 'Job Settings', 'nodeChild': []},
        {'nodeId': 'settings_employee_roles', 'nodeText': 'Employee Roles', 'nodeChild': []},
        {'nodeId': 'settings_pay_categories', 'nodeText': 'Pay Categories', 'nodeChild': []},
        {'nodeId': 'settings_timesheet_types', 'nodeText': 'Timesheet Types', 'nodeChild': []},
        # {'nodeId': 'tools_', 'nodeText': '', 'nodeChild': []},
    ],
    'admin_menu': [
        {'nodeId': 'admin_tenants', 'nodeText': 'Tenants', 'nodeChild': []},
        {'nodeId': 'admin_users', 'nodeText': 'Users', 'nodeChild': []},
        {'nodeId': 'admin_user_roles', 'nodeText': 'User Roles', 'nodeChild': []},
        {'nodeId': 'admin_permissions', 'nodeText': 'Permissions', 'nodeChild': []},
        {'nodeId': 'admin_settings', 'nodeText': 'Settings', 'nodeChild': []},

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
            {'nodeId': 'developer_form_preview', 'nodeText': 'Form Prview', 'nodeChild': []},
            {'nodeId': 'developer_grid_preview', 'nodeText': 'Grid View Preview', 'nodeChild': []},
            {'nodeId': 'developer_page_preview', 'nodeText': 'Page Preview', 'nodeChild': []},
        ]},
    ]
}


# Navigation items/actions
PL_NAV_ITEMS = {
    'timesheet_manage': {'model': 'Timesheet', 'type': 'view', 'action': 'open', 'props': {}},
    'timesheet_payroll': {'model': 'Timesheet', 'type': 'view', 'action': 'open', 'props': {}},

    'payroll_payrun_report': {'model': 'PayRun', 'type': 'view', 'action': 'open', 'props': {}},

    'business_company': {'name': 'CompanyDashboardPage', 'type': 'page', 'action': 'open', 'props': {}},
    'business_locations': {'model': 'Location', 'type': 'view', 'action': 'open', 'props': {}},
    'business_employees': {'model': 'Employee', 'type': 'view', 'action': 'open', 'props': {}},

    'settings_job_types': {'model': 'JobType', 'type': 'view', 'action': 'open', 'props': {}},
    # 'settings_job_settings': {'model': 'TimesheetType', 'type': 'view', 'action': 'open', 'props': {}},
    'settings_employee_roles': {'model': 'EmployeeRole', 'type': 'view', 'action': 'open', 'props': {}},
    'settings_pay_categories': {'model': 'PayCategory', 'type': 'view', 'action': 'open', 'props': {}},
    'settings_timesheet_types': {'model': 'TimesheetType', 'type': 'view', 'action': 'open', 'props': {}},

    'admin_tenants': {'model': 'Tenant', 'type': 'view', 'action': 'open', 'props': {}},
    'admin_users': {'model': 'User', 'type': 'view', 'action': 'open', 'props': {}},
    # 'admin_user_roles': {'model': 'UserRole', 'type': 'view', 'action': 'open', 'props': {}},
    # 'admin_permissions': {'model': 'Permission', 'type': 'view', 'action': 'open', 'props': {}},
    # 'admin_settings': {'model': 'Setting', 'type': 'view', 'action': 'open', 'props': {}},

    'developer_views': {'model': 'AppGridView', 'type': 'view', 'action': 'open', 'props': {}},
    # 'developer_pages': {'model': 'Page', 'type': 'view', 'action': 'open', 'props': {}},
    # 'developer_forms': {'model': 'Form', 'type': 'view', 'action': 'open', 'props': {}},
    # 'developer_models': {'model': 'Model', 'type': 'view', 'action': 'open', 'props': {}},
    # 'developer_migrate': {'type': 'function', 'function': migrate.migrate_db_schema, 'props': {}},
    'developer_migrate': {'type': 'page', 'page': MigratePage, 'props': {}},
    'developer_form_preview': {'type': 'form', 'class': 'CreateTenantForm', 'props': {}},
    # 'developer_grid_preview': {'type': 'page', 'page': MigratePage, 'props': {}},
    # 'developer_page_preview': {'type': 'page', 'page': MigratePage, 'props': {}},
}

PL_DEFAULT_NAV_ITEMS = {
    'timesheet_menu': 'timesheet_manage',
    'payroll_menu': 'payroll_payrun_report',
    'business_menu': 'business_company',
    'settings_menu': 'settings_job_types',
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


# Sidebar navigation class
class Sidebar:
    def __init__(self,
                 target_el,
                 container_el,
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
        self.container_el = container_el
        self.content_id = content_id
        self.nav_target_id = None
        self.content_control = None
        self.nav_items = nav_items

        # Init sidebar menu controls
        self.control = self.sidebar = ej.navigations.Sidebar({
            'width': sidebar_width,
            'target': self.target_el,
            'mediaQuery': '(min-width: 600px)',
            'isOpen': True,
            'animate': False,
        })

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


    # Show sidebar menu
    def show(self, menu_id):
        print('show', menu_id)
        self.menu.appendTo(jQuery(f"#{self.container_el}-menu")[0])
        self.control.appendTo(jQuery(f"#{self.container_el}")[0])
        self.show_menu(menu_id)


    # Sidebar toggle
    def toggle(self, args):
        self.control.toggle()


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
                self.content_control = view_class(container_id=nav_container_id)
            except Exception as e:
                print(e)

        if component['type'] == 'view':
            if 'config' in component:
                self.content_control = GridView(view_name=component['config'], container_id=nav_container_id)
            elif hasattr(AppEnv.views, f"{component['model']}View"):
                view_class = getattr(AppEnv.views, f"{component['model']}View")
                self.content_control = view_class(container_id=nav_container_id)
            else:
                self.content_control = GridView(model=component['model'], container_id=nav_container_id)

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
