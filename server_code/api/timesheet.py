from ..app.models import Timesheet
from .. import api
import anvil.server
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
            page = int(params.get('page', 1))
            timesheets = Timesheet.search(page=page, page_length=TIMESHEET_PAGE_LENGTH)
            print(timesheets.count, timesheets.total_pages, timesheets.page_length, timesheets.page)
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
