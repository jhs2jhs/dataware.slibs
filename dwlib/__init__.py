import urllib
import hashlib
from datetime import datetime
from django.db import models
from django.http import HttpResponse, HttpResponseBadRequest

class url_keys(object):
    # for each regist
    regist_status = 'REGIST_STATUS'
    regist_type = 'REGIST_TYPE'
    regist_callback = 'REGIST_CALLBACK'
    registrant_init_action = "REGISTRANT_INIT_ACTION"
    registrant_init_action_generate = "Generate"
    registrant_init_action_request = "Request"
    regist_redirect_url = "regist_redirect_url"
    regist_redirect_action = 'regist_redirect_action'
    regist_redirect_action_redirect = 'Redirect'
    regist_redirect_action_login_redirect = 'Login&Redirect'
    register_callback = 'REGISTER_CALLBACK'
    registrant_callback = 'REGISTRANT_CALLBACK'
    register_request_reminder = "REGISTER_REMINDER"
    registrant_request_reminder = "REGISTRANT_REMINDER"
    register_request_user_public = "REGISTER_USER_PUBLIC"
    registrant_request_user_public = "REGISTRANT_USER_PUBLIC"
    register_request_media = "REGISTER_REQUEST_MEDIA"
    registrant_request_media = "REGISTRANT_REQUEST_MEDIA"
    registrant_request_token = 'REGISTRANT_REQUEST_TOKEN'
    registrant_request_scope = 'REGISTRANT_REQUEST_SCOPE'
    registrant_redirect_token = 'REGISTRANT_REDIRECT_TOKEN'
    registrant_user_token = 'REGISTRANT_USER_TOKEN'
    registrant_access_token = 'REGISTRANT_ACCESS_TOKEN'
    registrant_validation = 'REGISTRANT_VALIDATION'
    register_request_token = 'REGISTER_REQUEST_TOKEN'
    register_request_scope = 'REGISTER_REQUEST_SCOPE'
    register_redirect_token = 'REGISTRANT_REDIRECT_TOKEN'    
    register_user_token = 'REGISTER_USER_TOKEN'
    register_access_token = 'REGISTER_ACCESS_TOKEN'
    register_validation = 'REGISTER_VALIDATION'    
    # registration between catalog and resource
    # 1. REQUEST
    catalog_callback = 'catalog_callback'
    catalog_request_token = 'catalog_request_token'
    catalog_access_scope = 'catalog_access_scope'
    # 2. REDIRECT
    redirect_token = 'redirect_token'
    # 3. GRANT
    user_id = 'user_id'
    grant_action = 'grant_action'
    grant_action_allow = 'allow'
    grant_action_decline = 'decline'
    # 4. AUTH
    resource_access_token = 'resource_access_token'
    resource_request_token = 'resource_request_token'
    resource_validate_code = 'resource_validate_code'
    resource_callback = 'resource_callback'
    resource_access_scope = 'resource_access_scope'
    # 5 CONFIRM
    catalog_access_token = 'catalog_access_token'
    catalog_validate_code = 'catalog_validate_code'
    


class form_label(object):
    regist_type = 'regist_type'
    register_callback = 'register_callback'
    # OWNER_REQUEST
    owner_request_callback = 'Catalog callback'
    owner_request_token = 'Catalog request token'
    owner_request_scope = 'Catalog registration scope'
    owner_request_action_allow = 'Allow'
    owner_request_action_decline = 'Decline'


def urlencode(url_dict):
    url_params = urllib.urlencode(url_dict)
    return url_params

# many library can be used to generate signature. 
# oauth suggested hmac-sha256 in draft 00, but not be found in other draft version. 
# in python, hashlib, hmac, base64, all can be use for hash generation. I choose hashlib here, as it is a comon interface to many different secure hash algorithm. 
# http://docs.python.org/library/hashlib.html#module-hashlib
def signature_create(key):
    m = hashlib.sha512()
    m.update(key)
    return m.hexdigest()

def token_create(other_callback):# may need to add user as a unique party
    param = {'start':str(datetime.now())}
    url_param = urlencode(param)
    key = '%s?%s'%(other_callback, param)
    token = signature_create(key)
    return token

def token_create_user(other_callback, user_id):
    param = {'start':str(datetime.now()), 'user_id':user_id}
    url_param = urlencode(param)
    key = '%s?%s'%(other_callback, param)
    token = signature_create(key)
    return token

def request_get(param, key):
    return param.get(key, None)

def request_params_get(params):
    request_params = {
        url_keys.regist_status: request_get(params, url_keys.regist_status),
        url_keys.regist_type: request_get(params, url_keys.regist_type),
        url_keys.regist_callback: request_get(params, url_keys.regist_callback),
        url_keys.registrant_request_token: request_get(params, url_keys.registrant_request_token),
        url_keys.registrant_request_scope: request_get(params, url_keys.registrant_request_scope),
        url_keys.registrant_redirect_token: request_get(params, url_keys.registrant_redirect_token),
        url_keys.registrant_user_token: request_get(params, url_keys.registrant_user_token),
        url_keys.registrant_access_token:request_get(params, url_keys.registrant_access_token),
        url_keys.registrant_validation: request_get(params, url_keys.registrant_validation),
        url_keys.register_request_token: request_get(params, url_keys.register_request_token),
        url_keys.register_request_scope: request_get(params, url_keys.register_request_scope),
        url_keys.register_redirect_token: request_get(params, url_keys.register_redirect_token),
        url_keys.register_user_token: request_get(params, url_keys.register_user_token),
        url_keys.register_access_token: request_get(params, url_keys.register_access_token),
        url_keys.register_validation: request_get(params, url_keys.register_validation)
        }
    return request_params

def error_response(type, params):
    if type == 1:
        return HttpResponseBadRequest('%s is not found in http request'%params)
    if type == 2:
        return HttpResponseBadRequest('%s is found but incorrect (%s) in http request'%params)

def find_key_by_value(tuples, value):
    key = [k for (k, v) in tuples if v == value]
    if len(key) == 0:
        return None
    else:
        return key[0]


