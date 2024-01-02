import anvil.server


@anvil.server.http_endpoint("/test")
def test_endpoint(**params):
    # auth, message = authenticate_request(anvil.server.request)
    # if not auth:
    #     return anvil.server.HttpResponse(401, message)
    return (f"method: {anvil.server.request.method}, headers: {anvil.server.request.headers}\n"
            # f"timesheet_uid: {timesheet_uid}, params: {params}\n"
            f"body: {anvil.server.request.body_json}\n")
