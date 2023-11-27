import anvil.server
from openai import OpenAI


openai_client = None


@anvil.server.callable
def init_openai_client(api_key=None):
    global openai_client
    openai_client = OpenAI(api_key=api_key)
    if not anvil.server.session.get('openai_thread_id'):
        thread = openai_client.beta.threads.create()
        print(thread)
        anvil.server.session['openai_thread_id'] = thread['id']
    return anvil.server.session['openai_thread_id']

