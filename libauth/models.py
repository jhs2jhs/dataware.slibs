from django.db import models
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseBadRequest
from dwlib import url_keys, request_get, error_response, find_key_by_value

def models_type_callback():
    return models.CharField(max_length=256, null=True)

def models_type_token():
    return models.CharField(max_length=256, null=True)

def models_type_access_scope():
    return models.CharField(max_length=256, null=True)

def models_type_validate_code():
    return models.CharField(max_length=256, null=True)

def models_type_reminder():
    return models.CharField(max_length=256, null=True)

def models_type_request_user_public():
    return models.CharField(max_length=256, null=True)

class REGIST_ROLE(object):
    unclear = 'UNCLEAR'
    resource = 'DATAWARE_RESOURCE'
    catalog = 'DATAWARE_CATALOG'
    client = 'DATAWARE_CLIENT'
    owner_resource = 'DATAWARE_RESOURCE_OWNER'
    owner_catalog = 'DATAWARE_CATALOG_OWNER'
    owner_client = 'DATAWARE_CLIENT_OWNER' # may not be used, just for position

REGIST_ROLE_CHOICES = (
    (0, REGIST_ROLE.unclear),
    (1, REGIST_ROLE.resource),
    (2, REGIST_ROLE.catalog),
    (3, REGIST_ROLE.client),
    (4, REGIST_ROLE.owner_resource),
    (5, REGIST_ROLE.owner_catalog),
    (6, REGIST_ROLE.owner_client),
    )

class REGIST_TYPE(object):
    unclear = 'UNCLEAR'
    catalog_resource = 'CATALOG_RESOURCE'
    client_catalog = 'CLIENT_CATALOG'

REGIST_TYPE_CHOICES = (
    (0, REGIST_TYPE.unclear),
    (1, REGIST_TYPE.catalog_resource),
    (2, REGIST_TYPE.client_catalog),
    )

class REGIST_STATUS(object):
    not_start = 'NOT_START'
    init = 'INIT_REGISTER_REQUEST'
    registrant_request = 'REGISTRANT_REQUEST'
    register_owner_redirect = 'REGISTER_OWNER_REDIRECT'
    register_owner_grant = 'REGISTER_OWNER_GRANT'
    register_grant = 'REGISTER_GRANT'
    registrant_owner_redirect = 'REGISTRANT_OWNER_REDIRECT'
    registrant_owner_grant = 'REGISTRANT_OWNER_GRANT'
    registrant_confirm = 'REGISTRANT_CONFIRM'
    register_activate = 'REGISTER_ACTIVATE' # may not be used, just for position
    finish = 'FINISH'

REGIST_STATUS_CHOICES = (
    (-1, REGIST_STATUS.not_start),
    (0, REGIST_STATUS.init),
    (1, REGIST_STATUS.registrant_request),
    (2, REGIST_STATUS.register_owner_redirect),
    (3, REGIST_STATUS.register_owner_grant),
    (4, REGIST_STATUS.register_grant),
    (5, REGIST_STATUS.registrant_owner_redirect),
    (6, REGIST_STATUS.registrant_owner_grant),
    (7, REGIST_STATUS.registrant_confirm),
    (8, REGIST_STATUS.register_activate),
    (10, REGIST_STATUS.finish),
    )

REQUEST_MEDIA = {
    'desktop_browser': "Desktop_Browser", # key:desc
    'email': "Email",
    }
    
REQUEST_MEDIA_CHOICES = (
    (1, REQUEST_MEDIA['desktop_browser']),
    (2, REQUEST_MEDIA['email']),
    )
    


# registrant: entity who want to register: registrant regist on register
# register: entity who was been register on: registrant regist on register 
class Registration(models.Model):
    regist_type = models.IntegerField(max_length=2, choices=REGIST_TYPE_CHOICES, default=0)
    regist_status = models.IntegerField(max_length=2, choices=REGIST_STATUS_CHOICES, default=-1)
    time_created = models.DateTimeField(auto_now_add=True)
    time_modified = models.DateTimeField(auto_now=True)

    redirect_token = models_type_token()
    user = models.ForeignKey(User, null=True)

    registrant_callback = models_type_callback()
    registrant_request_token = models_type_token()
    registrant_request_scope = models_type_access_scope()

    register_callback = models_type_callback()
    register_request_token = models_type_token()
    register_request_scope = models_type_access_scope()

    registrant_redirect_token = models_type_token()
    register_redirect_token = models_type_token()

    registrant_access_token = models_type_token()
    registrant_access_validate = models_type_validate_code()
    
    register_access_token = models_type_token()
    register_access_validate = models_type_validate_code()

    registrant_request_reminder = models_type_reminder()
    register_request_reminder = models_type_reminder()
    registrant_request_user_public = models_type_request_user_public()
    register_request_user_public = models_type_request_user_public()
    registrant_request_media = models.IntegerField(max_length=2, choices=REQUEST_MEDIA_CHOICES, default=1) # default is desktop_browser
    register_request_media = models.IntegerField(max_length=2, choices=REQUEST_MEDIA_CHOICES, default=1) # default is desktop_browser

    def __unicode__(self):
        return '{Registrant(%s) | Register(%s)}'%(self.registrant_callback, self.register_callback)


class regist_dealer(object):
    def __init__(self, request):
        self.request = request
        self.user = request.user
    def regist_init(self): pass
    def registrant_request(self): pass
    def register_owner_redirect(self): pass
    def register_owner_grant(self): pass
    def register_grant(self): pass
    def registrant_owner_redirect(self): pass
    def registrant_owner_grant(self): pass
    def registrant_confirm(self): pass
    def register_activate(self): pass
    def regist_finish(self): pass


def regist_steps(regist_dealer, request):
    regist_status = request_get(request.REQUEST, url_keys.regist_status)
    if regist_status == None:
        return error_response(1, url_keys.regist_status)
    if regist_status == REGIST_STATUS.init: # may not be necessary
        #@login_required
        return regist_dealer.regist_init()
    if regist_status == REGIST_STATUS.registrant_request:
        return regist_dealer.registrant_request()
    if regist_status == REGIST_STATUS.register_owner_redirect:
        #@login_required
        return regist_dealer.register_owner_redirect()
    if regist_status == REGIST_STATUS.register_owner_grant:
        return regist_dealer.register_owner_grant()
    if regist_status == REGIST_STATUS.register_grant:
        return regist_dealer.register_grant()
    if regist_status == REGIST_STATUS.registrant_owner_redirect:
        return regist_dealer.registrant_owner_redirect()
    if regist_status == REGIST_STATUS.registrant_owner_grant:
        return regist_dealer.registrant_owner_grant()
    if regist_status == REGIST_STATUS.registrant_confirm:
        return regist_dealer.registrant_confirm()
    if regist_status == REGIST_STATUS.register_activate:
        return regist_dealer.register_activate()
    if regist_status == REGIST_STATUS.regist_finish: ## may not be necessary
        return regist_dealer.regist_finish()
    return error_response(2, (url_keys.regist_status, regist_status))


def find_key_by_value_regist_type(regist_type):
    key = find_key_by_value(REGIST_TYPE_CHOICES, regist_type)
    return key

def find_key_by_value_regist_status(regist_status):
    key = find_key_by_value(REGIST_STATUS_CHOICES, regist_status)
    return key

def find_key_by_value_regist_request_media(regist_request_media):
    key = find_key_by_value(REQUEST_MEDIA_CHOICES, regist_request_media)
    if key == None:
        return 1 # the default one is to view by browser
    return key

    
class TOKEN_TYPE(object):
    request = "REQUEST"
    access = "ACCESS"
    redirect = 'REDIRECT'
