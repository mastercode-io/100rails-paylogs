from ..app.models import Timesheet
from .. import api
import anvil.server
import json
import datetime
import itertools


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
TIMESHEET_PAGE_LENGTH = 10


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
            timesheets = itertools.islice(Timesheet.search(),
                                          (page - 1) * TIMESHEET_PAGE_LENGTH,
                                          page * TIMESHEET_PAGE_LENGTH)
            timesheets = [ts.to_json_dict(json_schema=TIMESHEET_JSON_SCHEMA) for ts in timesheets]
            for i in range(3):
                print(f"timesheet {i}: {timesheets[i]}")
            return anvil.server.HttpResponse(
                200,
                json.dumps(timesheets),
                {'content-type': 'application/json'},
            )
