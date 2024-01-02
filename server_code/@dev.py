import anvil.server
import anvil.users
import uuid


@anvil.server.callable
def foo():
    api_user_row = anvil.users.signup_with_email('api_request@oaylogs.com', 'PlQsbaAJg3QwWGID')
    api_user_row.update(
        tenant_uid='00000000-0000-0000-0000-000000000000',
        uid=str(uuid.uuid4()),
        confirmed_email=True,
        first_name='api_request',
        last_name='system',
        permissions={'super_admin': True},
    )
