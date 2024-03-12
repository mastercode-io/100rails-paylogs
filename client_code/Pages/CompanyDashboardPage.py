from AnvilFusion.components.DashboardPage import DashboardPage

# PANEL_CSS_CLASS = 'pl-company-dashboard-panel'
PANEL_CSS_CLASS = ''


class CompanyDashboardPage(DashboardPage):

    def __init__(self, container_id, **kwargs):

        layout = {
            'showGridLines': True,
            'cellSpacing': [0, 0],
            'columns': 2,
            'cellAspectRatio': 100/50,
            'panels': [
                {
                    'sizeX': 1, 'sizeY': 1, 'row': 0, 'col': 0,
                    'id': 'widget_a',
                    # 'header': 'Company Info',
                    'cssClass': PANEL_CSS_CLASS,
                },
                {
                    'sizeX': 1, 'sizeY': 1, 'row': 0, 'col': 1,
                    'id': 'widget_b',
                    # 'header': 'Employees',
                    'cssClass': PANEL_CSS_CLASS,
                },
                {
                    'sizeX': 2, 'sizeY': 1, 'row': 1, 'col': 0,
                    'id': 'widget_c',
                    # 'header': 'Last Payrun',
                    'cssClass': PANEL_CSS_CLASS,
                },
                {
                    'sizeX': 2, 'sizeY': 2, 'row': 0, 'col': 2,
                    'id': 'widget_d',
                    # 'header': 'Labour Cost',
                    'cssClass': PANEL_CSS_CLASS,
                },
            ],
            # 'allowResizing': True,
            'allowDragging': False,
        }

        super().__init__(
            layout=layout,
            container_id=container_id,
            # page_title='Company Dashboard',
            title_class='h3',
            **kwargs
        )
