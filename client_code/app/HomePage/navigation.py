# Application navigation
from anvil.js.window import jQuery, ej
import sys
import time
from AnvilFusion.tools.utils import AppEnv
from AnvilFusion.components.GridView import GridView
from AnvilFusion.components.FormBase import FormBase


# Sidebar control CSS
VA_SIDEBAR_CSS = 'e-inherit e-caret-hide pm-sidebar-menu'
VA_SIDEBAR_WIDTH = 200
VA_SIDEBAR_POPUP_OFFSET = 1


# Appbar menu item list
VA_APPBAR_MENU = [
    {'id': 'tenant_menu', 'text': 'Tenants', 'items': []},
    {'id': 'views_menu', 'text': 'Views', 'items': []},
    {'id': 'tools_menu', 'text': 'Tools', 'items': []},
]


# Sidebar menu item list
VA_SIDEBAR_MENUS = {
    'tenant_menu': [
        {'nodeId': 'tenant_info', 'nodeText': 'Account Info', 'nodeChild': []},
        {'nodeId': 'tenant_users', 'nodeText': 'Users', 'nodeChild': []},
        {'nodeId': 'tenant_settings', 'nodeText': 'Settings', 'nodeChild': []},
        {'nodeId': 'tenant_customisations', 'nodeText': 'Customisations', 'nodeChild': []},
        {'nodeId': 'tenant_integrations', 'nodeText': 'Integrations', 'nodeChild': []},
        {'nodeId': 'tenant_billing', 'nodeText': 'Billing', 'nodeChild': []},
    ],
    'views_menu': [
        {'nodeId': 'views_default', 'nodeText': 'Default Views', 'nodeChild': []},
        # {'nodeId': 'views_', 'nodeText': '', 'nodeChild': []},
        # {'nodeId': 'views_', 'nodeText': '', 'nodeChild': []},
    ],
    'tools_menu': [
        {'nodeId': 'tools_logs', 'nodeText': 'System Logs', 'nodeChild': []},
        {'nodeId': 'tools_app_model', 'nodeText': 'Application Model', 'nodeChild': []},
        {'nodeId': 'tools_migrate_db', 'nodeText': 'Migrate DB', 'nodeChild': []},
        # {'nodeId': 'tools_', 'nodeText': '', 'nodeChild': []},
    ],
}


# Navigation items/actions
VA_NAV_ITEMS = {
    # 'case_agenda': {'model': '', 'type': 'page|view|form', 'action': 'open|popup', 'props': {}},
    'views_default': {'model': 'appGridViews', 'type': 'view', 'action': 'open', 'props': {}},
}


# Appbar navigation class
class AppbarMenu:
    def __init__(self, container_el, sidebar, menu_items):
        self.container_el = container_el
        self.sidebar = sidebar
        self.menu_items = menu_items
        self.selected_el = None

        self.menu = ej.navigations.Menu({
            'cssClass': 'e-inherit',
            'items': self.menu_items,
            'select': self.menu_select
        })


    def show(self):
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
                 sidebar_width=VA_SIDEBAR_WIDTH,
                 sections=VA_SIDEBAR_MENUS,
                 nav_items=VA_NAV_ITEMS,
                 **properties):

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
                'cssClass': VA_SIDEBAR_CSS,
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
        self.menu.appendTo(jQuery(f"#{self.container_el}-menu")[0])
        self.control.appendTo(jQuery(f"#{self.container_el}")[0])
        self.show_menu(menu_id)


    # Sidebar toggle
    def toggle(self, args):
        self.control.toggle()


    def show_menu(self, menu_id):
        self.menu.fields.dataSource = VA_SIDEBAR_MENUS[menu_id]


    def menu_select(self, args, subcomponent=None):
        if subcomponent is None:
            if 'e-level-1' in list(args.node.classList):
                print('Accordion')
                self.menu.collapseAll()
                self.menu.expandAll([args.node])
                self.nav_target_id = None

            menu_item_id = args.nodeData.id
            print(menu_item_id)
            component = VA_NAV_ITEMS[menu_item_id] if menu_item_id in VA_NAV_ITEMS else None
        else:
            component = VA_NAV_ITEMS[subcomponent]
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
            try:
                form_class = getattr(AppEnv.forms, f"{component['model']}Form")
                self.content_control = form_class(target=nav_container_id)
            except Exception as e:
                print(e.args)
                self.content_control = FormBase(model=component['model'], target=nav_container_id)

        elif component['type'] == 'page':
            try:
                page_class = getattr(AppEnv.pages, f"{component['model']}Page")
                self.content_control = page_class(container_id=nav_container_id)
            except Exception as e:
                print(e.args)
                # self.content_control = Pages.BaseForm(model=component['model'], target=self.content_id)

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
