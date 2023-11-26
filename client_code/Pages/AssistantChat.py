from AnvilFusion.components.PageBase import PageBase
from AnvilFusion.components.FormInputs import MultiLineInput
import anvil.js
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
                    style="flex-grow: 1; overflow-y: auto; padding: 10px; border-bottom: 1px solid #ccc;"
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
            page_title_class='h5',
            page_title_style='margin-top: 25px;',
            content=content,
            **kwargs
        )


    def show(self):
        print('AssistantChat.show')
        super().show()
        pl_assistant_el = anvil.js.window.document.getElementById('pl-assistant')
        content_el = anvil.js.window.document.getElementById(f'{self.page_el_id}-content')
        content_el.style.height = f'{pl_assistant_el.offsetHeight - 130}px'
        # max_height = int(self.container_el.style['max-height'][0:-2])
        # page_content_el.style.height = f'{max_height - 50}px'
