# from AnvilFusion.components.FormBase import FormBase, POPUP_WIDTH_COL1
from AnvilFusion.components.FormInputs import *
import anvil.js.window
from anvil.js.window import ej, jQuery
import uuid
from datetime import datetime, timedelta


class AssistantForm:
    def __init__(self, target):
        print('AssistantForm', target)

        self.target_el = anvil.js.window.document.getElementById(target)
        self.container_id = str(f"assistant-{uuid.uuid4()}")
        self.container_el = anvil.js.window.document.createElement('div')
        self.container_el.setAttribute('id', self.container_id)
        # self.container_el.style.visibility = 'hidden'
        self.target_el.append(self.container_el)
        self.form_id = str(f"assistant-form-{uuid.uuid4()}")
        self.chat_id = str(f"assistant-chat-{uuid.uuid4()}")
        self.chat_el = None
        self.chat = None


        self.user_message = MultiLineInput(name='user_message', label='', rows=1)
        self.thread = InlineMessage(name='thread')

        self.form_content = ''
        self.fields = [
            self.thread,
            self.user_message,
        ]
        self.form_content = f'<div id="{self.chat_id}""></div>'
        # self.form_content = f'<div id="{self.chat_id}" style="display: flex; flex-direction: column;">'
        # self.form_content += f'<div style="flex-grow: 1; overflow: auto;" ><div id="{self.thread.container_id}"></div></div></div>'
        # self.form_content += f'<div><div id="{self.user_message.container_id}"></div></div>'
        # self.form_content += '</div>'

        self.form_content = f'<div id="{self.form_id}" style="padding-top:1em;!important">' + self.form_content + '</div>'

        self.form = ej.popups.Dialog({
            'header': 'Assistant',
            'content': self.form_content,
            'showCloseIcon': True,
            'target': self.target_el,
            'isModal': True,
            'width': '500px',
            # 'height': '99%',
            'visible': True,
            'position': {'X': 'right', 'Y': '15'},
            'animationSettings': {'effect': 'Zoom'},
            'cssClass': 'e-fixed py-dialog',
            'open': self.form_open,
            # 'close': self.form_cancel,
            # 'beforeOpen': self.before_open,
            # 'created': self.form_created,
        })
        self.form.cssClass = 'e-fixed py-dialog'
        self.form.appendTo(self.container_el)
        print(self.target_el, self.container_el)


    def form_show(self):
        print('show assistant form')
        self.form.show()
        self.chat_el = anvil.js.window.document.getElementById(self.chat_id)
        max_height = int(self.container_el.style['max-height'][0:-2])
        # self.chat_el.style.height = f'{max_height - 50}px'
        self.form.element.style.height = f'{max_height - 50}px'
        self.chat = jQuery(f"#{self.chat_id}").kendoChat({
            'user': {
                'name': 'User',
                'iconUrl': 'https://demos.telerik.com/kendo-ui/content/chat/agent-01.png'
            },
            'messages': [
                {
                    'type': 'text',
                    'text': 'Hello, how may I help you today?',
                    'timestamp': datetime.now()
                }
            ],
            # 'actionClick': self.action_click,
            # 'toolbarClick': self.toolbar_click,
            # 'sendMessage': self.send_message,
            # 'typing': self.typing,
            # 'typingEnd': self.typing_end,
            'post': self.chat_post,
            # 'postEnd': self.post_end,
            # 'typingIndicator': self.typing_indicator,
            # 'typingIndicatorEnd': self.typing_indicator_end,
            # 'scrollToBottom': self.scroll_to_bottom,
            # 'scrollToBottomEnd': self.scroll_to_bottom_end,
            # 'attachmentUpload': self.attachment_upload,
            # 'attachmentUploadEnd': self.attachment_upload_end,
            'typingIndicatorTimeout': 5000,
            'toolbar': {
                'toggleable': True,
                'tools': [
                    {
                        'name': 'Insert',
                        'iconClass': 'k-icon k-i-plus-outline'
                    },
                    {
                        'name': 'Bold',
                        'iconClass': 'k-icon k-i-bold'
                    },
                    {
                        'name': 'Italic',
                        'iconClass': 'k-icon k-i-italic'
                    },
                    {
                        'name': 'Underline',
                        'iconClass': 'k-icon k-i-underline'
                    },
                    {
                        'name': 'strikethrough',
                        'iconClass': 'k-icon k-i-strikethrough'
                    },
                    {
                        'name': 'InsertUnorderedList',
                        'iconClass': 'k-icon k-i-bullets'
                    },
                    {
                        'name': 'InsertOrderedList',
                        'iconClass': 'k-icon k-i-numbered-list'
                    },
                    {
                        'name': 'Outdent',
                        'iconClass': 'k-icon k-i-outdent'
                    },
                    {
                        'name': 'Indent',
                        'iconClass': 'k-icon k-i-indent'
                    },
                    {
                        'name': 'CreateLink',
                        'iconClass': 'k-icon k-i-hyperlink-create'
                    },
                    {
                        'name': 'Unlink',
                        'iconClass':
                            'k-icon k-i-hyperlink-remove'
                    },
                    {
                        'name': 'InsertImage',
                        'iconClass': 'k-icon k-i-image-insert'
                    },
                    {
                        'name': 'InsertFile',
                        'iconClass': 'k-icon k-i-file-insert'
                    },
                    {
                        'name': 'ViewHtml',
                        'iconClass': 'k-icon k-i-html-view'
                    },
                    {
                        'name': 'CleanFormatting',
                        'iconClass': 'k-icon k-i-eraser'
                    },
                    {
                        'name': 'Print',
                        'iconClass': 'k-icon k-i-print'
                    },
                    {
                        'name': 'Undo',
                        'iconClass': 'k-icon k-i-undo'
                    },
                    {
                        'name': 'Redo',
                        'iconClass': 'k-icon k-i-redo'
                    }
                ]
            },
            'sendButton': {
                'iconClass': 'k-icon k-i-send'
            },
            'placeholder': 'Type a message...',
            'minLength': 1,
            'attachments': {
                'multiple': True,
                'maxFileSize': 3145728
            },
            'width': '100%',
            'height': '95%',
            'scrollToBottomOnFocus': True,
            'autoFocus': True,
            'typingIndicatorOffset': 0,
            'typingIndicatorHoldTime': 500,
            'typingIndicatorScrollSpeed': 1000,
            'typingIndicatorScrollDelay': 1000,
            'typingIndicatorScrollDistance': 100,
            'typingIndicatorOpacity': 0.5,
            'typingIndicatorTypingDelay': 1000,
            'typingIndicatorFadeDelay': 1000,
            'typingIndicatorFadeOutDelay': 1000,
            'typingIndicatorTemplate': '<span class="k-i-loading"></span>',
            'messageTemplate': '<div class="k-message"><div class="k-message-wrapper"><div class="k-message-avatar"><img src="#= user.iconUrl #" alt="#= user.name # avatar" /></div><div class="k-message-content"><div class="k-message-author">#: user.name #</div><div class="k-message-text">#: text #</div></div></div></div>',
            'systemMessageTemplate': '<div class="k-message"><div class="k-message-wrapper"><div class="k-message-content"><div class="k-message-text">#: text #</div></div></div></div>',
        }).data('kendoChat')
        self.chat = jQuery(f"#{self.chat_id}").kendoChat({
            'post': self.chat_post,
        }).data('kendoChat')
        print('kendo chat', self.chat)


    def form_open(self, args):
        print('form_open')
        # for field in self.fields:
        #     field.show()


    def chat_post(self, args):
        print('chat_post', args)
