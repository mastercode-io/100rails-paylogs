from AnvilFusion.components.DashboardPage import DashboardPage
from .widgets import TickerWidget, CircularChartWidget

PANEL_CSS_CLASS = 'pl-company-dashboard-panel'
# PANEL_CSS_CLASS = ''


class CompanyDashboardPage(DashboardPage):

    def __init__(self, container_id, **kwargs):

        total_staff_widget = TickerWidget(title='Total Staff This Pay',
                                          value=1400,
                                          change=0)

        total_pay_widget = TickerWidget(title='Total Paid This Pay',
                                        value=34544,
                                        value_format='${:,.0f}',
                                        change=-2317,
                                        change_format='{:,.2%}')

        pay_distribution_data = [
            {'label': 'Regular', 'value': 60},
            {'label': 'Overtime', 'value': 20},
            {'label': 'Holiday', 'value': 10},
            {'label': 'Sick', 'value': 5},
            {'label': 'Vacation', 'value': 5},
        ]
        pay_distribution_chart = CircularChartWidget(title='Pay Distribution by Rate Type',
                                                     chart_type='doughnut',
                                                     data=pay_distribution_data,
                                                     value_suffix='%',)

        self.widgets = [
            total_staff_widget,
            total_pay_widget,
            pay_distribution_chart,
        ]

        layout = {
            'showGridLines': True,
            'cellSpacing': [0, 0],
            'columns': 4,
            'cellAspectRatio': 100/100,
            'panels': [
                {
                    'sizeX': 1, 'sizeY': 1, 'row': 0, 'col': 0,
                    'id': 'total_staff_widget',
                    'content': total_staff_widget.html,
                    'cssClass': PANEL_CSS_CLASS,
                },
                {
                    'sizeX': 1, 'sizeY': 1, 'row': 0, 'col': 1,
                    'id': 'total_pay_widget',
                    'content': total_pay_widget.html,
                    'cssClass': PANEL_CSS_CLASS,
                },
                {
                    'sizeX': 2, 'sizeY': 2, 'row': 1, 'col': 0,
                    'id': 'pay_distribution_chart',
                    'content': pay_distribution_chart.html,
                    'cssClass': PANEL_CSS_CLASS,
                },
                {
                    'sizeX': 2, 'sizeY': 3, 'row': 0, 'col': 2,
                    'id': 'pay_trend_chat',
                    'cssClass': PANEL_CSS_CLASS,
                },
            ],
            # 'allowResizing': True,
            'allowDragging': False,
        }

        print('CompanyDashboardPage')
        super().__init__(
            layout=layout,
            container_id=container_id,
            page_title='Company Dashboard',
            title_class='pl-company-dashboard-title',
            **kwargs
        )


    def form_show(self):
        super().form_show()
        for widget in self.widgets:
            widget.form_show()
        print('CompanyDashboardPage refresh')
        self.dashboard.refresh()
