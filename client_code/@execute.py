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
        'RDO',
    ]
    enum_values = {x: x for x in enum_options}
    enum = models.AppEnum(name=enum_name, options=enum_values).save()
    print(enum)


init_user_session()
# print('client context', anvil.server.context)
# print('bg_task_id', getattr(anvil.server.context, 'background_task_id', None))
# anvil.server.call('foo')
job_type = models.Job_Type.get_by('remote_links', {{'76e14124-04dc-49e4-9f18-27b25a66f67e': 1886330000091365941}})
print('job type', job_type)
