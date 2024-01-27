import anvil.server
import anvil.users
import uuid
from AnvilFusion.server.utils import get_logged_user


@anvil.server.callable
def foo():
    print('Logged user: ', get_logged_user())
