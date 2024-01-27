import anvil.server
import anvil.users
import uuid


@anvil.server.callable
def foo():
    print('SERVER SESSION\n', anvil.server.session.keys())
