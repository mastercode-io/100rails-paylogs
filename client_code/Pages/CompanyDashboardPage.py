from AnvilFusion.components.DashboardPage import DashboardPage
from .widgets import TickerWidget, CircularChartWidget, StatWidget, STAT_UNCHANGED, STAT_UP, STAT_DOWN

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

        total_staff_stat = StatWidget(title='Total Staff',
                                      value=156,
                                      description='Total staff fo this payroll period',
                                      accent=STAT_UNCHANGED)
        total_hours_stat = StatWidget(title='Total Hours',
                                      value=4396,
                                      description='Total paid hours',
                                      accent=STAT_UP)
        total_pay_stat = StatWidget(title='Total Pay',
                                    value=34544,
                                    value_format='${:,.0f}',
                                    description='Total pay for this payroll period',
                                    accent=STAT_DOWN)

        stat_widgets_html = f'\
            <div class="pl-flex-row-start">\
                {total_staff_stat.html}\
                {total_hours_stat.html}\
                {total_pay_stat.html}\
            </div>'

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
                                                     value_suffix='%', )

        self.widgets = [
            # total_staff_widget,
            # total_pay_widget,
            total_staff_stat,
            total_hours_stat,
            total_pay_stat,
            pay_distribution_chart,
        ]

        layout = {
            'showGridLines': True,
            'cellSpacing': [0, 0],
            'columns': 4,
            'cellAspectRatio': 100 / 80,
            'panels': [
                {
                    'sizeX': 1, 'sizeY': 1, 'row': 0, 'col': 0,
                    'id': 'total_staff_stat',
                    'content': total_staff_stat.html,
                    'cssClass': PANEL_CSS_CLASS,
                },
                {
                    'sizeX': 1, 'sizeY': 1, 'row': 0, 'col': 1,
                    'id': 'total_hours_stat',
                    'content': total_hours_stat.html,
                    'cssClass': PANEL_CSS_CLASS,
                },
                {
                    'sizeX': 1, 'sizeY': 1, 'row': 0, 'col': 2,
                    'id': 'total_pay_stat',
                    'content': total_pay_stat.html,
                    'cssClass': PANEL_CSS_CLASS,
                },
                {
                    'sizeX': 1, 'sizeY': 1, 'row': 0, 'col': 3,
                    # 'id': 'total_pay_widget',
                    'cssClass': PANEL_CSS_CLASS,
                },
                {
                    'sizeX': 2, 'sizeY': 2, 'row': 1, 'col': 0,
                    'id': 'pay_distribution_chart',
                    'content': pay_distribution_chart.html,
                    'cssClass': PANEL_CSS_CLASS,
                },
                {
                    'sizeX': 2, 'sizeY': 2, 'row': 1, 'col': 2,
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
            print('widget', widget)
            widget.form_show()
        print('CompanyDashboardPage refresh')
        self.dashboard.refresh()
