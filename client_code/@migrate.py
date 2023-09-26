from AnvilFusion.tools.utils import AppEnv, init_user_session
from AnvilFusion.datamodel import migrate
from .app import models

AppEnv.APP_ID = 'PayLogs'
AppEnv.data_models = models

init_user_session()
migrate.migrate_db_schema()
