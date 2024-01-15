from AnvilFusion.server import utils as fusion_server_utils
from ..app.models import Tenant, User, AppIntegration, AppInApiCredential, AppOutApiCredential
import anvil.server
import anvil.users
import anvil.secrets
import base64
import json
import uuid
import secrets
import string
from Crypto.Cipher import AES
from .resources import *

API_REQUEST_USER = 'api_request@oaylogs.com'
API_REQUEST_PASSWORD = anvil.secrets.get_secret('api_request_password')
ACCESS_DENIED_RESPONSE = anvil.server.HttpResponse(401, "Access Denied. Authentication failed.")
API_RESPONSE_PAGE_LENGTH = 100


def generate_password(length=16):
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(length))
    return password


def get_api_service_login(tenant_uid, service_name):
    # tenant = Tenant.get(tenant_uid)
    return f"{service_name}_{tenant_uid}@paylogs.com"


@anvil.server.callable
def register_api_service(name, description, url, connection_type='in'):
    api_service = AppIntegration.get_by('service_name', name)
    if api_service:
        api_service['description'] = description
        api_service['url'] = url
        api_service['connection_type'] = connection_type
        api_service['status'] = 'active'
    else:
        api_service = AppIntegration(
            service_name=name,
            description=description,
            url=url,
            connection_type=connection_type,
            status='active',
        )
    api_service.save()
    return api_service


@anvil.server.callable
def generate_api_key(tenant_uid, api_service: AppIntegration):
    api_service_login = get_api_service_login(tenant_uid, api_service['name'])
    api_service_password = generate_password()
    api_service_user = User.get_by('email', api_service_login)
    if not api_service_user:
        api_user_row = anvil.users.signup_with_email(api_service_login, api_service_password)
        tenant = Tenant.get(tenant_uid)
        api_user_row.update(
            tenant_uid=tenant_uid,
            uid=str(uuid.uuid4()),
            confirmed_email=True,
            first_name=api_service['name'],
            last_name=tenant['name'],
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
    api_credential = AppInApiCredential.get_by('api_key', api_key)
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
        return api_credential['integration']['uid'], api_login['api_user'], api_login['password']


def authenticate_request(request: anvil.server.request):
    tenant_uid = request.headers.get('x-tenant-uid', None)
    api_key = request.headers.get('x-api-key', None)
    if not api_key:
        return None, anvil.server.HttpResponse(401, f'Missing x-api-key header: {request.headers}')
    else:
        print(API_REQUEST_USER, API_REQUEST_PASSWORD)
        logged_user = fusion_server_utils.init_user_session(user_email=API_REQUEST_USER, password=API_REQUEST_PASSWORD)
        integration_uid, api_user, api_password = decode_api_key(api_key)
        if not api_user:
            return None, anvil.server.HttpResponse(401, f'Invalid x-api-key header: {request.headers}')
        else:
            logged_user = fusion_server_utils.init_user_session(user_email=api_user, password=api_password)
            print('logged_user', logged_user)
            if not logged_user:
                return None, anvil.server.HttpResponse(401, f'Invalid user credentials: {api_user}, {api_password}')
            else:
                return integration_uid, None


@anvil.server.http_endpoint("/:resource_name/:resource_uid", methods=["GET", "POST"])
def resource_endpoint(resource_name, resource_uid, **params):
    integration_uid, http_response = authenticate_request(anvil.server.request)
    if integration_uid is None:
        return http_response
    resource_name = resource_name.lower()
    print(f"integration: {integration_uid}\n"
          f"method: {anvil.server.request.method}, headers: {anvil.server.request.headers}\n"
          f"resource_name: {resource_name}, resource_uid: {resource_uid}, params: {params}\n"
          f"body: {anvil.server.request.body_json}\n")

    if resource_name not in API_RESOURCES:
        return anvil.server.HttpResponse(404, f'Invalid resource name: {resource_name}')

    resource = API_RESOURCES[resource_name]

    # HTTP GET request handler
    if anvil.server.request.method == "GET":

        # get single resource object by uid or link_id
        link_id = params.get('link_id', None) if resource['remote_links'] else None
        if resource_uid or link_id:
            item = None
            if resource_uid:
                item = resource['model'].get(resource_uid)
            elif link_id:
                item = resource['model'].get_by('remote_links', {integration_uid: link_id})
            if item:
                return anvil.server.HttpResponse(
                    200,
                    json.dumps(item.to_json_dict(json_schema=resource['json_schema'])),
                    {'content-type': 'application/json'},
                )
            else:
                return anvil.server.HttpResponse(404, f'{resource_name} not found: {resource_uid}')

        # get list of resource objects with supported search, filter, sort, and pagination
        else:
            if resource['pagination']:
                page = params.get('page', 1)
                page_length = params.get('page_length', API_RESPONSE_PAGE_LENGTH)
                try:
                    page = int(page)
                except ValueError:
                    page = 1
                try:
                    page_length = int(page_length)
                except ValueError:
                    page_length = API_RESPONSE_PAGE_LENGTH
            else:
                page = 1
                page_length = None
            filters = resource['filters'](params, integration_uid) if resource.get('filters', None) else {}
            if resource['sorting']:
                filters['search_query'] = resource['sorting']
            print('filters:', filters)
            items = resource['model'].search(page=page, page_length=page_length, **filters)
            item_list = [item.to_json_dict(json_schema=resource['json_schema']) for item in items]
            resource_uri = f'{anvil.server.get_api_origin()}/{resource_name}/?page_length={page_length}'
            links = {
                'first': f'{resource_uri}&page=1',
                'last': f'{resource_uri}&page={items.total_pages}',
            }
            if page > 1:
                links['prev'] = f'{resource_uri}&page={page - 1}'
            if page < items.total_pages:
                links['next'] = f'{resource_uri}&page={page + 1}'
            return anvil.server.HttpResponse(
                200,
                json.dumps({
                    resource_name: item_list,
                    'count': len(item_list),
                    'page': page,
                    'total_pages': items.total_pages,
                    'links': links,
                }),
                {'content-type': 'application/json'},
            )

    # HTTP POST request handler
    elif anvil.server.request.method == "POST":

        # get single resource object by uid or link_id
        link_id = params.get('link_id', None) if resource['remote_links'] else None
        post_data = anvil.server.request.body_json
        if post_data is None:
            try:
                post_data = json.loads(anvil.server.request.body, strict=False)
            except json.JSONDecodeError:
                print(f'Invalid JSON body: {anvil.server.request.body}')
                return anvil.server.HttpResponse(400, f'Invalid JSON body: {anvil.server.request.body}')

        if resource_uid or link_id:
            item = None
            if resource_uid:
                item = resource['model'].get(resource_uid)
            elif link_id:
                item = resource['model'].get_by('remote_links', {integration_uid: link_id})
            if item is None:
                return anvil.server.HttpResponse(404, f'{resource_name} not found: {resource_uid}')
        else:
            item = resource['model']()

        item_data = {}
        for field in resource['json_schema']['fields']:
            if field in post_data:
                item_data[field] = post_data[field]
        for relationship in resource['json_schema'].get('relationships', {}):
            if relationship in post_data:
                rel_json = post_data[relationship]
                if rel_json:
                    if 'uid' in rel_json:
                        item_data[relationship] = {'uid': rel_json['uid']}
                    elif 'link_id' in rel_json:
                        rel_item = resource['model']._relationships[relationship].cls.get_by(
                            'remote_links', {integration_uid: rel_json['link_id']}
                        )
                        if not rel_item:
                            return anvil.server.HttpResponse(
                                404,
                                f'{relationship} not found: {link_id} (remote link)'
                            )
                        item_data[relationship] = {'uid': rel_item['uid']}
        if 'link_id' in post_data and 'remote_links' in resource['model']._attributes:
            if item['remote_links'] is None:
                item_data['remote_links'] = {}
            item_data['remote_links'][integration_uid] = post_data['link_id']
        item.update(item_data)
        item.save()
        item = resource['model'].get(item['uid'])
        return anvil.server.HttpResponse(
            200,
            json.dumps(item.to_json_dict(json_schema=resource['json_schema'])),
            {'content-type': 'application/json'},
        )
