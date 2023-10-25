from AnvilFusion.datamodel.particles import (
    model_type,
    Attribute,
    Relationship,
    Computed,
)
from AnvilFusion.datamodel import types
from datetime import datetime

from .timesheet import TimesheetType, Timesheet

TimesheetType.__module__ = __name__
Timesheet.__module__ = __name__

# Model list for enumerations
ENUM_MODEL_LIST = {
    # 'Activity': {'model': 'Activity', 'name_field': 'name'},
}


# ------------------------------
# Framework object model classes
# ------------------------------
@model_type
class AppAuditLog:
    model_type = types.ModelTypes.SYSTEM
    table_name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    record_uid = Attribute(field_type=types.FieldTypes.UID)
    action_type = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    action_time = Attribute(field_type=types.FieldTypes.DATETIME)
    action_by = Attribute(field_type=types.FieldTypes.UID)
    previous_state = Attribute(field_type=types.FieldTypes.OBJECT)
    new_state = Attribute(field_type=types.FieldTypes.OBJECT)


@model_type
class AppErrorLog:
    model_type = types.ModelTypes.SYSTEM
    component = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    action = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    error_message = Attribute(field_type=types.FieldTypes.MULTI_LINE)
    error_time = Attribute(field_type=types.FieldTypes.DATETIME)
    user_uid = Attribute(field_type=types.FieldTypes.SINGLE_LINE)


@model_type
class AppGridView:
    _title = "name"
    model_type = types.ModelTypes.SYSTEM
    name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    model = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    columns = Attribute(field_type=types.FieldTypes.OBJECT)
    config = Attribute(field_type=types.FieldTypes.OBJECT)
    permissions = Attribute(field_type=types.FieldTypes.OBJECT)
    owner = Attribute(field_type=types.FieldTypes.SINGLE_LINE)


@model_type
class AppUploadsCache:
    _model_type = types.ModelTypes.SYSTEM
    _singular_name = "AppUploadsCache"
    _plural_name = "AppUploadsCache"
    _table_name = "app_uploads_cache"
    _title = "name"
    name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    mime_type = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    size = Attribute(field_type=types.FieldTypes.NUMBER)
    meta_info = Attribute(field_type=types.FieldTypes.OBJECT)
    link_name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    link_uid = Attribute(field_type=types.FieldTypes.UID)
    content = Attribute(field_type=types.FieldTypes.MEDIA)


@model_type
class AppCustomFieldsSchema:
    _model_type = types.ModelTypes.SYSTEM
    _title = "name"
    name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    model = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    schema = Attribute(field_type=types.FieldTypes.OBJECT)


@model_type
class Upload:
    _title = "name"
    name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    mime_type = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    size = Attribute(field_type=types.FieldTypes.NUMBER)
    meta_info = Attribute(field_type=types.FieldTypes.OBJECT)
    link_name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    link_uid = Attribute(field_type=types.FieldTypes.UID)
    location = Attribute(field_type=types.FieldTypes.OBJECT)


@model_type
class File:
    model_type = types.ModelTypes.SYSTEM
    path = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    file = Attribute(field_type=types.FieldTypes.MEDIA)
    file_version = Attribute(field_type=types.FieldTypes.SINGLE_LINE)


@model_type
class Tenant:
    model_type = types.ModelTypes.SYSTEM
    name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    status = Attribute(field_type=types.FieldTypes.ENUM_SINGLE)


@model_type
class SubscriptionPlan:
    model_type = types.ModelTypes.SYSTEM
    name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    description = Attribute(field_type=types.FieldTypes.MULTI_LINE)
    price = Attribute(field_type=types.FieldTypes.CURRENCY)
    features = Attribute(field_type=types.FieldTypes.OBJECT)
    status = Attribute(field_type=types.FieldTypes.ENUM_SINGLE)


@model_type
class User:
    _title = "full_name"

    model_type = types.ModelTypes.SYSTEM
    first_name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    last_name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    email = Attribute(field_type=types.FieldTypes.EMAIL)
    enabled = Attribute(field_type=types.FieldTypes.BOOLEAN)
    last_login = Attribute(field_type=types.FieldTypes.DATETIME)
    password_hash = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    n_password_failures = Attribute(field_type=types.FieldTypes.NUMBER)
    confirmed_email = Attribute(field_type=types.FieldTypes.BOOLEAN)
    signed_up = Attribute(field_type=types.FieldTypes.DATETIME)
    user_roles = Relationship("UserRole", with_many=True)

    permissions_schema = {
        "administrator": Attribute(field_type=types.FieldTypes.BOOLEAN),
    }
    permissions = Attribute(field_type=types.FieldTypes.OBJECT, schema=permissions_schema)

    @staticmethod
    def get_full_name(args):
        return f"{args['first_name']} {args['last_name']}"
    full_name = Computed(("first_name", "last_name"), "get_full_name")


@model_type
class UserRole:
    _title = "name"

    model_type = types.ModelTypes.SYSTEM
    name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    description = Attribute(field_type=types.FieldTypes.MULTI_LINE)
    status = Attribute(field_type=types.FieldTypes.ENUM_SINGLE)
    permissions_schema = {
        "administrator": Attribute(field_type=types.FieldTypes.BOOLEAN),
    }
    permissions = Attribute(field_type=types.FieldTypes.OBJECT, schema=permissions_schema)


@model_type
class UserProfile:
    _title = "user"
    user = Relationship("User")


# -------------------------
# Data object model classes
# -------------------------
@model_type
class Business:
    _title = "name"

    name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    address_schema = {
        "address_line_1": Attribute(field_type=types.FieldTypes.SINGLE_LINE),
        "address_line_2": Attribute(field_type=types.FieldTypes.SINGLE_LINE),
        "city_district": Attribute(field_type=types.FieldTypes.SINGLE_LINE),
        "state_province": Attribute(field_type=types.FieldTypes.SINGLE_LINE),
        "country": Attribute(field_type=types.FieldTypes.SINGLE_LINE),
        "postal_code": Attribute(field_type=types.FieldTypes.SINGLE_LINE),
    }
    address = Attribute(field_type=types.FieldTypes.OBJECT, schema=address_schema)
    phone = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    email = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    website = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    logo = Attribute(field_type=types.FieldTypes.MEDIA)
    subscription_schema = {
        "plan": Attribute(field_type=types.FieldTypes.SINGLE_LINE),
        "status": Attribute(field_type=types.FieldTypes.ENUM_SINGLE),
        "start_date": Attribute(field_type=types.FieldTypes.DATE),
        "end_date": Attribute(field_type=types.FieldTypes.DATE),
        "trial_start": Attribute(field_type=types.FieldTypes.DATE),
        "trial_end": Attribute(field_type=types.FieldTypes.DATE),
        "current_period_start": Attribute(field_type=types.FieldTypes.DATE),
        "current_period_end": Attribute(field_type=types.FieldTypes.DATE),
    }
    subscription = Attribute(field_type=types.FieldTypes.OBJECT, schema=subscription_schema)


@model_type
class Calendar:
    _title = "name"

    name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    description = Attribute(field_type=types.FieldTypes.MULTI_LINE)
    week_start = Attribute(field_type=types.FieldTypes.ENUM_SINGLE)
    workdays = Attribute(field_type=types.FieldTypes.ENUM_MULTI)
    weekend = Attribute(field_type=types.FieldTypes.ENUM_MULTI)
    public_holidays = Attribute(field_type=types.FieldTypes.OBJECT)
    special_holidays = Attribute(field_type=types.FieldTypes.OBJECT)
    status = Attribute(field_type=types.FieldTypes.ENUM_SINGLE)


@model_type
class Employee:
    _title = "full_name"

    first_name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    last_name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    email = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    mobile = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    role = Relationship("EmployeeRole", with_many=True)
    status = Attribute(field_type=types.FieldTypes.ENUM_SINGLE)
    address_schema = {
        "address_line_1": Attribute(field_type=types.FieldTypes.SINGLE_LINE),
        "address_line_2": Attribute(field_type=types.FieldTypes.SINGLE_LINE),
        "city_district": Attribute(field_type=types.FieldTypes.SINGLE_LINE),
        "state_province": Attribute(field_type=types.FieldTypes.SINGLE_LINE),
        "country": Attribute(field_type=types.FieldTypes.SINGLE_LINE),
        "postal_code": Attribute(field_type=types.FieldTypes.SINGLE_LINE),
    }
    address = Attribute(field_type=types.FieldTypes.OBJECT, schema=address_schema)
    custom_fields = Attribute(field_type=types.FieldTypes.OBJECT)

    @staticmethod
    def get_full_name(args):
        return f"{args['first_name']} {args['last_name']}"

    full_name = Computed(("first_name", "last_name"), "get_full_name")


@model_type
class EmployeeRole:
    _title = "name"

    name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    pay_rate = Attribute(field_type=types.FieldTypes.CURRENCY)
    pay_rate_template = Relationship("PayRateTemplate")
    status = Attribute(field_type=types.FieldTypes.ENUM_SINGLE)


@model_type
class Job:
    _title = "name"

    job_type = Relationship("JobType")
    location = Relationship("Location")
    name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    number = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    description = Attribute(field_type=types.FieldTypes.MULTI_LINE)
    status = Attribute(field_type=types.FieldTypes.ENUM_SINGLE)
    custom_fields = Attribute(field_type=types.FieldTypes.OBJECT)


@model_type
class JobType:
    _title = "shot_code"

    name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    shot_code = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    description = Attribute(field_type=types.FieldTypes.MULTI_LINE)
    pay_rate_template = Relationship("PayRateTemplate")


@model_type
class Location:
    _title = "name"

    name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    description = Attribute(field_type=types.FieldTypes.MULTI_LINE)
    address_schema = {
        "address_line_1": Attribute(field_type=types.FieldTypes.SINGLE_LINE),
        "address_line_2": Attribute(field_type=types.FieldTypes.SINGLE_LINE),
        "city_district": Attribute(field_type=types.FieldTypes.SINGLE_LINE),
        "state_province": Attribute(field_type=types.FieldTypes.SINGLE_LINE),
        "country": Attribute(field_type=types.FieldTypes.SINGLE_LINE),
        "postal_code": Attribute(field_type=types.FieldTypes.SINGLE_LINE),
    }
    address = Attribute(field_type=types.FieldTypes.OBJECT, schema=address_schema)
    pay_rate_template = Relationship("PayRateTemplate")
    status = Attribute(field_type=types.FieldTypes.ENUM_SINGLE)

    @staticmethod
    def get_address_oneline(args):
        address_online = ''
        address_online += f'{args["address"]["address_line_1"]}, ' if args["address"]["address_line_1"] else ''
        address_online += f'{args["address"]["address_line_2"]}, ' if args["address"]["address_line_2"] else ''
        address_online += f'{args["address"]["city_district"]}, ' if args["address"]["city_district"] else ''
        address_online += f'{args["address"]["state_province"]}, ' if args["address"]["state_province"] else ''
        address_online += f'{args["address"]["country"]}, ' if args["address"]["country"] else ''
        address_online += f'{args["address"]["postal_code"]}' if args["address"]["postal_code"] else ''
        return address_online
    address_oneline = Computed(["address"], "get_address_oneline")


@model_type
class PayCategory:
    _title = "name"

    name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    pay_category_type = Attribute(field_type=types.FieldTypes.ENUM_SINGLE)
    description = Attribute(field_type=types.FieldTypes.MULTI_LINE)
    pay_rate = Attribute(field_type=types.FieldTypes.CURRENCY)
    pay_rate_type = Attribute(field_type=types.FieldTypes.ENUM_SINGLE)
    pay_rate_multiplier = Attribute(field_type=types.FieldTypes.NUMBER)
    status = Attribute(field_type=types.FieldTypes.ENUM_SINGLE)


@model_type
class PayRateRule:
    _title = "name"

    name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    description = Attribute(field_type=types.FieldTypes.MULTI_LINE)
    pay_rate = Attribute(field_type=types.FieldTypes.CURRENCY)
    pay_rate_type = Attribute(field_type=types.FieldTypes.ENUM_SINGLE)
    pay_rate_multiplier = Attribute(field_type=types.FieldTypes.NUMBER)
    pay_category = Relationship("PayCategory")
    calculation_settings = Attribute(field_type=types.FieldTypes.OBJECT)
    status = Attribute(field_type=types.FieldTypes.ENUM_SINGLE)


@model_type
class PayRateTemplate:
    _title = "name"
    name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    description = Attribute(field_type=types.FieldTypes.MULTI_LINE)
    scope = Relationship("Scope")
    status = Attribute(field_type=types.FieldTypes.ENUM_SINGLE)


@model_type
class PayRateTemplateItem:
    _title = "pay_rate_rule.name"
    pay_rate_template = Relationship("PayRateTemplate")
    pay_rate_rule = Relationship("PayRateRule")
    pay_rate = Attribute(field_type=types.FieldTypes.CURRENCY)
    pay_rate_multiplier = Attribute(field_type=types.FieldTypes.NUMBER)
    pay_rate_title = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    status = Attribute(field_type=types.FieldTypes.ENUM_SINGLE)


@model_type
class PayRun:
    _title = "reference"

    pay_run_type = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    pay_period_start = Attribute(field_type=types.FieldTypes.DATE)
    pay_period_end = Attribute(field_type=types.FieldTypes.DATE)
    pay_date = Attribute(field_type=types.FieldTypes.DATE)
    status = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    notes = Attribute(field_type=types.FieldTypes.MULTI_LINE)

    @staticmethod
    def get_payrun_reference(args):
        return f"{args['pay_run_type']}: ({args['pay_period_start']} - {args['pay_period_end']})"
    reference = Computed(
        ("pay_run_type", "pay_period_start", "pay_period_end"), "get_payrun_reference"
    )

    @staticmethod
    def get_payrun_week(args):
        return  f"{args['pay_period_end'].year} - WK{args['pay_period_end'].isocalendar()[1]}"
    payrun_week = Computed(["pay_period_end"], "get_payrun_week")


@model_type
class PayRunConfig:
    _title = "name"

    name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    type = Attribute(field_type=types.FieldTypes.ENUM_SINGLE)
    pay_period_start_day = Attribute(field_type=types.FieldTypes.ENUM_SINGLE)
    pay_period_end_day = Attribute(field_type=types.FieldTypes.ENUM_SINGLE)
    pay_day = Attribute(field_type=types.FieldTypes.ENUM_SINGLE)
    scopes = Relationship("Scope", with_many=True)
    status = Attribute(field_type=types.FieldTypes.ENUM_SINGLE)


@model_type
class PayRunItem:
    _title = "title"

    pay_run = Relationship("PayRun")
    employee = Relationship("Employee")
    timesheet = Relationship("Timesheet")
    pay_category = Relationship("PayCategory")
    title = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    pay_rate = Attribute(field_type=types.FieldTypes.CURRENCY)
    units = Attribute(field_type=types.FieldTypes.NUMBER)
    amount = Attribute(field_type=types.FieldTypes.CURRENCY)
    status = Attribute(field_type=types.FieldTypes.ENUM_SINGLE)


@model_type
class Scope:
    _title = "name"

    name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    description = Attribute(field_type=types.FieldTypes.MULTI_LINE)
    type = Relationship("ScopeType")
    custom_fields = Attribute(field_type=types.FieldTypes.OBJECT)
    status = Attribute(field_type=types.FieldTypes.ENUM_SINGLE)


@model_type
class ScopeType:
    _title = "name"

    name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    description = Attribute(field_type=types.FieldTypes.MULTI_LINE)
    pay_rate_template = Relationship("PayRateTemplate")
    status = Attribute(field_type=types.FieldTypes.ENUM_SINGLE)