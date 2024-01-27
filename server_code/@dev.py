import anvil.server
import anvil.users
import uuid
from AnvilFusion.server.utils import get_logged_user, save_logged_user
from .app import models
from anvil.tables import app_tables


def save_background_task_context(task_id, context=None, logged_user=None):
    bg_task_row = app_tables.app_background_tasks.get(task_id=task_id)
    if bg_task_row is None:
        app_tables.app_background_tasks.add_row(task_id=task_id, context=context, logged_user=logged_user)
    else:
        bg_task_row['context'] = context
        bg_task_row['logged_user'] = logged_user


@anvil.server.callable
def foo():
    print('Lunching BG task')
    print('server context', anvil.server.context)
    bg_task = anvil.server.launch_background_task('background_task', get_logged_user())
    print(bg_task)


@anvil.server.background_task
def background_task(logged_user=None):
    print('Background task started')
    print('background task context', anvil.server.context)
    if logged_user:
        save_logged_user(current_user=logged_user)
    print('AnvilFusion function', get_logged_user())
    save_background_task_context(
        anvil.server.context.background_task_id,
        logged_user=get_logged_user()
    )
    bar()
    return 'Background task done'


def bar():
    print('bar context', anvil.server.context)
    print('BAR', get_logged_user())
    tenant = models.Tenant.search()
    for t in tenant:
        print(t['name'])
