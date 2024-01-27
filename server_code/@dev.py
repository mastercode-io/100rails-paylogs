import anvil.server
import anvil.users
import uuid


@anvil.server.callable
def foo():
    print(anvil.server.session)
