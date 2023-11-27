import anvil.server
import json


OPENAI_API_KEY = "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"
COPILOT_ASSISTANT_ID = "asst_Sy84Rcs6K3GsD2WnNqKnDwE3"


class Copilot:

    def __init__(self, api_key=None, assistant_id=None):
        self.api_key = api_key or OPENAI_API_KEY
        self.assistant_id = assistant_id or COPILOT_ASSISTANT_ID
        self.thread_id = anvil.server.call('openai_init_client', api_key=self.api_key)


    def send_message(self, question):
        response =  anvil.server.call(
            'openai_send_message',
            question,
             assistant_id=self.assistant_id,
             thread_id=self.thread_id,
        )
        return json.loads(response)
