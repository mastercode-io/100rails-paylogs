from AnvilFusion.tools.utils import init_user_session
from ..app.models import Tenant
import anvil.server
import anvil.users
import anvil.secrets
import base64
import json
import uuid
import secrets
import string
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


ACCESS_DENIED_RESPONSE = anvil.server.HttpResponse(401, "Access Denied. Authentication failed.")


def generate_password(length=16):
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(length))
    return password


def get_api_user_email(tenant_uid, api_user_name):
    return f'{tenant_uid}_{api_user_name}@paylogs.com'


@anvil.server.callable
def generate_tenant_api_key(tenant_uid, api_user_name):
    tenant = Tenant.get(tenant_uid)
    if not tenant:
        raise Exception(f'Tenant {tenant_uid} not found')
    if not tenant['api_secret']:
        api_secret = generate_password()
        tenant['api_secret'] = api_secret
    secret_key = tenant['api_secret']
    api_user_password = generate_password()
    api_user_email = get_api_user_email(tenant_uid, api_user_name)
    api_user = anvil.users.signup_with_email(api_user_email, api_user_password)
    api_user.update(
        tenant_uid=tenant_uid,
        uid=str(uuid.uuid4()),
        confirmed_email=True,
        first_name=api_user_name,
        last_name='API User',
    )

    cipher = AES.new(secret_key.encode(), AES.MODE_EAX)
    cipher_text, tag = cipher.encrypt_and_digest(
        json.dumps({'api_user_name': api_user_name, 'password': api_user_password}).encode()
    )
    api_key = base64.urlsafe_b64encode(cipher.nonce + tag + cipher_text).decode()
    if tenant['api_keys'] is not None:
        tenant['api_keys'].append(api_key)
    else:
        tenant['api_keys'] = [api_key]
    tenant.save()
    return api_key


def decode_tenant_api_key(tenant_uid, api_key):
    tenant = Tenant.get(tenant_uid)
    if not tenant:
        raise Exception(f'Tenant {tenant_uid} not found')
    if not tenant['api_secret']:
        raise Exception(f'Tenant {tenant_uid} has no API secret')
    secret_key = tenant['api_secret']
    encrypted_bytes = base64.urlsafe_b64decode(api_key)
    nonce = encrypted_bytes[:16]
    tag = encrypted_bytes[16:32]
    ciphertext = encrypted_bytes[32:]
    cipher = AES.new(secret_key.encode(), AES.MODE_EAX, nonce=nonce)
    json_bytes = cipher.decrypt_and_verify(ciphertext, tag)
    json_str = json_bytes.decode('utf-8')
    data = json.loads(json_str)

    return data['api_user_name'], data['password']


def authenticate_request(request: anvil.server.request):
    tenant_uid = request.headers.get('X-Tenant-UID', None)
    api_key = request.headers.get('X-API-Key', None)
    if not tenant_uid or not api_key:
        return False
    else:
        api_user_name, api_user_password = decode_tenant_api_key(tenant_uid, api_key)
        api_user_email = get_api_user_email(tenant_uid, api_user_name)
        try:
            anvil.users.login_with_email(api_user_email, api_user_password)
        except anvil.users.AuthenticationFailed:
            return False
        logged_user = init_user_session()
        if not logged_user:
            return False
    return True
