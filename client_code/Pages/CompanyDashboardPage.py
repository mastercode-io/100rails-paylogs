from AnvilFusion.components.DashboardPage import DashboardPage
from .widgets import (TickerWidget, CircularChartWidget, StatWidget, ChartWidget,
                      STAT_UNCHANGED, STAT_UP, STAT_DOWN)

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

        rate_per_hour_chart_config = {
            'primaryXAxis': {
                'title': 'Week Number',
                'minimum': 1,
                'maximum': 52,
                'interval': 1,
            },
            'primaryYAxis': {
                'title': 'Average Rate per Hour',
                'labelFormat': '${value}',
                'minimum': 20,
                'maximum': 250,
                'interval': 20,
            },
            'series': [{
                'xName': 'week',
                'yName': 'rate',
                'type': 'Line',
            }],
        }
        rate_per_hour_chart_data = [
            {'week': 1, 'rate': 38.26},
            {'week': 2, 'rate': 35.14},
            {'week': 3, 'rate': 42.58},
            {'week': 4, 'rate': 45.23},
            {'week': 5, 'rate': 50.12},
            {'week': 6, 'rate': 46.34},
            {'week': 7, 'rate': 48.23},
            {'week': 8, 'rate': 51.36},
            {'week': 9, 'rate': 39.84},
            {'week': 10, 'rate': 42.36},
            {'week': 11, 'rate': 41.71},
            {'week': 12, 'rate': 40.44},
            {'week': 13, 'rate': 42.94},
            {'week': 14, 'rate': 43.17},
            {'week': 15, 'rate': 48.68},
            {'week': 16, 'rate': 47.09},
        ]
        rate_per_hour_chart = ChartWidget(title='Average Rate per Hour',
                                          chart_config=rate_per_hour_chart_config,
                                          data=rate_per_hour_chart_data,)

        self.widgets = [
            # total_staff_widget,
            # total_pay_widget,
            total_staff_stat,
            total_hours_stat,
            total_pay_stat,
            pay_distribution_chart,
            rate_per_hour_chart,
        ]

        layout = {
            'showGridLines': True,
            'cellSpacing': [0, 0],
            'columns': 4,
            'cellAspectRatio': 100 / 80,
            'panels': [
                {
                    'sizeX': 4, 'sizeY': 1, 'row': 0, 'col': 0,
                    'id': 'total_staff_stat',
                    # 'content': total_staff_stat.html,
                    'content': stat_widgets_html,
                    'cssClass': PANEL_CSS_CLASS,
                },
                # {
                #     'sizeX': 1, 'sizeY': 1, 'row': 0, 'col': 1,
                #     'id': 'total_hours_stat',
                #     'content': total_hours_stat.html,
                #     'cssClass': PANEL_CSS_CLASS,
                # },
                # {
                #     'sizeX': 1, 'sizeY': 1, 'row': 0, 'col': 2,
                #     'id': 'total_pay_stat',
                #     'content': total_pay_stat.html,
                #     'cssClass': PANEL_CSS_CLASS,
                # },
                # {
                #     'sizeX': 1, 'sizeY': 1, 'row': 0, 'col': 3,
                #     # 'id': 'total_pay_widget',
                #     'cssClass': PANEL_CSS_CLASS,
                # },
                {
                    'sizeX': 2, 'sizeY': 2, 'row': 1, 'col': 0,
                    'id': 'pay_distribution_chart',
                    'content': pay_distribution_chart.html,
                    'cssClass': PANEL_CSS_CLASS,
                },
                {
                    'sizeX': 2, 'sizeY': 2, 'row': 1, 'col': 2,
                    'id': 'rate_per_hour_chart',
                    'content': rate_per_hour_chart.html,
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
            page_title='Dashboard',
            title_class='text-indigo-600 text-5xl font-semibold leading-loose ml-5 mb-5',
            **kwargs
        )

    def form_show(self):
        super().form_show()
        for widget in self.widgets:
            print('widget', widget)
            widget.form_show()
        print('CompanyDashboardPage refresh')
        self.dashboard.refresh()
