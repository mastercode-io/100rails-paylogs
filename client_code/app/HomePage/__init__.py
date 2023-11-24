from ._anvil_designer import HomePageTemplate
import anvil.js
from anvil.js.window import ej, jQuery
# from anvil import get_url_hash
import anvil.users
from AnvilFusion.tools.utils import AppEnv, DotDict, init_user_session
from .. import models
from ... import Forms
from ... import Views
from ... import Pages
import navigation as nav


AppEnv.APP_ID = "PayLogs"
AppEnv.ANVIL_FUSION_VERSION = "0.0.2"
AppEnv.data_models = models
AppEnv.forms = Forms
AppEnv.views = Views
AppEnv.pages = Pages
AppEnv.grid_settings = {
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
AppEnv.start_menu = "business_menu"


class HomePage(HomePageTemplate):
    def __init__(self, **properties):

        self.content_id = "pl-content"
        self.content_control = None

        # Appbar configuration
        self.appbar = ej.navigations.AppBar({"colorMode": "Primary", "isSticky": True})
        self.appbar_logo = ej.buttons.Button({"cssClass": "e-inherit"})
        self.appbar_sidebar_toggle = ej.buttons.Button(
            {"cssClass": "e-inherit", "iconCss": "fa-solid fa-bars pl-appbar-menu-icon"}
        )
        self.appbar_settings_menu = None
        self.appbar_assistant_toggle = ej.buttons.Button(
            {"cssClass": "e-inherit", "iconCss": "fa-solid fa-comments pl-appbar-menu-icon"}
        )

        self.sidebar = nav.Sidebar(
            target_el=".pl-content",
            container_el="pl-sidebar",
            content_id=self.content_id,
        )
        self.appbar_menu = nav.AppbarMenu(
            container_el="pl-appbar-menu",
            sidebar=self.sidebar,
            menu_items=nav.PL_APPBAR_MENU,
        )
        self.assistant = nav.Assistant(
            target_el=".pl-content",
            container_el="pl-assistant-panel",
            content_id=self.content_id,
        )

        self.appbar_notification_list = ej.splitbuttons.DropDownButton(
            {
                "cssClass": "e-inherit e-caret-hide pl-menu-font",
                "iconCss": "fa-solid fa-bell pl-appbar-menu-icon",
                "items": [{"text": "No new notifications", "disabled": True}],
                "open": self.appbar_menu_popup_open,
            }
        )
        self.appbar_user_menu_items = [
            {
                "text": "Admin<br>admin@100rails.com",
                "disabled": True,
                "id": "pl-appbar-user-account-name",
            },
            {
                "text": "Account",
                "iconCss": "fa-regular fa-user-gear",
                "id": "pl-appbar-user-settings",
            },
            {
                "text": "Sign Out",
                "iconCss": "fa-regular fa-arrow-right-from-bracket",
                "id": "pl-appbar-sign-out",
            },
        ]
        self.appbar_user_menu = ej.splitbuttons.DropDownButton(
            {
                "cssClass": "e-inherit e-caret-hide pl-menu-font",
                "iconCss": "fa-solid fa-user pl-appbar-menu-icon",
                "items": self.appbar_user_menu_items,
                "open": self.appbar_menu_popup_open,
                "select": self.appbar_user_menu_select,
            }
        )
        self.appbar_assistant_button = ej.buttons.Button({
            'cssClass': 'e-inherit e-caret-hide pl-menu-font',
            'iconCss': 'fa-solid fa-comments pl-appbar-menu-icon',
        })

        AppEnv.login_user = self.login_user
        AppEnv.after_login = self.after_login


    def login_user(self):
        print('login_user')
        AppEnv.logged_user = init_user_session(login_form=Forms.UserLoginForm, after_login=self.after_login)
        if AppEnv.logged_user:
            self.after_login()


    def after_login(self):
        AppEnv.init_enumerations(model_list=models.ENUM_MODEL_LIST)

        if (AppEnv.logged_user.permissions.super_admin
                or AppEnv.logged_user.permissions.administrator
                or AppEnv.logged_user.permissions.developer):
            if self.appbar_settings_menu is None:
                print('settings menu', self.appbar_settings_menu)
                self.appbar_settings_menu = ej.buttons.Button(
                    {"cssClass": "e-inherit", "iconCss": "fa-solid fa-cog pl-appbar-menu-icon"}
                )
                self.appbar_settings_menu.appendTo(jQuery("#pl-appbar-settings-menu")[0])
                self.appbar_settings_menu.element.addEventListener(
                    "click", self.settings_click
                )

        self.appbar_menu.menu_items = nav.PL_APPBAR_MENU.copy()
        if (AppEnv.logged_user.permissions.super_admin
                or AppEnv.logged_user.permissions.developer):
            self.appbar_menu.menu_items.extend(nav.PL_APPBAR_MENU_ADMIN)
        if AppEnv.logged_user.permissions.developer:
            self.appbar_menu.menu_items.extend(nav.PL_APPBAR_MENU_DEVELOPER)
        self.appbar_menu.show()

        self.appbar_user_menu.items[0].text = AppEnv.logged_user.user_name + '<br>' + AppEnv.logged_user.email
        anvil.js.window.document.getElementById('pl-appbar-spacer').innerHTML = AppEnv.logged_user.tenant_name

        self.sidebar.show(AppEnv.start_menu)
        self.assistant.show()


    def form_show(self, **event_args):
        # Append appbar controls to elements
        self.appbar.appendTo(jQuery("#pl-appbar")[0])
        self.appbar_notification_list.appendTo(jQuery("#pl-appbar-notification-list")[0])
        self.appbar_user_menu.appendTo(jQuery("#pl-appbar-user-menu")[0])
        # self.appbar_assistant_button.appendTo(jQuery('#pl-appbar-help-menu')[0])
        # self.appbar_assistant_button.element.addEventListener('click', self.appbar_assistant_button_click)
        self.appbar_sidebar_toggle.appendTo(jQuery("#pl-appbar-sidebar-toggle")[0])
        self.appbar_sidebar_toggle.element.addEventListener(
            "click", self.sidebar.toggle
        )
        self.appbar_assistant_toggle.appendTo(jQuery("#pl-appbar-assistant-toggle")[0])
        self.appbar_assistant_toggle.element.addEventListener(
            "click", self.assistant.toggle
        )

        self.login_user()


    def settings_click(self, args):
        print('settings menu')
        self.sidebar.show_menu("settings_menu")

    # Sidebar toggle event handler
    def sidebar_toggle(self, args):
        self.sidebar.toggle(args)


    def appbar_assistant_button_click(self, args):
        print('appbar_assistant_button_click')
        if AppEnv.assistant is None:
            AppEnv.assistant = Forms.AssistantForm(target=self.content_id)
        AppEnv.assistant.form_show()


    # Appbar menu popup window position adjustment
    @staticmethod
    def appbar_menu_popup_open(args):
        args.element.parentElement.style.top = (
            str(float(args.element.parentElement.style.top[:-2]) + 10) + "px"
        )

    # Sidebar menu popup window position adjustment
    @staticmethod
    def sidebar_menu_popup_open(args):
        args.element.parentElement.style.top = (
            str(
                args.element.getBoundingClientRect().top
                - args.element.parentElement.offsetHeight
                + 44
            )
            + "px"
        )
        args.element.parentElement.style.left = "100px"

    def appbar_user_menu_select(self, args):
        print('appbar_user_menu_select', args.item.id)
        if args.item.id == 'pl-appbar-sign-out':
            anvil.users.logout()
            if self.content_control:
                self.content_control.destroy()
                self.content_control = None
            self.sidebar.show_menu(AppEnv.start_menu)
            self.login_user()
            # self.appbar_user_menu.items[0].text = 'Sign In'
            # self.appbar_user_menu.items[0].iconCss = 'fa-solid fa-sign-in'
            # self.appbar_user_menu.items[0].id = 'pl-appbar-sign-in'
        # elif args.item.id == 'pl-appbar-sign-in':
        #     AppEnv.logged_user = init_user_session(login_form=Forms.UserLoginForm)
        #     self.appbar_user_menu.items[0].text = AppEnv.logged_user['email']
        #     self.appbar_user_menu.items[0].disabled = True

