from AnvilFusion.datamodel.particles import model_type, Attribute, Relationship, Computed
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
    _title = 'name'
    model_type = types.ModelTypes.SYSTEM
    name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    model = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    columns = Attribute(field_type=types.FieldTypes.OBJECT)
    config = Attribute(field_type=types.FieldTypes.OBJECT)
    permissions = Attribute(field_type=types.FieldTypes.OBJECT)
    owner = Attribute(field_type=types.FieldTypes.SINGLE_LINE)


@model_type
class AppUploadsCahce:
    _model_type = types.ModelTypes.SYSTEM
    _singular_name = 'AppUploadsCahce'
    _plural_name = 'AppUploadsCahce'
    _table_name = 'app_uploads_cache'
    _title = 'name'
    name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    mime_type = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    size = Attribute(field_type=types.FieldTypes.NUMBER)
    meta_info = Attribute(field_type=types.FieldTypes.OBJECT)
    link_name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    link_uid = Attribute(field_type=types.FieldTypes.UID)
    content = Attribute(field_type=types.FieldTypes.MEDIA)


@model_type
class Upload:
    _title = 'name'
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
    _title = 'user'
    user = Relationship('User')


# -------------------------
# Data object model classes
# -------------------------
@model_type
class Business:
    _title = 'name'

    name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    address_schema = {
        'address_line_1': Attribute(field_type=types.FieldTypes.SINGLE_LINE),
        'address_line_2': Attribute(field_type=types.FieldTypes.SINGLE_LINE),
        'city_district': Attribute(field_type=types.FieldTypes.SINGLE_LINE),
        'state_province': Attribute(field_type=types.FieldTypes.SINGLE_LINE),
        'country': Attribute(field_type=types.FieldTypes.SINGLE_LINE),
        'postal_code': Attribute(field_type=types.FieldTypes.SINGLE_LINE),
    }
    address = Attribute(field_type=types.FieldTypes.OBJECT, schema=address_schema)
    phone = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    email = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    website = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    logo = Attribute(field_type=types.FieldTypes.MEDIA)


@model_type
class Employee:
    _title = 'full_name'

    first_name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    last_name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    email = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    mobile = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    role = Relationship('EmployeeRole', with_many=True)
    
    address_schema = {
        'address_line_1': Attribute(field_type=types.FieldTypes.SINGLE_LINE),
        'address_line_2': Attribute(field_type=types.FieldTypes.SINGLE_LINE),
        'city_district': Attribute(field_type=types.FieldTypes.SINGLE_LINE),
        'state_province': Attribute(field_type=types.FieldTypes.SINGLE_LINE),
        'country': Attribute(field_type=types.FieldTypes.SINGLE_LINE),
        'postal_code': Attribute(field_type=types.FieldTypes.SINGLE_LINE),
    }
    address = Attribute(field_type=types.FieldTypes.OBJECT, schema=address_schema)

    @staticmethod
    def get_full_name(args):
        return f"{args['first_name']} {args['last_name']}"
    full_name = Computed(('first_name', 'last_name'), 'get_full_name')


@model_type
class EmployeeRole:
    _title = 'name'

    name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    pay_rate = Attribute(field_type=types.FieldTypes.CURRENCY)
    

@model_type
class Job:
    _title = 'name'

    name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    description = Attribute(field_type=types.FieldTypes.MULTI_LINE)
    status = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    job_type = Relationship('JobType')
    location = Relationship('Location')
    
    
@model_type
class JobType:
    _title = 'name'

    name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    description = Attribute(field_type=types.FieldTypes.MULTI_LINE)
    pay_rate_template = Relationship('PayRateTemplate')


@model_type
class Location:
    _title = 'name'

    name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    description = Attribute(field_type=types.FieldTypes.MULTI_LINE)
    address_schema = {
        'address_line_1': Attribute(field_type=types.FieldTypes.SINGLE_LINE),
        'address_line_2': Attribute(field_type=types.FieldTypes.SINGLE_LINE),
        'city_district': Attribute(field_type=types.FieldTypes.SINGLE_LINE),
        'state_province': Attribute(field_type=types.FieldTypes.SINGLE_LINE),
        'country': Attribute(field_type=types.FieldTypes.SINGLE_LINE),
        'postal_code': Attribute(field_type=types.FieldTypes.SINGLE_LINE),
    }
    address = Attribute(field_type=types.FieldTypes.OBJECT, schema=address_schema)


@model_type
class PayCategory:
    _title = 'name'

    name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    description = Attribute(field_type=types.FieldTypes.MULTI_LINE)
    pay_rate = Attribute(field_type=types.FieldTypes.CURRENCY)
    pay_rate_type = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    pay_rate_multiplier = Attribute(field_type=types.FieldTypes.NUMBER)


@model_type
class PayRateTemplate:
    _title = 'name'


@model_type
class Timesheet:
    _title = 'employee'

    employee = Relationship('Employee')
    job = Relationship('Job')
    start_time = Attribute(field_type=types.FieldTypes.DATETIME)
    end_time = Attribute(field_type=types.FieldTypes.DATETIME)
    total_hours = Attribute(field_type=types.FieldTypes.NUMBER)
    total_pay = Attribute(field_type=types.FieldTypes.CURRENCY)
    status = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    timesheet_line = Relationship('TimesheetLine', with_many=True)


