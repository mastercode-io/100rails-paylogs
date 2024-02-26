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

pay_rates = {
    "CAS-CW1-LAB-ORD": 32.0,
    "CAS-CW2-SCAF-ORD": 42.0,
    "CAS-CW3-SCAF-ORD": 42.0,
    "CAS-CW4-SCAF-ORD": 42.0,
    "CAS-YD1-ORD": 56.48,
    "CAS-YD2-ORD": 28.0,
    "PFT-YDM-ORD": 45.0,
    "PPT-TD1-ORD": 35.0,
    "PPT-YD1-ORD": 35.0,
    "PPT-YD2-ORD": 28.0,
    "CAS-CW2-LH-ORD": 58.68,
    "PFT-CW4-ORD": 53.98,
    "SUP2 SALARY": 51.44,
    "SUP3 SALARY": 52.92,
    "CAS-YD1-OT150%": 84.72,
    "CAS-YD1-OT200%": 112.96,
    "CAS-YD2-OT150%": 42.0,
    "CAS-YD2-OT200%": 56.0,
    "PFT-YDM-OT150%": 67.5,
    "PFT-YDM-OT200%": 90.0,
    "PPT-TD1-OT150%": 52.5,
    "PPT-TD1-OT200%": 70.0,
    "PPT-YD1-OT150%": 52.5,
    "PPT-YD1-OT200%": 70.0,
    "PPT-YD2-OT150%": 42.0,
    "PPT-YD2-OT200%": 56.0,
    "CAS-YDM-ORD": 56.48,
    "CAS-YDM-OT150%": 84.72,
    "CAS-YDM-OT200%": 112.96,
    "SUP2 OT150%": 77.16,
    "SUP2 OT200%": 102.88,
    "SUP3 OT150%": 77.16,
    "SUP3 OT200%": 102.88,
    "CAS-TD1-ORD": 46.9,
    "PFT-CW1-LAB-ORD": 26.88,
    "PFT-CW1-LAB-OT150%": 40.32,
    "PFT-CW1-LAB-OT200%": 53.76,
    "PFT-CW2-SCAF-ORD": 35.28,
    "PFT-CW2-SCAF-OT150%": 52.92,
    "PFT-CW2-SCAF-OT200%": 70.56,
    "PFT-CW2-LH-ORD": 49.48,
    "PFT-CW2-LH-OT150%": 74.22,
    "PFT-CW2-LH-OT200%": 98.96,
    "PFT-CW3-SCAF-ORD": 35.28,
    "PFT-CW3-SCAF-OT150%": 52.92,
    "PFT-CW3-SCAF-OT200%": 70.56,
    "PFT-CW4-SCAF-ORD": 35.28,
    "PFT-CW4-SCAF-OT150%": 52.92,
    "PFT-CW4-SCAF-OT200%": 70.56,
    "PFT-TD1-ORD": 39.4,
    "PFT-TD1-OT150%": 59.1,
    "PFT-TD1-OT200%": 78.79,
    "PFT-YD1-ORD": 47.63,
    "PFT-YD1-OT150%": 71.45,
    "PFT-YD1-OT200%": 95.26,
    "PFT-YD2-ORD": 23.52,
    "PFT-YD2-OT150%": 35.28,
    "PFT-YD2-OT200%": 47.04
}
ord_rates = [x for x in pay_rates.keys() if 'ORD' in x]
mult15_rates = [x for x in pay_rates.keys() if 'OT150%' in x]
mult20_rates = [x for x in pay_rates.keys() if 'OT200%' in x]
print(len(ord_rates), len(mult15_rates), len(mult20_rates))

pay_rate_template = models.PayRateTemplate.get_by('name', 'C1 Job')
print(pay_rate_template)
rate_item = models.PayRateTemplateItem.search(pay_rate_template=pay_rate_template, default_pay_rate_title='ORD')
print(rate_item)
