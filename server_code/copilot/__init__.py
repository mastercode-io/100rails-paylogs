import anvil.server
import openai



@anvil.server.callable
def get_openai_client(api_key=None):
    client = openai.Client(api_key=api_key)
    return client


@anvil.server.callable
def get_current_thread_id():
    return anvil.server.session.get('current_thread_id', None)