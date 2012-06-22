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

def dict_to_choices(d):
    choices = []
    i = 1
    for k, v in d.iteritems():
        choice = (i, v)
        choices.append(choice)
        i = i + 1
    return choices

# not used at moment
REGIST_ROLE = {
    'unclear':'UNCLEAR',
    'resource':'DATAWARE_RESOURCE',
    'catalog':'DATAWARE_CATALOG',
    'client':'DATAWARE_CLIENT',
    'owner_resource':'DATAWARE_RESOURCE_OWNER',
    'owner_catalog':'DATAWARE_CATALOG_OWNER',
    'owner_client':'DATAWARE_CLIENT_OWNER', # may not be used, just for position
}
REGIST_ROLE_CHOICES = dict_to_choices(REGIST_ROLE)

REGIST_TYPE = {
    'unclear':'UNCLEAR',
    'catalog_resource':'CATALOG_RESOURCE',
    'client_catalog':'CLIENT_CATALOG',
    'mutual':'MUTUAL',
    'one_way':'ONE_WAY',
    }
REGIST_TYPE_CHOICES = dict_to_choices(REGIST_TYPE)

REGIST_STATUS = {
    'not_start':'NOT_START',
    'init':'INIT',
    'registrant_request':'REGISTRANT_REQUEST',
    'register_owner_redirect':'REGISTER_OWNER_REDIRECT',
    'register_owner_grant':'REGISTER_OWNER_GRANT',
    'register_grant':'REGISTER_GRANT',
    'registrant_owner_redirect':'REGISTRANT_OWNER_REDIRECT',
    'registrant_owner_grant':'REGISTRANT_OWNER_GRANT',
    'registrant_confirm':'REGISTRANT_CONFIRM',
    'finish':'FINISH',
    }
REGIST_STATUS_CHOICES = dict_to_choices(REGIST_STATUS)

REQUEST_MEDIA = {
    'desktop_browser': "Desktop_Browser", # key:desc
    'email': "Email",
    }
    
REQUEST_MEDIA_CHOICES = dict_to_choices(REQUEST_MEDIA)

TOKEN_TYPE = {
    'request':"REQUEST",
    'access':"ACCESS",
    'redirect':'REDIRECT',
    'grant':'GRANT',
    }
    

# registrant: entity who want to register: registrant regist on register
# register: entity who was been register on: registrant regist on register 
class Registration(models.Model):
    regist_type = models.IntegerField(max_length=2, choices=REGIST_TYPE_CHOICES, default=0) # all default is 0, 0 mean not set
    regist_status = models.IntegerField(max_length=2, choices=REGIST_STATUS_CHOICES, default=0)
    time_created = models.DateTimeField(auto_now_add=True)
    time_modified = models.DateTimeField(auto_now=True)

    redirect_token = models_type_token()
    user = models.ForeignKey(User, null=True)

    registrant_callback = models_type_callback()
    registrant_request_token = models_type_token()
    registrant_request_scope = models_type_access_scope()
    registrant_request_reminder = models_type_reminder()
    registrant_request_user_public = models_type_request_user_public() # leave it as interface
    registrant_redirect_token = models_type_token()
    registrant_grant_user_token = models_type_token()
    registrant_access_token = models_type_token()
    registrant_access_validate = models_type_validate_code()

    register_callback = models_type_callback()
    register_request_token = models_type_token()
    register_request_scope = models_type_access_scope()
    register_request_reminder = models_type_reminder()
    register_request_user_public = models_type_request_user_public() # not used at moment
    register_redirect_token = models_type_token()
    register_grant_user_token = models_type_token()
    register_access_token = models_type_token()
    register_access_validate = models_type_validate_code()

    registrant_request_media = models.IntegerField(max_length=2, choices=REQUEST_MEDIA_CHOICES, default=0)
    register_request_media = models.IntegerField(max_length=2, choices=REQUEST_MEDIA_CHOICES, default=0) 

    def __unicode__(self):
        return '{Registrant(%s) | Register(%s)}'%(self.registrant_callback, self.register_callback)


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

