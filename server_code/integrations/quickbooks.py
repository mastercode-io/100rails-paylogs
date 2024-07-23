from AnvilFusion.server import utils as fusion_server_utils
import anvil.server
import anvil.users
import anvil.secrets
from anvil import app
from intuitlib.client import AuthClient
from intuitlib.enums import Scopes
import base64
import json
import uuid


QB_AUTH = json.loads(anvil.secrets.get_secret('qb_auth_sandbox'))
QB_CLIENT_ID = QB_AUTH['client_id']
QB_CLIENT_SECRET = QB_AUTH['client_secret']
QB_OAUTH_REDIRECT_URL = 'https://bbezaphmpn72gfkm.anvil.app/XOLVUAFPYYUDPOS3TNHURVTN/_/api/integrations/qb/auth'


@anvil.server.callable
def get_qb_auth_url(tenant_uid):
    qb_auth_client = AuthClient(
        QB_CLIENT_ID,
        QB_CLIENT_SECRET,
        QB_OAUTH_REDIRECT_URL,
        'sandbox',
    )
    qb_auth_url = qb_auth_client.get_authorization_url([Scopes.ACCOUNTING], state_token=tenant_uid)
    print('quickbooks auth url', qb_auth_url)
    return qb_auth_url


@anvil.server.http_endpoint("integrations/qb/auth", methods=["GET", "POST"])
def qb_auth(**params):
    print(f"method: {anvil.server.request.method}\n"
          f"headers: {anvil.server.request.headers}\n"
          f"params: {params}\n")

    tenant_uid = params.get("state", None)
    print("tenant_uid", tenant_uid)

    return anvil.server.HttpResponse(200, "OK")
