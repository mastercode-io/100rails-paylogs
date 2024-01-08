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
    stime = datetime.datetime.now()
    integration_name, http_response = api.authenticate_request(anvil.server.request)
    if integration_name is None:
        return http_response
    print(f"method: {anvil.server.request.method}, headers: {anvil.server.request.headers}\n"
          f"timesheet_uid: {timesheet_uid}, params: {params}\n"
          f"body: {anvil.server.request.body_json}\n")
    etime = datetime.datetime.now()
    print(f"authenticate_request time: {round((etime - stime).total_seconds(), 2)}")
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
            stime = datetime.datetime.now()
            timesheets = itertools.islice(Timesheet.search(),
                                          (page - 1) * TIMESHEET_PAGE_LENGTH,
                                          page * TIMESHEET_PAGE_LENGTH)
            etime = datetime.datetime.now()
            print(f"search time: {round((etime - stime).total_seconds(), 2)}")
            ts_list = []
            stime = datetime.datetime.now()
            for ts in timesheets:
                sstime = datetime.datetime.now()
                ts_list.append(ts.to_json_dict(json_schema=TIMESHEET_JSON_SCHEMA))
                eetime = datetime.datetime.now()
                print(f"to_json_dict time: {round((eetime - sstime).total_seconds(), 5)}")
            etime = datetime.datetime.now()
            print(f"for loop time: {round((etime - stime).total_seconds(), 2)}")
            return anvil.server.HttpResponse(
                200,
                json.dumps({
                    'timesheets': ts_list,
                    'count': len(ts_list),
                }),
                {'content-type': 'application/json'},
            )
