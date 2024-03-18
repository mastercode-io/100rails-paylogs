from AnvilFusion.components.DashboardPage import DashboardPage

PANEL_CSS_CLASS = 'pl-company-dashboard-panel'
# PANEL_CSS_CLASS = ''


class CompanyDashboardPage(DashboardPage):

    def __init__(self, container_id, **kwargs):

        total_staff_widget_content = f'\
            <div style="padding: 10px; height:100%;">\
                <div height="100%" style="border: 1px solid; border-radius: 5px; border-color: lightgrey;\
                background-color: #F5F5F5; height:100%; text-align: center; \
                display: flex; flex-direction: column; justify-content: space-evenly;">\
                    <div style="font-size: 14px; font-weight: bold;">\
                        Total Staff This Pay\
                    </div>\
                    <div style="font-size: 30px; font-weight: bold;">\
                        1,400\
                    </div>\
                    <div style="font-size: 16px; color: green;">\
                        <i class="fa-solid fa-caret-up" style="font-size: 50px;\
                         position: relative; top: 20px;"></i>\
                        &nbsp;&nbsp;&nbsp;Up by 3\
                    </div>\
                </div>\
            </div>'

        total_pay_widget_content = f'\
            <div style="padding: 10px;">\
                <div style="border: 1px solid; background-color:grey;">\
                    <p>Total Paid This Pay</p>\
                    <p style="font-size:20px;font-weight:bold;">$34,544</p>\
                </div>\
            </div>'

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
                    'content': total_staff_widget_content,
                    'cssClass': PANEL_CSS_CLASS,
                },
                {
                    'sizeX': 1, 'sizeY': 1, 'row': 0, 'col': 1,
                    'id': 'total_pay_widget',
                    # 'header': 'Widget B',
                    'content': total_pay_widget_content,
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
