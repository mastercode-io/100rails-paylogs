import anvil.js
from anvil.js.window import ej
from AnvilFusion.tools import utils


class TickerWidget:

    def __init__(self,
                 title=None,
                 symbol=None,
                 value=None,
                 value_format=None,
                 change=None,
                 change_format=None,
                 **kwargs):

        self.title = title or ''
        self.symbol = symbol
        self.value = value or 0
        self.value_format = value_format or '{:,.0f}'
        self.change = change or 0
        self.change_format = change_format or '{:,.0f}'

        if '%' in self.change_format:
            self.change = (self.change / (self.value + abs(self.change)))

        if self.change > 0:
            self.ticker_direction = f'\
                <div style="font-size: 16px; color: green;">\
                    <i class="fa-solid fa-caret-up" style="font-size: 70px;\
                     position: relative; top: 20px; margin-top: -30px;"></i>\
                    &nbsp;&nbsp;&nbsp;Up by {self.change_format.format(self.change)}\
                </div>'
            value_el_position = 7
        elif self.change < 0:
            self.ticker_direction = f'\
                <div style="font-size: 16px; color: red;">\
                    <i class="fa-solid fa-caret-down" style="font-size: 70px;\
                     position: relative; top: 10px; margin-top: -30px;"></i>\
                    &nbsp;&nbsp;&nbsp;Down by {self.change_format.format(-self.change)}\
                </div>'
            value_el_position = 7

        else:
            self.ticker_direction = f'\
                <div style="font-size: 16px; color: grey;">\
                    <i class="fa-solid fa-dash" style="font-size: 40px;\
                     position: relative; top: 10px; margin-top: -30px;"></i>\
                    &nbsp;&nbsp;&nbsp;Unchanged\
                </div>'
            value_el_position = 0

        self.html = f'\
            <div style="padding: 10px; height:100%;">\
                <div height="100%" style="border: 1px solid; border-radius: 5px; border-color: lightgrey;\
                background-color: #F5F5F5; height:100%; text-align: center; \
                display: flex; flex-direction: column; justify-content: space-evenly;">\
                    <div style="font-size: 14px; font-weight: bold;">\
                        {self.title}{(" (" + self.symbol + ")") if self.symbol else ""}\
                    </div>\
                    <div style="font-size: 30px; font-weight: bold;\
                    position: relative; top: {value_el_position}px;">\
                        {self.value_format.format(self.value)}\
                    </div>\
                    {self.ticker_direction}\
                </div>\
            </div>'


    def form_show(self):
        pass


class CircularChartWidget:

    def __init__(self,
                 title=None,
                 chart_type=None,
                 data=None,
                 **kwargs):
        # self._element_id = utils.new_el_id()
        self._element_id = ej.getUniqueID('fus-circular-chart')
        self.title = title or ''
        self.chart_type = chart_type or 'pie'
        self.data = data or []

        chart_config = {
             'series': [{
                 'dataSource': self.data,
                 'xName': 'label',
                 'yName': 'value',
                 'dataLabel': {'visible': True, 'position': 'Outside', 'name': 'label'},
                 'innerRadius': '40%' if self.chart_type == 'doughnut' else '0%',
             }]
        }
        self.chart = ej.charts.AccumulationChart(chart_config)

        self.html = f'\
            <div style="padding: 10px;">\
                <div style="border: 1px solid; background-color:grey;">\
                    <p>{self.title}</p>\
                    <div id="{self._element_id}"></div>\
                </div>\
            </div>'


    def form_show(self):
        self.chart.appendTo(f"#{self._element_id}")
