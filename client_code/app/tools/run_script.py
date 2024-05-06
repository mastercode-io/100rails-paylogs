import anvil.server
import anvil.tables.query as q
from ...app import models
from ..models import AppIntegration, Tenant
import datetime


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
    # search_query = [q.none_of(payrun=None)]
    # ts_list = models.Timesheet.search(search_query=search_query)
    # for ts in ts_list:
    #     ts['payrun'] = None
    #     ts.save()
    payrun = models.Payrun.get_by('pay_period_start', datetime.date(2024, 4, 8))
    print(payrun)
    ts_list = models.Timesheet.search(date=q.between(datetime.date(2024, 4, 8), datetime.date(2024, 4, 15)))
    print(len(ts_list))
    for ts in ts_list:
        ts['payrun'] = payrun
        ts.save()
    payrun = models.Payrun.get_by('pay_period_start', datetime.date(2024, 4, 15))
    print(payrun)
    ts_list = models.Timesheet.search(date=q.between(datetime.date(2024, 4, 15), datetime.date(2024, 4, 22)))
    print(len(ts_list))
    for ts in ts_list:
        ts['payrun'] = payrun
        ts.save()


def foo():
    bar()
