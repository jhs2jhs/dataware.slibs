import urllib
import hashlib
from datetime import datetime

class url_keys(object):
    # registration between catalog and resource
    # 1. REQUEST
    catalog_callback = 'catalog_callback'
    catalog_temp_id = 'catalog_temp_id'
    access_scope_action = 'access_scope_action'
    access_scope_content = 'access_scope_content'
    # 2. REDIRECT
    request_temp = 'request_temp'

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

def token_create(other_url, other_callback):# may need to add user as a unique party
    param = {'start':str(datetime.now())}
    url_param = urlencode(param)
    key = '%s/%s?%s'%(other_url, other_callback, param)
    token = signature_create(key)
    return token

