import anvil.server
from ...app import models
from ..models import AppIntegration, Tenant


def add_enum_list():
    enum_name = 'DAY_TYPE_OPTIONS'
    enum_options = [
        'AnyDay',
        'Weekday',
        'Weekend',
        'Saturday',
        'Sunday',
        'PublicHoliday',
        'Week',
        'RDO',
    ]
    enum_values = {x: x for x in enum_options}
    enum = models.AppEnum(name=enum_name, options=enum_values).save()
    print(enum)


def bar():
    print('func')
    integration = AppIntegration.get_by('service_name', 'scaflog')
    tenant = Tenant.get_by('name', 'Simos')
    print(integration, tenant)
    print(integration['uid'], integration['service_name'])
    api_credentials = anvil.server.call('generate_api_key', tenant['uid'], integration)
    print(api_credentials)


def foo():
    add_enum_list()
