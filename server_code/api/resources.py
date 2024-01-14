from ..app import models
from anvil.tables import query as q
import anvil.tables as tables
import json
import datetime


def get_timesheet_filters(params, integration_uid):
    start_date = params.get('start_date', '')
    end_date = params.get('end_date', '')
    employee_uid = params.get('employee_uid', None)
    employee_link_id = params.get('employee_link_id', None)
    filters = {}
    if employee_uid:
        employee = models.Employee.get(employee_uid)
        if employee is not None:
            filters['employee'] = employee
    elif employee_link_id:
        filters['remote_links'] = {integration_uid: employee_link_id}
    if start_date and not end_date:
        filters['date'] = q.greater_than_or_equal_to(start_date)
    elif end_date and not start_date:
        filters['date'] = q.less_than_or_equal_to(end_date)
    elif start_date and end_date:
        filters['date'] = q.between(start_date, end_date, max_inclusive=True)
    return filters


EMPLOYEE_JSON_SCHEMA = {
    'fields': [
        'uid',
        'first_name',
        'last_name',
        'email',
        'mobile',
        'status',
        'address',
        'custom_fields',
        'remote_links',
    ],
    'relationships': {
        'role': {
            'fields': [
                'name',
                'pay_rate',
            ],
        },
    },
}

EMPLOYEE_ROLE_JSON_SCHEMA = {
    'fields': [
        'uid',
        'name',
        'pay_rate',
        'status',
        'remote_links',
    ]
}


JOB_JSON_SCHEMA = {
    'fields': [
        'uid',
        'name',
        'number',
        'description',
        'status',
        'custom_fields',
        'remote_links',
    ],
    'relationships': {
        'job_type': {
            'fields': [
                'name',
                'short_code',
            ],
        },
        'location': {
            'fields': [
                'name',
                'address',
            ],
        },
    },
}

JOB_TYPE_JSON_SCHEMA = {
    'fields': [
        'uid',
        'name',
        'short_code',
        'description',
        'remote_links',
    ],
}

LOCATION_JSON_SCHEMA = {
    'fields': [
        'uid',
        'name',
        'description',
        'address',
        'remote_links',
    ],
}

TIMESHEET_JSON_SCHEMA = {
    'fields': [
        'uid',
        'date',
        'start_time',
        'end_time',
        'total_hours',
        'total_pay',
        'pay_lines',
        'status',
        'notes',
        'remote_links',
    ],
    'relationships': {
        'timesheet_type': {
            'fields': [
                'name',
                'short_code',
            ],
        },
        'employee': {
            'fields': [
                'full_name',
            ],
        },
        'approved_by': {
            'fields': [
                'full_name',
            ],
        },
        'payrun': {
            'fields': [
                'name',
            ],
        },
        'job': {
            'fields': [
                'name',
            ],
        },
    },
}

TIMESHEET_TYPE_JSON_SCHEMA = {
    'fields': [
        'uid',
        'name',
        'short_code',
        'description',
        'status',
        'configuration',
        'remote_links',
    ],
}

API_RESOURCES = {

    'employees': {
        'model': models.Employee,
        'json_schema': EMPLOYEE_JSON_SCHEMA,
        'sorting': [
            tables.order_by('first_name', ascending=True),
            tables.order_by('last_name', ascending=True),
        ],
        'pagination': True,
        'remote_links': True,
        'filters': None,
    },

    'employee_roles': {
        'model': models.EmployeeRole,
        'json_schema': EMPLOYEE_ROLE_JSON_SCHEMA,
        'sorting': [
            tables.order_by('name', ascending=True),
        ],
        'pagination': False,
        'remote_links': True,
        'filters': None,
    },

    'jobs': {
        'model': models.Job,
        'json_schema': JOB_JSON_SCHEMA,
        'sorting': [
            tables.order_by('number', ascending=True),
        ],
        'pagination': True,
        'remote_links': True,
        'filters': None,
    },

    'job_types': {
        'model': models.JobType,
        'json_schema': JOB_TYPE_JSON_SCHEMA,
        'sorting': [
            tables.order_by('name', ascending=True),
        ],
        'pagination': False,
        'remote_links': True,
        'filters': None,
    },

    'location': {
        'model': models.Location,
        'json_schema': LOCATION_JSON_SCHEMA,
        'sorting': [
            tables.order_by('name', ascending=True),
        ],
        'pagination': False,
        'remote_links': True,
        'filters': None,
    },

    'timesheets': {
        'model': models.Timesheet,
        'json_schema': TIMESHEET_JSON_SCHEMA,
        'sorting': [
            tables.order_by('employee', ascending=True),
            tables.order_by('date', ascending=True),
        ],
        'pagination': True,
        'remote_links': True,
        'filters': get_timesheet_filters,
    },

    'timesheet_types': {
        'model': models.TimesheetType,
        'json_schema': TIMESHEET_TYPE_JSON_SCHEMA,
        'sorting': [
            tables.order_by('name', ascending=True),
        ],
        'pagination': False,
        'remote_links': True,
        'filters': None,
    },

    'payruns': {
        'model': 'Payrun',
        'name_field': 'name',
    },
}

