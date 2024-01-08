from AnvilFusion.tools.utils import AppEnv, init_user_session
from .app import models
from . import Forms
from . import Views
from . import Pages
from . import api
import uuid
import anvil.server
import anvil.users

AppEnv.APP_ID = "PayLogs"
AppEnv.ANVIL_FUSION_VERSION = "0.0.2"
AppEnv.data_models = models
AppEnv.forms = Forms
AppEnv.views = Views
AppEnv.pages = Pages


def add_enum_list():
    enum_name = 'DAY_TYPE_OPTIONS'
    enum_options = [
        'Any Day',
        'Weekday',
        'Weekend',
        'Saturday',
        'Sunday',
        'Public Holiday',
        'Week',
    ]
    enum_values = {x: x for x in enum_options}
    enum = models.AppEnum(name=enum_name, options=enum_values).save()
    print(enum)


init_user_session()
timesheet_schema = models.Timesheet.get_json_schema()
# print(timesheet_schema)

ts = models.Timesheet.get('febd487a-f5ab-45f5-862a-8a1016568d27')
print(ts.to_json_dict(json_schema=timesheet_schema))

# api_service = api.register_api_service(
#     name='scaflog',
#     description='Scaflog API Integration',
#     url='https://creatorapp.zoho.com/100rails/goscaffold',
#     connection_type='in',
# )
# api_service = api.AppApiService.get_by('name', 'scaflog')
# print(api_service)
# tenant_uid = 'a48a5f3f-f4a0-40a7-9b56-23d08c98e182'
# api_credential = anvil.server.call('generate_api_key', tenant_uid, api_service)
# print(api_credential['api_key'])
# anvil.server.call('foo')
