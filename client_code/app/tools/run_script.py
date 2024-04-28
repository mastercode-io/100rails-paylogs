import anvil.server
from ..models import AppIntegration, Tenant


def bar():
    print('func')
    integration = AppIntegration.get_by('service_name', 'scaflog')
    tenant = Tenant.get_by('name', 'Simos')
    print(integration, tenant)
    api_credentials = anvil.server.call('generate_api_key', tenant['uid'], integration)
    print(api_credentials)


def foo():
    bar()
