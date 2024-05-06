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


def add_integration():
    print('func')
    integration = AppIntegration.get_by('service_name', 'scaflog')
    tenant = Tenant.get_by('name', 'Simos')
    print(integration, tenant)
    print(integration['uid'], integration['service_name'])
    api_credentials = anvil.server.call('generate_api_key', tenant['uid'], integration)
    print(api_credentials)


def add_grid_view():
    models.AppGridView(
        name='PayrunList',
        model='Payrun',
        owner='system',
        columns=[
            {
                "name": "payrun_week",
                "label": "Year Week"
            },
            {
                "name": "pay_period_start",
                "label": "Pay Period Start",
                "format": "MMM dd"
            },
            {
                "name": "pay_period_end",
                "label": "Pay Period End",
                "format": "MMM dd"
            },
            {
                "name": "pay_date",
                "label": "Pay Date",
                "format": "MMM dd"
            },
            {
                "name": "status",
                "label": "Status"
            },
            {
                "name": "notes",
                "label": "Notes"
            }
        ],
    ).save()


def bar():
    ts_list = models.Timesheet.search()
    print('ts_list', len(ts_list))
    for ts in ts_list:
        print(ts, ts['uid'], ts['payrun'])
        ts['payrun'] = None
        ts.save()
        print(ts['payrun'])
    ts_list = models.Timesheet.search()
    print('ts_list', len(ts_list))
    for ts in ts_list:
        print(ts['uid'], ts['payrun'])
    print('done')


def foo():
    bar()
