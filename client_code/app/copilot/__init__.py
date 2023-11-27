import anvil.server
from AnvilFusion.tools.utils import AppEnv

OPENAI_API_KEY = "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"
COPILOT_ASSISTANT_ID = "asst_Sy84Rcs6K3GsD2WnNqKnDwE3"


class Copilot:

    def __init__(self, api_key=None, assistant_id=None):
        self.api_key = api_key or OPENAI_API_KEY
        self.assistant_id = assistant_id or COPILOT_ASSISTANT_ID
        self.client = anvil.server.call('get_openai_client', api_key=self.api_key)
        self.thread_id = AppEnv.copilot_thread_id
        if not self.thread_id:
            thread = self.client.beta.threads.create()
            self.thread_id = thread['id']
            AppEnv.copilot_thread_id = self.thread_id
            print('Copilot', thread)
