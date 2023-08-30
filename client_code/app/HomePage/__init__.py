import anvil.users
from ._anvil_designer import AdminHomeTemplate
from anvil.js.window import jQuery, ej
from AnvilFusion.tools.utils import AppEnv, init_user_session
from V3.app import models as v3_models
from ... import Forms
from ... import Views
from ... import Pages
import navigation as nav


AppEnv.APP_ID = 'PayLog'
AppEnv.data_models = v3_models
AppEnv.forms = Forms
AppEnv.views = Views
AppEnv.pages = Pages
AppEnv.grid_settings  = {
#   'modes': ['Sort', 'Filter', 'InfiniteScroll', 'Edit', 'ForeignKey', 'Toolbar'],
#   'toolbar_items': [
#     {'text': 'Add', 'prefixIcon': 'e-add', 'cssClass': '', 'style': 'background-color:#87CEEB; color:white;'},
#     {'text': 'Edit', 'prefixIcon': 'e-edit', 'cssClass': '', 'style': 'background-color:#98FB98; color:white;'},
#     {'text': 'Delete', 'prefixIcon': 'e-delete', 'cssClass': '', 'style': 'background-color:#FF6347; color:white;'},
#     {'text': 'Search'},
#     {'text': '', 'prefixIcon': 'e-add', 'align': 'Right'},
#     {'text': '', 'prefixIcon': 'e-search', 'align': 'Right'},
#   ],
#   'commands': [
#
#   ],
#   'command_column': {'headerText': '', 'width': 80, 'visible': True},
#   'top_indent': 25,
#   'column_width': 150,
}


class HomePage(HomePageTemplate):
    def __init__(self, **properties):
        AppEnv.logged_user = init_user_session()
        AppEnv.add_enumerations(model_list=v3_models.ENUM_MODEL_LIST)

        self.content_id = 'va-content'
        self.content_control = None

        # Appbar configuration
        self.appbar = ej.navigations.AppBar({'colorMode': 'Primary', 'isSticky': True})
        self.appbar_logo = ej.buttons.Button({'cssClass': 'e-inherit'})
        self.appbar_sidebar_toggle = ej.buttons.Button(
            {'cssClass': 'e-inherit', 'iconCss': 'fa-solid fa-bars va-appbar-menu-icon'})
        self.appbar_notification_list = ej.splitbuttons.DropDownButton({
            'cssClass': 'e-inherit e-caret-hide va-menu-font',
            'iconCss': 'fa-solid fa-bell va-appbar-menu-icon',
            'items': [{'text': 'No new notifications', 'disabled': True}],
            'open': self.appbar_menu_popup_open
        })
        appbar_user_menu_items = [
            {'text': 'Admin<br>admin@100rails.com', 'disabled': True, 'id': 'va-appbar-user-account-name'},
            {'text': 'Account', 'iconCss': 'fa-regular fa-user-gear', 'id': 'va-appbar-user-settings'},
            {'text': 'Sign Out', 'iconCss': 'fa-regular fa-arrow-right-from-bracket', 'id': 'va-appbar-sign-out'},
        ]
        self.appbar_user_menu = ej.splitbuttons.DropDownButton({
            'cssClass': 'e-inherit e-caret-hide va-menu-font',
            'iconCss': 'fa-solid fa-user va-appbar-menu-icon',
            'items': appbar_user_menu_items,
            'open': self.appbar_menu_popup_open
        })

        self.sidebar = nav.Sidebar(target_el='.va-page-container', container_el='va-sidebar',
                                   content_id=self.content_id)
        self.appbar_menu = nav.AppbarMenu(container_el='va-appbar-menu', sidebar=self.sidebar,
                                          menu_items=nav.VA_APPBAR_MENU)

    def form_show(self, **event_args):
        # Append appbar controls to elements
        self.appbar.appendTo(jQuery('#va-appbar')[0])
        self.appbar_notification_list.appendTo(jQuery('#va-appbar-notification-list')[0])
        self.appbar_user_menu.appendTo(jQuery('#va-appbar-user-menu')[0])
        self.appbar_sidebar_toggle.appendTo(jQuery('#va-appbar-sidebar-toggle')[0])
        self.appbar_sidebar_toggle.element.addEventListener('click', self.sidebar.toggle)
        self.appbar_menu.show()

        # Show sidebar menu
        self.sidebar.show('tenant_menu')

        # Show start page

    # Sidebar toggle event handler
    def sidebar_toggle(self, args):
        self.sidebar.toggle()

    # Appbar menu popup window position adjustment
    @staticmethod
    def appbar_menu_popup_open(args):
        args.element.parentElement.style.top = str(float(args.element.parentElement.style.top[:-2]) + 10) + 'px'

    # Sidebar menu popup window position adjustment
    @staticmethod
    def sidebar_menu_popup_open(args):
        args.element.parentElement.style.top = str(
            args.element.getBoundingClientRect().top - args.element.parentElement.offsetHeight + 44) + 'px'
        args.element.parentElement.style.left = '100px'


    def appbar_add_item_select(self, args):
        nav.add_item_select(args, self.content_id)
