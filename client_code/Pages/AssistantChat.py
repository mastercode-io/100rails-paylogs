from AnvilFusion.components.PageBase import PageBase
from AnvilFusion.components.FormInputs import MultiLineInput


class AssistantChat(PageBase):

    def __init__(self, container_id, **kwargs):
        print('AssistantChat')

        title = 'PayLogs Assistant'
        self.user_message = MultiLineInput(name='user_message', label='Message', rows=2)
        content = f'''\
            <div id="container">
                <div id="List" tabindex="1"></div>
                <div style="width: 100%;margin: 0 auto;">
                    {self.user_message.html}
                    <button id="btn" style="float:right">Send</button>
                </div>
            </div>
        '''
        super().__init__(
            container_id=container_id,
            page_title=title,
            page_title_class='h3',
            content=content,
            **kwargs
        )