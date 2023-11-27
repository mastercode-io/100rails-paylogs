import anvil.server
from openai import OpenAI


@anvil.server.callable
def get_openai_client(api_key=None):
    return OpenAI(api_key=api_key)


@anvil.server.callable
def get_current_thread_id():
    return anvil.server.session.get('current_thread_id', None)