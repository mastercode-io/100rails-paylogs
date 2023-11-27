import anvil.server
from openai import OpenAI


@anvil.server.portable_class
class OpenAIClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.client = OpenAI(api_key=api_key)


@anvil.server.callable
def get_openai_client(api_key=None):
    client = OpenAIClient(api_key=api_key)
    return client


@anvil.server.callable
def get_current_thread_id():
    return anvil.server.session.get('current_thread_id', None)