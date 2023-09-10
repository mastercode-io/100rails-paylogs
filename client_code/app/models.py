from AnvilFusion.datamodel.particles import (
    model_type,
    Attribute,
    Relationship,
    Computed,
)
from AnvilFusion.datamodel import types


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


@model_type
class User:
    model_type = types.ModelTypes.SYSTEM
    email = Attribute(field_type=types.FieldTypes.EMAIL)
    enabled = Attribute(field_type=types.FieldTypes.BOOLEAN)
    last_login = Attribute(field_type=types.FieldTypes.DATETIME)
    password_hash = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    n_password_failures = Attribute(field_type=types.FieldTypes.NUMBER)
    confirmed_email = Attribute(field_type=types.FieldTypes.BOOLEAN)
    signed_up = Attribute(field_type=types.FieldTypes.DATETIME)


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


@model_type
class Employee:
    _title = "full_name"

    first_name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    last_name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    email = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    mobile = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    role = Relationship("EmployeeRole", with_many=True)

    address_schema = {
        "address_line_1": Attribute(field_type=types.FieldTypes.SINGLE_LINE),
        "address_line_2": Attribute(field_type=types.FieldTypes.SINGLE_LINE),
        "city_district": Attribute(field_type=types.FieldTypes.SINGLE_LINE),
        "state_province": Attribute(field_type=types.FieldTypes.SINGLE_LINE),
        "country": Attribute(field_type=types.FieldTypes.SINGLE_LINE),
        "postal_code": Attribute(field_type=types.FieldTypes.SINGLE_LINE),
    }
    address = Attribute(field_type=types.FieldTypes.OBJECT, schema=address_schema)

    @staticmethod
    def get_full_name(args):
        return f"{args['first_name']} {args['last_name']}"

    full_name = Computed(("first_name", "last_name"), "get_full_name")


@model_type
class EmployeeRole:
    _title = "name"

    name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    pay_rate = Attribute(field_type=types.FieldTypes.CURRENCY)


@model_type
class Job:
    _title = "name"

    job_type = Relationship("JobType")
    location = Relationship("Location")
    name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    description = Attribute(field_type=types.FieldTypes.MULTI_LINE)
    status = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    custom_fields = Attribute(field_type=types.FieldTypes.OBJECT)


@model_type
class JobType:
    _title = "name"

    name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    description = Attribute(field_type=types.FieldTypes.MULTI_LINE)


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


@model_type
class PayCategory:
    _title = "name"

    name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    description = Attribute(field_type=types.FieldTypes.MULTI_LINE)
    pay_rate = Attribute(field_type=types.FieldTypes.CURRENCY)
    pay_rate_type = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    pay_rate_multiplier = Attribute(field_type=types.FieldTypes.NUMBER)


@model_type
class PayRateTemplate:
    _title = "name"


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


@model_type
class Timesheet:
    _title = "employee"

    employee = Relationship("Employee")
    timesheet_type = Relationship("TimesheetType")
    job = Relationship("Job")
    date = Attribute(field_type=types.FieldTypes.DATE)
    start_time = Attribute(field_type=types.FieldTypes.DATETIME)
    end_time = Attribute(field_type=types.FieldTypes.DATETIME)
    total_pay = Attribute(field_type=types.FieldTypes.CURRENCY)
    status = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    approved_by = Relationship("Employee")
    notes = Attribute(field_type=types.FieldTypes.MULTI_LINE)

    @staticmethod
    def calculate_total_hours(args):
        return (args["end_time"] - args["start_time"]).total_seconds() / 3600

    # total_hours = Computed(("start_time", "end_time"), "calculate_total_hours")


@model_type
class TimesheetType:
    _title = "short_code"

    short_code = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    description = Attribute(field_type=types.FieldTypes.MULTI_LINE)
    notes = Attribute(field_type=types.FieldTypes.MULTI_LINE)

    configuration_schema = {
        "job_required": Attribute(field_type=types.FieldTypes.BOOLEAN),
        "paid_time": Attribute(field_type=types.FieldTypes.BOOLEAN),
        "paid_breaks": Attribute(field_type=types.FieldTypes.BOOLEAN),
        "break_length": Attribute(field_type=types.FieldTypes.NUMBER),
        "work_time": Attribute(field_type=types.FieldTypes.BOOLEAN),
        "break_time": Attribute(field_type=types.FieldTypes.BOOLEAN),
        "sick_leave": Attribute(field_type=types.FieldTypes.BOOLEAN),
        "annual_leave": Attribute(field_type=types.FieldTypes.BOOLEAN),
        "unpaid_leave": Attribute(field_type=types.FieldTypes.BOOLEAN),
        "other": Attribute(field_type=types.FieldTypes.BOOLEAN),
    }
    configuration = Attribute(
        field_type=types.FieldTypes.OBJECT, schema=configuration_schema
    )
