import urllib
import hashlib
from datetime import datetime
from django.db import models

class url_keys(object):
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

