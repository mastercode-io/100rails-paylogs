import anvil.server
import anvil.users
from AnvilFusion.server.utils import get_logged_user, save_logged_user
from anvil.tables import app_tables
import traceback


def register_background_task(task_id, context=None, logged_user=None):
    bg_task_row = app_tables.app_background_tasks.get(task_id=task_id)
    if bg_task_row is None:
        app_tables.app_background_tasks.add_row(task_id=task_id, context=context, logged_user=logged_user)
    else:
        bg_task_row['context'] = context
        bg_task_row['logged_user'] = logged_user


def update_background_task(task_id, status=None, result=None):
    bg_task = anvil.server.get_background_task(task_id)
    bg_task_row = app_tables.app_background_tasks.get(task_id=task_id)
    if bg_task_row:
        bg_task_row['status'] = status
        bg_task_row['result'] = result


@anvil.server.background_task
def background_task_manager(logged_user, context, func, *args, **kwargs):
    if logged_user:
        save_logged_user(current_user=logged_user)
    else:
        logged_user = {}
    register_background_task(
        anvil.server.context.background_task_id,
        context=context,
        logged_user=logged_user,
    )
    try:
        result = func(*args, **kwargs)
        status = 'finished'
    except Exception as e:  # noqa
        result = traceback.format_exc()
        status = 'error'
    update_background_task(
        anvil.server.context.background_task_id,
        status=status,
        result=result
    )
    return result
