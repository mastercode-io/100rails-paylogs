from ._anvil_designer import HomePageTemplate
import anvil.js
from anvil.js.window import ej, jQuery
import anvil.users
from AnvilFusion.tools.utils import AppEnv, DotDict, init_user_session
from AnvilFusion.components.FormInputs import DropdownInput
from .. import models
from ... import Forms
from ... import Views
from ... import Pages
import navigation as nav
# from ..copilot import Copilot
import json


AppEnv.APP_ID = "PayLogs"
AppEnv.ANVIL_FUSION_VERSION = "0.0.2"
AppEnv.data_models = models
AppEnv.forms = Forms
AppEnv.views = Views
AppEnv.pages = Pages
AppEnv.grid_settings = {}
AppEnv.theme = {
    'components': {
        'alert': {
            'success': {'class': 'alert alert-success', 'icon': 'fa-regular fa-circle-check pl-message-icon'},
            'info': {'class': 'alert alert-info', 'icon': 'fa-regular fa-circle-info pl-message-icon'},
            'warning': {'class': 'alert alert-warning', 'icon': 'fa-regular fa-triangle-exclamation pl-message-icon'},
            'error': {'class': 'alert alert-error', 'icon': 'fa-regular fa-circle-xmark pl-message-icon'},
        },
    }
}
AppEnv.start_menu = "timesheet_menu"


class HomePage(HomePageTemplate):
    def __init__(self, **properties):

        self.appbar_settings_menu_show = False
        self.content_id = "pl-content"
        self.content_control = None

        # Appbar configuration
        self.appbar = ej.navigations.AppBar({"colorMode": "Primary", "isSticky": True})
        self.appbar_logo = ej.buttons.Button({"cssClass": "e-inherit"})
        # self.appbar_sidebar_toggle = ej.buttons.Button(
        #     {"cssClass": "e-inherit", "iconCss": "fa-solid fa-bars pl-appbar-menu-icon"}
        # )
        self.appbar_assistant_toggle = ej.buttons.Button(
            {"cssClass": "e-inherit", "iconCss": "fa-solid fa-comments pl-appbar-menu-icon"}
        )

        self.assistant = nav.Assistant(
            target_el=".pl-page-container",
            container_id="pl-assistant",
            content_id=self.content_id,
        )
        # self.sidebar = nav.Sidebar(
        #     target_el=".pl-page-container",
        #     container_id="pl-sidebar",
        #     content_id=self.content_id,
        # )
        self.appbar_menu = nav.AppbarMenu(
            container_el="pl-appbar-menu",
            target_el=".pl-page-container",
            container_id="pl-sidebar",
            content_id=self.content_id,
            menu_items=nav.PL_APPBAR_MENU,
            nav_items=nav.PL_NAV_ITEMS,
            # sidebar=self.sidebar,
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
        self.appbar_data_file = DropdownInput(name='data_file',
                                              container_id='pl-appbar-data-file',
                                              on_change=self.appbar_data_file_select)
        self.appbar_settings_menu_items = nav.PL_MENU_ITEMS['settings_menu']
        #     [
        #     {'id': 'settings_users', 'text': 'Users', 'items': []},
        #     {'id': 'settings_locations', 'text': 'Locations', 'items': []},
        #     {'id': 'settings_employee_roles', 'text': 'Employee Roles', 'items': []},
        #     {'id': 'settings_job_types', 'text': 'Job Types', 'items': []},
        #     {'id': 'settings_timesheet_types', 'text': 'Timesheet Types', 'items': []},
        # ]
        # self.appbar_settings_menu = ej.splitbuttons.DropDownButton(
        #     {
        #         "cssClass": "e-inherit e-caret-hide pl-menu-font",
        #         "iconCss": "fa-solid fa-cog pl-appbar-menu-icon",
        #         "items": self.appbar_settings_menu_items,
        #         "open": self.appbar_menu_popup_open,
        #         "select": self.appbar_settings_menu_select,
        #     }
        # )
        self.appbar_settings_button = ej.buttons.Button({
            'cssClass': 'e-inherit e-caret-hide pl-menu-font',
            'iconCss': 'fa-solid fa-cog pl-appbar-menu-icon',
        })
        self.appbar_settings_form = ej.buttons.Button({
            'cssClass': 'e-inherit e-caret-hide pl-menu-font',
            'iconCss': 'fa-solid fa-input-text pl-appbar-menu-icon',
        })
        self.appbar_assistant_button = ej.buttons.Button({
            'cssClass': 'e-inherit e-caret-hide pl-menu-font',
            'iconCss': 'fa-solid fa-comments pl-appbar-menu-icon',
        })

        AppEnv.login_user = self.login_user
        AppEnv.after_login = self.after_login


    def login_user(self):
        print('login_user')
        AppEnv.logged_user = init_user_session(login_form=Forms.UserLoginForm, after_login=self.after_login)
        # AppEnv.logged_user = init_user_session(
        #     user_email='alex@100email.co',
        #     password='7CAwXs-D"H:a]84',
        #     after_login=self.after_login,
        # )
        if AppEnv.logged_user:
            self.after_login()


    def after_login(self):
        AppEnv.init_enumerations(model_list=models.ENUM_MODEL_LIST)
        AppEnv.init_enum_constants()
        print('enum_constants', AppEnv.enum_constants)
        do_something()
        # AppEnv.navigation = self.sidebar
        AppEnv.assistant = self.assistant

        # if (AppEnv.logged_user.permissions.super_admin
        #         or AppEnv.logged_user.permissions.administrator
        #         or AppEnv.logged_user.permissions.developer):
        #     if self.appbar_settings_menu_show is False:
        #         self.appbar_settings_menu_show = True
        #         print('settings menu', self.appbar_settings_menu)
        #         # self.appbar_settings_menu = ej.buttons.Button(
        #         #     {"cssClass": "e-inherit", "iconCss": "fa-solid fa-cog pl-appbar-menu-icon"}
        #         # )
        #         self.appbar_settings_menu.appendTo(jQuery("#pl-appbar-settings-menu")[0])
        #         # self.appbar_settings_menu.element.addEventListener(
        #         #     "click", self.settings_click
        #         # )

        self.appbar_menu.menu_items = nav.PL_APPBAR_MENU.copy()
        if (AppEnv.logged_user.permissions.super_admin
                or AppEnv.logged_user.permissions.developer):
            self.appbar_menu.menu_items.extend(nav.PL_APPBAR_MENU_ADMIN)
            self.appbar_menu.menu_items.extend(nav.PL_APPBAR_MENU_DEVELOPER)
        # if AppEnv.logged_user.permissions.developer:
        #     self.appbar_menu.menu_items.extend(nav.PL_APPBAR_MENU_DEVELOPER)
        self.appbar_menu.show()

        self.appbar_user_menu.items[0].text = AppEnv.logged_user.user_name + '<br>' + AppEnv.logged_user.email
        anvil.js.window.document.getElementById('pl-appbar-spacer').innerHTML = AppEnv.logged_user.tenant_name

        # self.appbar_data_file.options = AppEnv.logged_user.data_files
        # self.appbar_data_file.value = AppEnv.logged_user.data_files[0]
        self.appbar_data_file.show()
        print(AppEnv.logged_user)
        print(self.appbar_data_file.options)
        print(self.appbar_data_file.control.dataSource)

        self.assistant.show()
        self.appbar_menu.show_selected('timesheet_dashboard')
        # self.sidebar.show(AppEnv.start_menu)
        # self.sidebar.refresh_content()

        # copilot = Copilot()
        # message = 'what are you?'
        # thread = copilot.send_message(message)
        # print('copilot', message)
        # print(thread)


    def form_show(self, **event_args):
        # Append appbar controls to elements
        self.appbar.appendTo(jQuery("#pl-appbar")[0])
        self.appbar_notification_list.appendTo(jQuery("#pl-appbar-notification-list")[0])
        self.appbar_user_menu.appendTo(jQuery("#pl-appbar-user-menu")[0])
        # self.appbar_assistant_button.appendTo(jQuery('#pl-appbar-help-menu')[0])
        # self.appbar_assistant_button.element.addEventListener('click', self.appbar_assistant_button_click)
        # self.appbar_sidebar_toggle.appendTo(jQuery("#pl-appbar-sidebar-toggle")[0])
        # self.appbar_sidebar_toggle.element.addEventListener(
        #     "click", self.sidebar.toggle
        # )
        self.appbar_settings_button.appendTo(jQuery("#pl-appbar-settings-menu")[0])
        self.appbar_settings_form.appendTo(jQuery("#pl-appbar-settings-form")[0])
        # self.appbar_settings_button.element.onclick = self.appbar_menu.show_selected('settings_account')
        self.appbar_settings_button.element.onclick = self.appbar_settings_button_click
        self.appbar_settings_form.element.onclick = self.appbar_settings_form_click
        self.appbar_assistant_toggle.appendTo(jQuery("#pl-appbar-assistant-toggle")[0])
        self.appbar_assistant_toggle.element.onclick = self.assistant.toggle
        # self.appbar_assistant_toggle.element.addEventListener(
        #     "click", self.assistant.toggle
        # )
        self.login_user()


    # def settings_click(self, args):
    #     print('settings menu', args.item.id)
    # self.sidebar.show_menu("settings_menu")

    # Sidebar toggle event handler


    def sidebar_toggle(self, args):
        pass
        # self.sidebar.toggle(args)


    def appbar_settings_button_click(self, args):
        print('appbar_settings_button_click')
        tenant = models.Tenant.get(AppEnv.logged_user.tenant_uid)
        print('tenant', tenant)
        nav.PL_NAV_ITEMS['settings_account']['props'] = {'data': tenant}
        self.appbar_menu.show_selected('settings_account')

    def appbar_settings_form_click(self, args):
        print('appbar_settings_button_click')
        tenant = models.Tenant.get_row(AppEnv.logged_user.tenant_uid)
        recs = models.Account.search(data_files=[tenant])
        print('recs', len(recs))
        account = next(iter(models.Account.search(data_files=[tenant])), None)
        print('tenant', tenant)
        print('account', account)
        nav.PL_NAV_ITEMS['settings_account']['props'] = {'data': account}
        self.appbar_menu.show_selected('settings_form')

    # def appbar_assistant_button_click(self, args):
    #     print('appbar_assistant_button_click')
    #     if AppEnv.assistant is None:
    #         AppEnv.assistant = Forms.AssistantForm(target=self.content_id)
    #     AppEnv.assistant.form_show()

    # Appbar menu popup window position adjustment

    @staticmethod
    def appbar_menu_popup_open(args):
        args.element.parentElement.style.top = (
                str(float(args.element.parentElement.style.top[:-2]) + 3) + "px"
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
            # self.sidebar.show_menu(AppEnv.start_menu)
            self.login_user()
            self.appbar_user_menu.items[0].text = 'Sign In'
            self.appbar_user_menu.items[0].iconCss = 'fa-solid fa-sign-in'
            self.appbar_user_menu.items[0].id = 'pl-appbar-sign-in'
        elif args.item.id == 'pl-appbar-sign-in':
            AppEnv.logged_user = init_user_session(login_form=Forms.UserLoginForm)
            self.appbar_user_menu.items[0].text = AppEnv.logged_user['email']
            self.appbar_user_menu.items[0].disabled = True


    def appbar_settings_menu_select(self, args):
        print('appbar_user_menu_select', args.item.id)
        self.appbar_menu.show_selected(args.item.id)


    def appbar_data_file_select(self, args):
        print('appbar_data_file_select', args)
        print(self.appbar_data_file.value)
        # self.appbar_menu.show_selected(args.item.id)


def do_something():
    print('do_something')
    print(anvil.server.get_api_origin())
    # new_api_key = anvil.server.call('generate_tenant_api_key', AppEnv.logged_user.tenant_uid, 'scaflog')
    # print('new_api_key', new_api_key)
    # enum_name = 'DAY_TYPE_OPTIONS'
    # enum_options = [
    #     'Any Day',
    #     'Weekday',
    #     'Weekend',
    #     'Saturday',
    #     'Sunday',
    #     'Public Holiday',
    #     'Week',
    # ]
    # enum_values = {x: x for x in enum_options}
    # enum = models.AppEnum(name=enum_name, options=enum_values).save()
    # print(enum)
