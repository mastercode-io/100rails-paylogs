import anvil.server
import anvil.users
import uuid
from AnvilFusion.server.utils import get_logged_user, save_logged_user


@anvil.server.callable
def foo():
    print('Lunching BG task')
    bg_task = anvil.server.launch_background_task('background_task', get_logged_user())
    print(bg_task)


@anvil.server.background_task
def background_task(logged_user=None):
    if logged_user:
        save_logged_user(logged_user)
    print('Background task logged user: ', get_logged_user())
    return 'Background task done'
