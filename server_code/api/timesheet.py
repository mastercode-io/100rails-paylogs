from ..app.models import Timesheet
from .. import api
import anvil.server
import json
import datetime

# timesheet_type = Relationship("TimesheetType")
# employee = Relationship("Employee")
# payrun = Relationship("Payrun")
# job = Relationship("Job")
# date = Attribute(field_type=types.FieldTypes.DATE)
# start_time = Attribute(field_type=types.FieldTypes.DATETIME)
# end_time = Attribute(field_type=types.FieldTypes.DATETIME)
# status = Attribute(field_type=types.FieldTypes.ENUM_SINGLE)
# approved_by = Relationship("Employee")
# notes = Attribute(field_type=types.FieldTypes.MULTI_LINE)
# total_pay = Attribute(field_type=types.FieldTypes.CURRENCY)
# pay_lines = Attribute(field_type=types.FieldTypes.OBJECT)

TIMESHEET_JSON_FIELDS = [
    {'name': 'uid'},
    {'name': 'timesheet_type'},
    {'name': 'employee'},
    {'name': 'approved_by'},
    {'name': 'payrun.name'},
    {'name': 'job'},
    {'name': 'date'},
    {'name': 'start_time'},
    {'name': 'end_time'},
    {'name': 'total_hours'},
    {'name': 'total_pay'},
    {'name': 'pay_lines'},
    {'name': 'status'},
    {'name': 'notes'},
]


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
            return anvil.server.HttpResponse(
                200,
                json.dumps(timesheets),
                {'content-type': 'application/json'},
            )
