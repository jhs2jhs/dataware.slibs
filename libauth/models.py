from django.db import models
from django.contrib.auth.models import User

def models_type_callback():
    return models.CharField(max_length=256, null=True)

def models_type_token():
    return models.CharField(max_length=256, null=True)

def models_type_access_scope():
    return models.CharField(max_length=256, null=True)

def models_type_validate_code():
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
    register_confirm = 'REGISTER_CONFIRM'
    registrant_owner_redirect = 'REGISTRANT_OWNER_REDIRECT'
    registrant_owner_grant = 'REGISTRANT_OWNER_GRANT'
    registrant_confirm = 'REGISTRANT_CONFIRM'
    register_confirm = 'REGISTER_COFNIRM' # may not be used, just for position
    finish = 'FINISH'

REGIST_STATUS_CHOICES = (
    (-1, REGIST_STATUS.not_start),
    (0, REGIST_STATUS.init),
    (1, REGIST_STATUS.registrant_request),
    (2, REGIST_STATUS.register_owner_redirect),
    (3, REGIST_STATUS.register_owner_grant),
    (4, REGIST_STATUS.register_auth),
    (5, REGIST_STATUS.registrant_owner_redirect),
    (6, REGIST_STATUS.registrant_owner_grant)
    (7, REGIST_STATUS.registrant_confirm),
    (8, REGIST_STATUS.register_confirm),
    (10, REGIST_STATUS.finish),
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

    registrant_access_token = models_type_token()
    registrant_access_validate = models_type_validate_code()
    
    register_access_token = models_type_token()
    register_access_validate = models_type_validate_code()

    def __unicode__(self):
        return '{Registrant(%s) | Register(%s)}'%(self.registrant_callback, self.register_callback)


    

    
