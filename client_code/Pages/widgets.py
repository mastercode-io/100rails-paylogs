

class TickerWidget:

    def __init__(self,
                 ticker_title,
                 ticker_value,
                 ticker_symbol=None,
                 ticket_change=None,
                 **kwargs):

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
                     position: relative; top: 10px; margin-top: -30px;"></i>\
                    &nbsp;&nbsp;&nbsp;Down by {-self.ticker_change}\
                </div>'
        else:
            self.ticker_direction = f'\
                <div style="font-size: 16px; color: grey;">\
                    <i class="fa-solid fa-dash" style="font-size: 70px;\
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
