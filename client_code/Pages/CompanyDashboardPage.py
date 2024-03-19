from AnvilFusion.components.DashboardPage import DashboardPage

PANEL_CSS_CLASS = 'pl-company-dashboard-panel'
# PANEL_CSS_CLASS = ''


class CompanyDashboardPage(DashboardPage):

    def __init__(self, container_id, **kwargs):

        # total_staff_widget_content = f'\
        #     <div style="padding: 10px; height:100%;">\
        #         <div height="100%" style="border: 1px solid; border-radius: 5px; border-color: lightgrey;\
        #         background-color: #F5F5F5; height:100%; text-align: center; \
        #         display: flex; flex-direction: column; justify-content: space-evenly;">\
        #             <div style="font-size: 14px; font-weight: bold;">\
        #                 Total Staff This Pay\
        #             </div>\
        #             <div style="font-size: 30px; font-weight: bold;">\
        #                 1,400\
        #             </div>\
        #             <div style="font-size: 16px; color: green;">\
        #                 <i class="fa-solid fa-caret-up" style="font-size: 70px;\
        #                  position: relative; top: 20px; margin-top: -30px;"></i>\
        #                 &nbsp;&nbsp;&nbsp;Up by 3\
        #             </div>\
        #         </div>\
        #     </div>'
        #
        # total_pay_widget_content = f'\
        #     <div style="padding: 10px;">\
        #         <div style="border: 1px solid; background-color:grey;">\
        #             <p>Total Paid This Pay</p>\
        #             <p style="font-size:20px;font-weight:bold;">$34,544</p>\
        #         </div>\
        #     </div>'
        total_staff_widget = TickerWidget('Total Staff This Pay', '1,400',
                                          ticket_change=3)
        total_pay_widget = TickerWidget('Total Paid This Pay', '$34,544',
                                        ticket_change=-2568)

        layout = {
            'showGridLines': True,
            'cellSpacing': [0, 0],
            'columns': 4,
            'cellAspectRatio': 100/100,
            'panels': [
                {
                    'sizeX': 1, 'sizeY': 1, 'row': 0, 'col': 0,
                    'id': 'total_staff_widget',
                    # 'header': 'Widget A',
                    'content': total_staff_widget.html,
                    'cssClass': PANEL_CSS_CLASS,
                },
                {
                    'sizeX': 1, 'sizeY': 1, 'row': 0, 'col': 1,
                    'id': 'total_pay_widget',
                    # 'header': 'Widget B',
                    'content': total_pay_widget.html,
                    'cssClass': PANEL_CSS_CLASS,
                },
                {
                    'sizeX': 2, 'sizeY': 1, 'row': 1, 'col': 0,
                    'id': 'pay_distribution_chart',
                    # 'header': 'Widget C',
                    'cssClass': PANEL_CSS_CLASS,
                },
                {
                    'sizeX': 2, 'sizeY': 2, 'row': 0, 'col': 2,
                    'id': 'pay_trend_chat',
                    # 'header': 'Widget D',
                    'cssClass': PANEL_CSS_CLASS,
                },
            ],
            # 'allowResizing': True,
            'allowDragging': False,
        }

        super().__init__(
            layout=layout,
            container_id=container_id,
            page_title='Company Dashboard',
            title_class='pl-company-dashboard-title',
            **kwargs
        )


class TickerWidget:

    def __init__(self, ticker_title, ticker_value, ticker_symbol=None, ticket_change=None, **kwargs):
        self.ticker_title = ticker_title
        self.ticker_symbol = ticker_symbol
        self.ticker_value = ticker_value
        self.ticker_change = ticket_change or 0

        if self.ticker_change > 0:
            self.ticker_direction = f'\
                <div style="font-size: 16px; color: green;">\
                    <i class="fa-solid fa-caret-up" style="font-size: 70px;\
                     position: relative; top: 20px; margin-top: -30px;"></i>\
                    &nbsp;&nbsp;&nbsp;Up by {self.ticker_change}\
                </div>'
        elif self.ticker_change < 0:
            self.ticker_direction = f'\
                <div style="font-size: 16px; color: red;">\
                    <i class="fa-solid fa-caret-down" style="font-size: 70px;\
                     position: relative; top: 20px; margin-top: -30px;"></i>\
                    &nbsp;&nbsp;&nbsp;Down by {-self.ticker_change}\
                </div>'
        else:
            self.ticker_direction = f'\
                <div style="font-size: 16px; color: grey;">\
                    <i class="fa-solid fa-caret-right" style="font-size: 70px;\
                     position: relative; top: 20px; margin-top: -30px;"></i>\
                    &nbsp;&nbsp;&nbsp;No Change\
                </div>'

        self.html = f'\
            <div style="padding: 10px; height:100%;">\
                <div height="100%" style="border: 1px solid; border-radius: 5px; border-color: lightgrey;\
                background-color: #F5F5F5; height:100%; text-align: center; \
                display: flex; flex-direction: column; justify-content: space-evenly;">\
                    <div style="font-size: 14px; font-weight: bold;">\
                        {self.ticker_symbol or self.ticker_title}\
                    </div>\
                    <div style="font-size: 30px; font-weight: bold;">\
                        {self.ticker_value}\
                    </div>\
                    {self.ticker_direction}\
                </div>\
            </div>'
