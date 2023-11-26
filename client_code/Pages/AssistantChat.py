from AnvilFusion.components.PageBase import PageBase
from AnvilFusion.components.FormInputs import MultiLineInput
import uuid


class AssistantChat(PageBase):

    def __init__(self, container_id, **kwargs):
        print('AssistantChat')

        title = 'PayLogs Assistant'
        el_id_prefix = uuid.uuid4()
        self.user_message = MultiLineInput(name='user_message', label='Message', rows=2)
        content = f'''\
            <div id="{el_id_prefix}-assistant-container" style="display: flex; flex-direction: column; height: 100%;">
                <div id="{el_id_prefix}-assistant-thread" tabindex="1" 
                    style="flex-grow: 1; overflow-y: auto; padding: 10px; border: 1px solid #ccc;"
                ></div>
                <div style="width: 100%;margin: 0 auto;">
                    {self.user_message.html}
                    <button id="{el_id_prefix}-send-button" style="float:right">Send</button>
                </div>
            </div>
        '''
        super().__init__(
            container_id=container_id,
            page_title=title,
            page_title_class='h4',
            content=content,
            **kwargs
        )
