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
    {"name": "name", "label": "Name"},
    {"name": "description", "label": "Description"},
    {"name": "address", "label": "Address"},
    {"name": "pay_rate_template.name", "label": "Pay Rate Template"},
    {"name": "status", "label": "Status"},
]
model = 'TimesheetType'
AppEnv.data_models.AppGridView(model=model, columns=columns).save()
# view_obj = AppEnv.data_models.AppGridView.get_by('model', model)
# view_config = view_obj['config'] or {}
# view_config['model'] = model
# view_config['columns'] = view_obj['columns'] or []
# grid_data = AppEnv.data_models.TimesheetType.get_grid_view(view_config,
#                                                            search_queries=None,
#                                                            filters=None,
#                                                            include_rows=False)
# print(grid_data)