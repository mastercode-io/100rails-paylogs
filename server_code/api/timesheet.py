from ..app.models import Timesheet
from .. import api
import anvil.server
import json
import datetime


TIMESHEET_JSON_FIELDS = {
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


@anvil.server.http_endpoint("/timesheets/:timesheet_uid", methods=["GET", "POST"])
def test_endpoint(timesheet_uid, **params):
    auth, http_response = api.authenticate_request(anvil.server.request)
    if not auth:
        return http_response
    print(f"method: {anvil.server.request.method}, headers: {anvil.server.request.headers}\n"
          f"timesheet_uid: {timesheet_uid}, params: {params}\n"
          f"body: {anvil.server.request.body_json}\n")
    if anvil.server.request.method == "GET":
        if timesheet_uid:
            timesheet = Timesheet.get(timesheet_uid)
            if timesheet:
                return json.dumps(timesheet.to_dict())
            else:
                return anvil.server.HttpResponse(404, f"Timesheet not found: {timesheet_uid}")
        else:
            # timesheets = Timesheet.get_json_view({'columns': TIMESHEET_JSON_FIELDS})
            timesheets = Timesheet.get_json_view({'columns': TIMESHEET_JSON_FIELDS}, )
            for i in range(10):
                print(f"timesheet {i}: {timesheets[i]}")
            return anvil.server.HttpResponse(
                200,
                json.dumps(timesheets),
                {'content-type': 'application/json'},
            )
