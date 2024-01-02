from ..app.models import Timesheet
from . import *
import anvil.server
import json
import datetime


# @anvil.server.http_endpoint("/test")
# def test_endpoint(**params):
#     auth, message = authenticate_request(anvil.server.request)
#     if not auth:
#         return anvil.server.HttpResponse(401, message)
#     return (f"method: {anvil.server.request.method}, headers: {anvil.server.request.headers}\n"
#             # f"timesheet_uid: {timesheet_uid}, params: {params}\n"
#             f"body: {anvil.server.request.body_json}\n")
    # if anvil.server.request.method == "GET":
    #     timesheet = Timesheet.get(timesheet_uid)
    #     return json.dumps(timesheet.to_dict())
    # elif anvil.server.request.method == "POST":
    #     data = anvil.server.request.body_json
    #     timesheet = Timesheet.get(timesheet_uid)
    #     timesheet.update(data)
    #     return json.dumps(timesheet.to_dict())
