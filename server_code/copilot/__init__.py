import anvil.server
from openai import OpenAI
import time
import json


openai_client = None


@anvil.server.callable
def openai_init_client(api_key=None):
    global openai_client
    openai_client = OpenAI(api_key=api_key)
    if not anvil.server.session.get('openai_thread_id'):
        thread = openai_client.beta.threads.create()
        print(thread)
        anvil.server.session['openai_thread_id'] = thread.id
    return anvil.server.session['openai_thread_id']


@anvil.server.callable
def openai_send_message(question, assistant_id=None, thread_id=None):
    global openai_client
    if not openai_client or not assistant_id or not thread_id:
        return None
    start = time.time()
    openai_client.beta.threads.messages.create(
        thread_id=thread_id,
        content=question,
        role='user',
    )
    run = openai_client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
    )
    while run.status == "queued" or run.status == "in_progress":
        run = openai_client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id,
        )
        time.sleep(0.5)
    messages = openai_client.beta.threads.messages.list(thread_id=thread_id)
    print('openai_ask_question', time.time() - start)
    print('question', question)
    print('messages', messages)
    return json.loads(messages.model_dump_json())
