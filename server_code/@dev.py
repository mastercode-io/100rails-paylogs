import anvil.server
import anvil.users
import uuid
from AnvilFusion.server.utils import get_logged_user, save_logged_user
from .app import models
from anvil.tables import app_tables


def add_background_task(task_id, context=None, logged_user=None):
    bg_task_row = app_tables.app_background_tasks.get(task_id=task_id)
    if bg_task_row is None:
        app_tables.app_background_tasks.add_row(task_id=task_id, context=context, logged_user=logged_user)
    else:
        bg_task_row['context'] = context
        bg_task_row['logged_user'] = logged_user


def update_background_task(task_id, status, result=None):
    bg_task_row = app_tables.app_background_tasks.get(task_id=task_id)
    if bg_task_row:
        bg_task_row['status'] = status
        bg_task_row['result'] = result


@anvil.server.background_task
def background_task(logged_user=None):
    # print('Background task started')
    # print('background task context', anvil.server.context)
    if logged_user:
        save_logged_user(current_user=logged_user)
    # print('AnvilFusion function', get_logged_user())
    add_background_task(
        anvil.server.context.background_task_id,
        logged_user=get_logged_user()
    )
    result = bar()
    # result = None
    # print('bg_task_id', getattr(anvil.server.context, 'background_task_id', None))
    update_background_task(
        anvil.server.context.background_task_id,
        status='finished',
        result=result
    )
    return 'Background task done'


@anvil.server.callable
def foo():
    print('Lunching BG task')
    print('server context', anvil.server.context)
    bg_task = anvil.server.launch_background_task('background_task', get_logged_user())
    print(bg_task)


def bar():
    print('bar context', anvil.server.context)
    location = models.Location(name='test', short_code='TST').save()
    print('location', location, location['name'], location['uid'])
    item = models.Location.get(location['uid'])
    print('item', item, item['name'], item['uid'])
    item.update({'name': 'TEST'})
    item.save()
    print('item', item, item['name'])
    item2 = models.Location.get_by('short_code', 'TST')
    print('item2', item2, item2['name'], item2['uid'])
    # return location.to_json_dict()
