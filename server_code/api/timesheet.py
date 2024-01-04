from ..app.models import Timesheet
from .. import api
import anvil.server
import json
import datetime


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
            timesheets = Timesheet.search()
            return json.dumps([timesheet.to_dict() for timesheet in timesheets])
    # if anvil.server.request.method == "GET":
    #     timesheet = Timesheet.get(timesheet_uid)
    #     return json.dumps(timesheet.to_dict())
    # elif anvil.server.request.method == "POST":
    #     data = anvil.server.request.body_json
    #     timesheet = Timesheet.get(timesheet_uid)
    #     timesheet.update(data)
    #     return json.dumps(timesheet.to_dict())
