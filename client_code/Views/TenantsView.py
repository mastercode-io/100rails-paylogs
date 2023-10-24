from AnvilFusion.components.GridView import GridView
from AnvilFusion.tools.utils import AppEnv


class TenantsView(GridView):
    def __init__(self, **kwargs):
        print('TenantsView')
        view_config = {
            'model': 'Tenant',
            'columns': [
                {'name': 'name', 'label': 'Account Name'},
                {'name': 'status', 'label': 'Status'},
                {'name': '_spacer', 'no_data': True},
            ],
        }

        context_menu_items = [
            {'id': 'select_tenant', 'label': 'Lock Dataset', 'action': self.lock_datset},
            {'id': 'reset_tenant', 'label': 'Reset Dataset', 'action': self.reset_dataset},
        ]

        super().__init__(
            model='Tenant',
            view_config=view_config,
            context_menu_items=context_menu_items,
            **kwargs)


    def lock_datset(self, args):
        print('lock_dataset', args.item.rowData.uid)
        AppEnv.set_tenant(tenant_uid=args.item.rowData.uid, reload_func=AppEnv.after_login)


    def reset_dataset(self, args):
        print('reset_dataset', args.item.rowData.uid)
        AppEnv.reset_tenant(reload_func=AppEnv.after_login)
