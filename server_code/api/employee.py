from ..app.models import Employee, EmployeeRole
from .. import api
import anvil.server
from anvil.tables import query as q
import anvil.tables as tables
import json
import datetime


EMPLOYEE_JSON_SCHEMA = {
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


@anvil.server.http_endpoint("/employees/:employee_uid", methods=["GET", "POST"])
def employee_endpoint(employee_uid, **params):
    integration_uid, http_response = api.authenticate_request(anvil.server.request)
    if integration_uid is None:
        return http_response
    print(f"method: {anvil.server.request.method}, headers: {anvil.server.request.headers}\n"
          f"employee_uid: {employee_uid}, params: {params}\n"
          f"body: {anvil.server.request.body_json}\n")

    if anvil.server.request.method == "GET":

        employee_link_id = params.get('employee_link_id', None)
        if employee_uid or employee_link_id:
            employee= None
            if employee_uid:
                employee = Employee.get(employee_uid)
            elif employee_link_id:
                employee = Employee.get_by('remote_links', {integration_uid: employee_link_id})
            if employee:
                return anvil.server.HttpResponse(
                    200,
                    json.dumps(employee.to_json_dict(json_schema=EMPLOYEE_JSON_SCHEMA)),
                    {'content-type': 'application/json'},
                )
            else:
                return anvil.server.HttpResponse(404, f"Employee not found: {employee_uid}")

        else:
            page = params.get('page', 1)
            page_length = params.get('page_length', 0)
            try:
                page = int(page)
            except ValueError:
                page = 1
            try:
                page_length = int(page_length)
            except ValueError:
                page_length = api.RESPONSE_PAGE_LENGTH
            filters = {'search_query': [
                tables.order_by('last_name', ascending=True),
            ]}
            print('filters:', filters)
            employees = Employee.search(page=page, page_length=page_length, **filters)
            employee_list = [emp.to_json_dict(json_schema=EMPLOYEE_JSON_SCHEMA) for emp in employees]
            employee_uri = f'{anvil.server.get_api_origin()}/employees/?page_length={page_length}'
            url_list = {
                'first': f'{employee_uri}&page=1',
                'last': f'{employee_uri}&page={employees.total_pages}',
            }
            if page > 1:
                url_list['prev'] = f'{employee_uri}&page={page - 1}'
            if page < employees.total_pages:
                url_list['next'] = f'{employee_uri}&page={page + 1}'
            return anvil.server.HttpResponse(
                200,
                json.dumps({
                    'timesheets': employee_list,
                    'count': len(employee_list),
                    'page': page,
                    'total_pages': employees.total_pages,
                    'links': url_list,
                }),
                {'content-type': 'application/json'},
            )

    elif anvil.server.request.method == "POST":
        if employee_uid:
            return anvil.server.HttpResponse(400, f"Invalid request: {anvil.server.request}")
        else:
            timesheet = Employee()
            timesheet.from_json_dict(anvil.server.request.body_json, json_schema=EMPLOYEE_JSON_SCHEMA)
            timesheet.save()
            return anvil.server.HttpResponse(
                200,
                json.dumps(timesheet.to_json_dict(json_schema=EMPLOYEE_JSON_SCHEMA)),
                {'content-type': 'application/json'},
            )
