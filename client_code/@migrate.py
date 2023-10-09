from AnvilFusion.tools.utils import AppEnv, init_user_session
from AnvilFusion.datamodel import migrate
from .app import models
from . import Forms
from . import Views
from . import Pages

AppEnv.APP_ID = "PayLogs"
AppEnv.ANVIL_FUSION_VERSION = "0.0.2"
AppEnv.data_models = models
AppEnv.forms = Forms
AppEnv.views = Views
AppEnv.pages = Pages

init_user_session()
# migrate.migrate_db_schema()

columns = [
    {"name": "short_code", "label": "Short Code"},
    {"name": "name", "label": "Name"},
    {"name": "description", "label": "Description"},
    {"name": "configuration.paid_time", "label": "Paid Time"},
    {"name": "configuration.paid_breaks", "label": "Paid Breaks"},
    {"name": "configuration.sick_leave", "label": "Sick Leave"},
    {"name": "configuration.annual_leave", "label": "Annual Leave"},
    {"name": "status", "label": "Status"},
]
model = 'TimesheetType'
view_obj = AppEnv.data_models.AppGridView.get_by('model', model)
view_config = view_obj['config'] or {}
view_config['model'] = model
view_config['columns'] = view_obj['columns'] or []
grid_data = AppEnv.data_models.TimesheetType.get_grid_view(view_config,
                                                           search_queries=None,
                                                           filters=None,
                                                           include_rows=False)
print(grid_data)