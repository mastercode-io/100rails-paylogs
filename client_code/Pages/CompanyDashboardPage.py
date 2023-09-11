from AnvilFusion.components.DashboardPage import DashboardPage


class CompanyDashboardPage(DashboardPage):

    def __init__(self, container_id, **kwargs):

        layout = {
            'cellSpacing': [10, 10],
            'columns': 2,
            'cellAspectRatio': 100/50,
            'panels': [
                {
                    'sizeX': 2, 'sizeY': 1, 'row': 0, 'col': 0,
                    'id': 'company_info', 'header': 'Company Info',
                },
                {
                    'sizeX': 1, 'sizeY': 2, 'row': 1, 'col': 0,
                    'id': 'employees', 'header': 'Employees',
                },
                {
                    'sizeX': 1, 'sizeY': 1, 'row': 1, 'col': 1,
                    'id': 'labour_cost', 'header': 'Labour Cost',
                },
                {
                    'sizeX': 1, 'sizeY': 1, 'row': 2, 'col': 1,
                    'id': 'last_payrun', 'header': 'Last Payrun',
                },
            ],
        }

        super().__init__(
            layout=layout,
            container_id=container_id,
            page_title='Company Dashboard',
            title_class='h3',
            **kwargs
        )
