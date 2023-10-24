from AnvilFusion.components.GridView import GridView


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
            {'id': 'select_tenant', 'label': 'Select Tenant', 'action': self.select_tenant},
            {'id': 'reset_tenant', 'label': 'Reset Tenant', 'action': self.reset_tenant},
        ]

        super().__init__(
            model='Tenant',
            view_config=view_config,
            context_menu_items=context_menu_items,
            **kwargs)


    def select_tenant(self, args):
        print('select_tenant', args)
        pass


    def reset_tenant(self, args):
        print('reset_tenant', args)
        pass
