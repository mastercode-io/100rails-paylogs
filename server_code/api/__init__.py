from AnvilFusion.tools.utils import init_user_session
from AnvilFusion.server import utils as fusion_server_utils
from ..app.models import Tenant, User, AppApiService, AppInApiCredential, AppOutApiCredential
import anvil.server
import anvil.users
import anvil.secrets
import base64
import json
import uuid
import secrets
import string
from Crypto.Cipher import AES


ACCESS_DENIED_RESPONSE = anvil.server.HttpResponse(401, "Access Denied. Authentication failed.")


def generate_password(length=16):
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(length))
    return password


def get_api_service_login(tenant_uid, service_name):
    tenant = Tenant.get(tenant_uid)
    return f"{service_name}_{tenant['name']}@paylogs.com"


@anvil.server.callable
def register_api_service(name, description, url, connection_type='in'):
    api_service = AppApiService.get_by('name', name)
    if api_service:
        api_service['description'] = description
        api_service['url'] = url
        api_service['connection_type'] = connection_type
        api_service['status'] = 'active'
    else:
        api_service = AppApiService(
            name=name,
            description=description,
            url=url,
            connection_type=connection_type,
            status='active',
        )
    api_service.save()
    return api_service


@anvil.server.callable
def generate_api_key(tenant_uid, api_service: AppApiService):
    api_service_login = get_api_service_login(tenant_uid, api_service['name'])
    api_service_password = generate_password()
    api_service_user = User.get_by('email', api_service_login)
    if not api_service_user:
        api_user_row = anvil.users.signup_with_email(api_service_login, api_service_password)
        api_user_row.update(
            tenant_uid=tenant_uid,
            uid=str(uuid.uuid4()),
            confirmed_email=True,
            first_name=api_service['name'],
            last_name='API User',
        )
        api_service_user = User.get(api_user_row['uid'])
    else:
        temp_user = anvil.users.signup_with_email(f'{str(uuid.uuid4())}@paylogs.com', api_service_password)
        api_service_user['password_hash'] = temp_user['password_hash']
        temp_user.delete()
    api_service_user.save()

    if api_service['connection_type'] == 'in' or api_service['connection_type'] == 'bidirectional':
        api_credential = AppInApiCredential.search(api_service=api_service, api_user=api_service_user)
        if not api_credential:
            api_credential = AppInApiCredential(
                api_service=api_service,
                api_user=api_service_user,
            )
        api_secret = generate_password()
        cipher = AES.new(api_secret.encode(), AES.MODE_EAX)
        cipher_text, tag = cipher.encrypt_and_digest(
            json.dumps({'api_user': api_service_login, 'password': api_service_password}).encode()
        )
        api_key = base64.urlsafe_b64encode(cipher.nonce + tag + cipher_text).decode()
        api_credential['api_key'] = api_key
        api_credential['api_secret'] = api_secret
        api_credential['tenant_uid'] = tenant_uid
        api_credential['status'] = 'active'
        api_credential.save()
        return api_credential


def decode_api_key(api_key):
    api_credential = AppInApiCredential.search(api_key=api_key)
    if api_credential:
        api_secret = api_credential['api_secret']
        encrypted_bytes = base64.urlsafe_b64decode(api_key)
        nonce = encrypted_bytes[:16]
        tag = encrypted_bytes[16:32]
        ciphertext = encrypted_bytes[32:]
        cipher = AES.new(api_secret.encode(), AES.MODE_EAX, nonce=nonce)
        json_bytes = cipher.decrypt_and_verify(ciphertext, tag)
        json_str = json_bytes.decode('utf-8')
        api_login = json.loads(json_str)
        return api_login['api_user'], api_login['password']


def authenticate_request(request: anvil.server.request):
    tenant_uid = request.headers.get('x-tenant-uid', None)
    api_key = request.headers.get('x-api-key', None)
    if not api_key:
        return False, f'Missing x-api-key header: {request.headers}'
    else:
        api_user, api_password = decode_api_key(api_key)
        if not api_user:
            return False, f'Invalid x-api-key header: {request.headers}'
        else:
            logged_user = fusion_server_utils.init_user_session(user_email=api_user, password=api_password)
            print('logged_user', logged_user)
            if not logged_user:
                return False, f'Invalid user credentials: {api_user}, {api_password}'
            else:
                return True, None
