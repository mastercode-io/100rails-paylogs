from AnvilFusion.features.developer.MigratePage import MigratePage
from ..tools.RunScriptPage import RunScriptPage


# App menu item list
PL_MENU_ITEMS = {
    'timesheet_menu': [
        {'id': 'timesheet_dashboard', 'text': 'Dashboard','items': []},
        {'id': 'timesheet_report', 'text': 'Timesheets', 'items': []},
        {'id': 'timesheet_sync', 'text': 'Transfer Data', 'items': []},
        {'id': 'timesheet_upload', 'text': 'Upload Data', 'items': []},
    ],
    'payroll_menu': [
        {'id': 'payroll_dashboard', 'text': 'Dashboard',  'whatever': 'hah?', 'items': []},
        {'id': 'payroll_payruns', 'text': 'Payruns', 'items': []},
        {'id': 'payroll_timesheets', 'text': 'Timesheets', 'items': []},
        {'id': 'payroll_transfer_data', 'text': 'Transfer Data', 'items': []},
        # {'id': 'payroll_pay_categories', 'text': 'Pay Categories', 'items': []},
        # {'id': 'payroll_pay_rate_rules', 'text': 'Pay Rate RULES', 'items': []},
        # {'id': 'payroll_pay_rate_scopes', 'text': 'Pay Rate SCOPES', 'items': []},
        # {'id': 'payroll_pay_rate_templates', 'text': 'Pay Rate TEMPLATES', 'items': []},
        # {'id': 'payroll_calendar', 'text': 'Payroll CALENDAR', 'items': []},
        # {'id': 'payroll_settings', 'text': 'Payroll SETTINGS', 'items': []},
    ],
    'directory_menu': [
        {'id': 'directory_employees', 'text': 'Employees', 'items': []},
        {'id': 'directory_locations', 'text': 'Locations', 'items': []},
        {'id': 'directory_jobs', 'text': 'Jobs', 'items': []},
        {'id': 'directory_job_types', 'text': 'Job Types', 'items': []},
        {'id': 'directory_employee_roles', 'text': 'Employee Roles', 'items': []},
        {'id': 'directory_timesheet_types', 'text': 'Timesheet Types', 'items': []},
    ],
    'settings_menu': [
        {'id': 'settings_users', 'text': 'Users', 'items': []},
    ],
    'admin_menu': [
        {'id': 'admin_accounts', 'text': 'Accounts', 'items': []},
        {'id': 'admin_tenants', 'text': 'Tenants', 'items': []},
        {'id': 'admin_user_roles', 'text': 'User Roles', 'items': []},
        {'id': 'admin_permissions', 'text': 'Permissions', 'items': []},
        {'id': 'admin_settings', 'text': 'Settings', 'items': [
            {'id': 'admin_settings_scope_types', 'text': 'Scope Types', 'items': []},
        ]},
        {'id': 'admin_integrations', 'text': 'Integrations', 'items': []},

    ],
    'developer_menu': [
        {'id': 'developer_components', 'text': 'Components', 'items': [
            {'id': 'developer_views', 'text': 'Views', 'items': []},
            {'id': 'developer_pages', 'text': 'Pages', 'items': []},
            {'id': 'developer_forms', 'text': 'Forms', 'items': []},
        ]},
        {'id': 'developer_schema', 'text': 'App Schema', 'items': [
            {'id': 'developer_enums', 'text': 'Enumerations', 'items': []},
            {'id': 'developer_models', 'text': 'Models', 'items': []},
            {'id': 'developer_migrate', 'text': 'Migrate DB', 'items': []},
        ]},
        {'id': 'developer_tools', 'text': 'Tools', 'items': [
            {'id': 'developer_import', 'text': 'Import Data', 'items': []},
            {'id': 'developer_export', 'text': 'Export Data', 'items': []},
            {'id': 'developer_run_script', 'text': 'Run Script', 'items': []},
        ]},
        {'id': 'developer_prototype', 'text': 'Prototype', 'items': [
            {'id': 'developer_tenant_form', 'text': 'Tenant Form', 'items': []},
            {'id': 'developer_tree_grid', 'text': 'Tree Grid View', 'items': []},
        ]},
    ]
}

# Navigation items/actions
PL_NAV_ITEMS = {
    'timesheet_sync': {'type': 'page', 'name': 'ImportTimesheetsPage', 'action': 'open', 'props': {}},
    'timesheet_upload': {'type': 'page', 'name': 'UploadDataPage', 'action': 'open', 'props': {}},

    'payroll_dashboard': {'name': 'CompanyDashboardPage', 'type': 'page', 'action': 'open', 'props': {}},
    'payroll_payruns': {'model': 'Payrun', 'type': 'view', 'action': 'open', 'props': {}},
    'payroll_timesheets': {'class': 'TimesheetView', 'type': 'custom', 'action': 'open', 'props': {}},
    'payroll_transfer_data': {'type': 'page', 'name': 'TransferDataPage', 'action': 'open', 'props': {}},
    'payroll_pay_categories': {'model': 'PayCategory', 'type': 'view', 'action': 'open', 'props': {}},
    'payroll_pay_rate_rules': {'model': 'PayRateRule', 'type': 'view', 'action': 'open', 'props': {}},
    'payroll_pay_rate_scopes': {'model': 'Scope', 'type': 'view', 'action': 'open', 'props': {}},
    'payroll_pay_rate_templates': {'model': 'PayRateTemplate', 'type': 'view', 'action': 'open', 'props': {}},
    # 'payroll_calendar': {'type': 'page', 'name': 'CalendarPage', 'action': 'open', 'props': {}},
    'payroll_settings': {'class': 'PayrollSettingsForm', 'type': 'form', 'action': 'open', 'props': {}},

    'directory_employees': {'model': 'Employee', 'type': 'view', 'action': 'open', 'props': {}},
    'directory_locations': {'model': 'Location', 'type': 'view', 'action': 'open', 'props': {}},
    'directory_jobs': {'model': 'Job', 'type': 'view', 'action': 'open', 'props': {}},
    'directory_job_types': {'model': 'JobType', 'type': 'view', 'action': 'open', 'props': {}},
    'directory_employee_roles': {'model': 'EmployeeRole', 'type': 'view', 'action': 'open', 'props': {}},
    'directory_timesheet_types': {'model': 'TimesheetType', 'type': 'view', 'action': 'open', 'props': {}},

    'settings_users': {'model': 'User', 'type': 'view', 'action': 'open', 'props': {}},
    # 'settings_account': {'name': 'SettingsPage', 'type': 'page', 'action': 'open', 'props': {}},
    'settings_form': {'class': 'SettingsForm', 'type': 'form', 'action': 'open', 'props': {}},

    'admin_accounts': {'class': 'AccountsAdminView', 'type': 'custom', 'action': 'open', 'props': {}},
    'admin_tenants': {'class': 'TenantsView', 'type': 'custom', 'action': 'open', 'props': {}},
    'admin_users': {'model': 'User', 'type': 'view', 'action': 'open', 'props': {}},
    'admin_settings_scope_types': {'model': 'ScopeType', 'type': 'view', 'action': 'open', 'props': {}},
    'admin_integrations': {'model': 'AppIntegration', 'type': 'view', 'action': 'open', 'props': {}},
    'admin_user_roles': {'model': 'UserRole', 'type': 'view', 'action': 'open', 'props': {}},
    # 'admin_permissions': {'model': 'Permission', 'type': 'view', 'action': 'open', 'props': {}},
    # 'admin_settings': {'model': 'Setting', 'type': 'view', 'action': 'open', 'props': {}},

    'developer_views': {'model': 'AppGridView', 'type': 'view', 'action': 'open', 'props': {}},
    # 'developer_forms': {'model': 'Form', 'type': 'view', 'action': 'open', 'props': {}},
    'developer_enums': {'model': 'AppEnum', 'type': 'view', 'action': 'open', 'props': {}},
    # 'developer_models': {'model': 'Model', 'type': 'view', 'action': 'open', 'props': {}},
    'developer_migrate': {'type': 'page', 'page': MigratePage, 'props': {}},
    'developer_run_script': {'type': 'page', 'page': RunScriptPage, 'props': {}},
    'developer_tenant_form': {'type': 'form', 'class': 'SettingsForm', 'props': {}},
    'developer_tree_grid': {'type': 'page', 'name': 'TreeGridPage', 'props': {}},
    # 'developer_grid_preview': {'type': 'page', 'page': MigratePage, 'props': {}},
    # 'developer_page_preview': {'type': 'page', 'page': MigratePage, 'props': {}},
}

PL_DEFAULT_NAV_ITEMS = {
    # 'timesheet_menu': 'timesheet_dashboard',
    'payroll_menu': 'payroll_dashboard',
    'directory_menu': 'directory_employees',
    'settings_menu': 'settings_users',
    'admin_menu': 'admin_tenants',
    'developer_menu': 'developer_views',
}

# Appbar main menu
PL_APPBAR_MENU = [
    {'id': 'payroll_menu', 'text': 'PAYROLL', 'items': PL_MENU_ITEMS['payroll_menu']},
    {'id': 'directory_menu', 'text': 'DIRECTORY', 'items': PL_MENU_ITEMS['directory_menu']},
    # {'id': 'settings_menu', 'text': 'SETTINGS', 'items': PL_MENU_ITEMS['settings_menu']},
    # {'id': 'admin_menu', 'text': 'ADMIN', 'items': PL_MENU_ITEMS['admin_menu']},
    # {'id': 'developer_menu', 'text': 'DEVELOPER', 'items': PL_MENU_ITEMS['developer_menu']},
]
PL_APPBAR_MENU_ADMIN = [
    {'separator': True},
    {'id': 'admin_menu', 'text': 'ADMIN', 'items': PL_MENU_ITEMS['admin_menu']},
]
PL_APPBAR_MENU_DEVELOPER = [
    {'id': 'developer_menu', 'text': 'DEVELOPER', 'items': PL_MENU_ITEMS['developer_menu']},
]

DEFAULT_PERMISSIONS_SCHEMA = {
    'payroll_menu': {
        'access': {'account_admin': True, 'payroll_admin': True, 'payroll_manager': True},
        'items': [
            {
                'payroll_dashboard': {
                    'access': {'account_admin': True, 'payroll_admin': True, 'payroll_manager': False},
                    'items': []
                }
            },
            {
                'payroll_payruns': {
                    'access': {'account_admin': True, 'payroll_admin': True, 'payroll_manager': True},
                    'items': []
                }
            },
            {
                'payroll_timesheets': {
                    'access': {'account_admin': True, 'payroll_admin': True, 'payroll_manager': True},
                    'items': []
                }
            },
            {
                'payroll_transfer_data': {
                    'account_admin': True, 'payroll_admin': True, 'payroll_manager': True},
                'items': []
            },
        ]
    },
    'directory_menu': {
        'access': {'account_admin': True, 'payroll_admin': True, 'payroll_manager': True},
        'items': [
            {
                'directory_employees': {
                    'access': {'account_admin': True, 'payroll_admin': True, 'payroll_manager': True},
                    'items': []
                }
            },
            {
                'directory_locations': {
                    'access': {'account_admin': True, 'payroll_admin': True, 'payroll_manager': False},
                    'items': []
                }
            },
            {
                'directory_jobs': {
                    'access': {'account_admin': True, 'payroll_admin': True, 'payroll_manager': True},
                    'items': []
                }
            },
            {
                'directory_job_types': {
                    'access': {'account_admin': True, 'payroll_admin': True, 'payroll_manager': False},
                    'items': []
                }
            },
            {
                'directory_employee_roles': {
                    'access': {'account_admin': True, 'payroll_admin': True, 'payroll_manager': False},
                    'items': []
                }
            },
            {
                'directory_timesheet_types': {
                    'access': {'account_admin': True, 'payroll_admin': True, 'payroll_manager': False},
                    'items': []
                }
            },
        ]
    },
    'settings_menu': {
        'access': {'account_admin': False, 'payroll_admin': False, 'payroll_manager': False},
        'items': [
            {
                'settings_users': {
                    'access': {'account_admin': False, 'payroll_admin': False, 'payroll_manager': False},
                    'items': []
                }
            },
        ]
    },
    'admin_menu': {
        'access': {'account_admin': True, 'payroll_admin': False, 'payroll_manager': False},
        'items': [
            {
                'admin_accounts': {
                    'access': {'account_admin': True, 'payroll_admin': False, 'payroll_manager': False},
                    'items': []
                }
            },
            {
                'admin_tenants': {
                    'access': {'account_admin': True, 'payroll_admin': False, 'payroll_manager': False},
                    'items': []
                }
            },
            {
                'admin_user_roles': {
                    'access': {'account_admin': True, 'payroll_admin': False, 'payroll_manager': False},
                    'items': []
                }
            },
            {
                'admin_permissions': {
                    'access': {'account_admin': True, 'payroll_admin': False, 'payroll_manager': False},
                    'items': []
                }
            },
            {
                'admin_settings': {
                    'access': {'account_admin': True, 'payroll_admin': True, 'payroll_manager': False},
                    'items': [
                        {
                            'admin_settings_scope_types': {
                                'access': {'account_admin': True, 'payroll_admin': True, 'payroll_manager': False},
                                'items': []
                            }
                        }
                    ]
                }
            },
            {
                'admin_integrations': {
                    'access': {'account_admin': True, 'payroll_admin': True, 'payroll_manager': True},
                    'items': []
                }
            },
        ]
    },
    'developer_menu': {
        'access': {'account_admin': True, 'payroll_admin': False, 'payroll_manager': False},
        'items': [
            {
                'developer_components': {
                    'access': {'account_admin': True, 'payroll_admin': False, 'payroll_manager': False},
                    'items': [
                        {
                            'developer_views': {
                                'access': {'account_admin': True, 'payroll_admin': False, 'payroll_manager': False},
                                'items': []
                            }
                        },
                        {
                            'developer_pages': {
                                'access': {'account_admin': True, 'payroll_admin': False, 'payroll_manager': False},
                                'items': []
                            }
                        },
                        {
                            'developer_forms': {
                                'access': {'account_admin': True, 'payroll_admin': False, 'payroll_manager': False},
                                'items': []
                            }
                        },
                    ]
                }
            },
            {
                'developer_schema': {
                    'access': {'account_admin': True, 'payroll_admin': False, 'payroll_manager': False},
                    'items': [
                        {
                            'developer_enums': {
                                'access': {'account_admin': True, 'payroll_admin': False, 'payroll_manager': False},
                                'items': []
                            }
                        },
                        {
                            'developer_models': {
                                'access': {'account_admin': True, 'payroll_admin': False, 'payroll_manager': False},
                                'items': []
                            }
                        },
                        {
                            'developer_migrate': {
                                'access': {'account_admin': True, 'payroll_admin': False, 'payroll_manager': False},
                                'items': []
                            }
                        },
                    ]
                }
            },
            {
                'developer_tools': {
                    'access': {'account_admin': True, 'payroll_admin': False, 'payroll_manager': False},
                    'items': [
                        {
                            'developer_import': {
                                'access': {'account_admin': True, 'payroll_admin': False, 'payroll_manager': False},
                                'items': []
                            }
                        },
                        {
                            'developer_export': {
                                'access': {'account_admin': True, 'payroll_admin': False, 'payroll_manager': False},
                                'items': []
                            }
                        },
                        {
                            'developer_run_script': {
                                'access': {'account_admin': True, 'payroll_admin': False, 'payroll_manager': False},
                                'items': []
                            }
                        },
                    ]
                }
            },
        ],
    },
}
