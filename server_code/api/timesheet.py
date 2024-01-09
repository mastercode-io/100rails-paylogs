from ..app.models import Timesheet, Employee
from .. import api
import anvil.server
from anvil.tables import query as q
import anvil.tables as tables
import json
import datetime


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
TIMESHEET_PAGE_LENGTH = 100


@anvil.server.http_endpoint("/timesheets/:timesheet_uid", methods=["GET", "POST"])
def test_endpoint(timesheet_uid, **params):
    integration_name, http_response = api.authenticate_request(anvil.server.request)
    if integration_name is None:
        return http_response
    print(f"method: {anvil.server.request.method}, headers: {anvil.server.request.headers}\n"
          f"timesheet_uid: {timesheet_uid}, params: {params}\n"
          f"body: {anvil.server.request.body_json}\n")

    if anvil.server.request.method == "GET":
        if timesheet_uid:
            timesheet = Timesheet.get(timesheet_uid)
            if timesheet:
                return anvil.server.HttpResponse(
                    200,
                    json.dumps(timesheet.to_json_dict(json_schema=TIMESHEET_JSON_SCHEMA)),
                    {'content-type': 'application/json'},
                )
            else:
                return anvil.server.HttpResponse(404, f"Timesheet not found: {timesheet_uid}")
        else:
            page = params.get('page', 1)
            start_date = params.get('start_date', '')
            end_date = params.get('end_date', '')
            employee_uid = params.get('employee_uid', None)
            employee_link_id = params.get('employee_link_id', None)
            try:
                page = int(page)
            except ValueError:
                page = 1
            try:
                start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
            except (ValueError, TypeError):
                start_date = None
            try:
                end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
            except (ValueError, TypeError):
                end_date = None
            filters = {}
            queries = []
            if employee_uid:
                employee = Employee.get(employee_uid)
                if employee is not None:
                    filters['employee'] = employee
            elif employee_link_id:
                filters['remote_links'] = {integration_name: employee_link_id}
            if start_date and not end_date:
                filters['date'] = q.greater_than_or_equal_to(start_date)
            elif end_date and not start_date:
                filters['date'] = q.less_than_or_equal_to(end_date)
            elif start_date and end_date:
                # filters['date'] = q.all_of(q.greater_than_or_equal_to(start_date), q.less_than_or_equal_to(end_date))
                filters['date'] = q.between(start_date, end_date)
            # filters['search_query'] = tables.order_by('date', ascending=True)
            print('filters:', filters)
            timesheets = Timesheet.search(page=page, page_length=TIMESHEET_PAGE_LENGTH, **filters)
            # print('timesheets search result:')
            # print(timesheets.count, timesheets.total_pages, timesheets.page_length, timesheets.page)
            ts_list = [ts.to_json_dict(json_schema=TIMESHEET_JSON_SCHEMA) for ts in timesheets]
            return anvil.server.HttpResponse(
                200,
                json.dumps({
                    'timesheets': ts_list,
                    'count': len(ts_list),
                    'page': page,
                    # 'links': {
                    #     'next': f'/timesheets?page={page + 1}' if len(ts_list) == TIMESHEET_PAGE_LENGTH else None,
                    #     'prev': f'/timesheets?page={page - 1}' if page > 1 else None,
                    # }
                }),
                {'content-type': 'application/json'},
            )

    elif anvil.server.request.method == "POST":
        if timesheet_uid:
            return anvil.server.HttpResponse(400, f"Invalid request: {anvil.server.request}")
        else:
            timesheet = Timesheet()
            timesheet.from_json_dict(anvil.server.request.body_json, json_schema=TIMESHEET_JSON_SCHEMA)
            timesheet.save()
            return anvil.server.HttpResponse(
                200,
                json.dumps(timesheet.to_json_dict(json_schema=TIMESHEET_JSON_SCHEMA)),
                {'content-type': 'application/json'},
            )
