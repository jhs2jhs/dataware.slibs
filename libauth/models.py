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

REGISTRATION_STATUS_CHOICES = (
    (-1, 'NOT YET'),
    (0, 'INIT'),
    (1, 'REQUEST'),
    (2, 'REDIRECT'),
    (3, 'GRANT'),
    (4, 'AUTH'),
    (5, 'CONFIRM'),
    (10, 'FINISH'),
    )

class CatalogResourceRegistration(models.Model):
    registration_status = models.IntegerField(max_length=1, choices=REGISTRATION_STATUS_CHOICES, default=-1)
    time_created = models.DateTimeField(auto_now_add=True)
    time_modified = models.DateTimeField(auto_now=True)

    redirect_token = models_type_token()
    user = models.ForeignKey(User, null=True)

    resource_callback = models_type_callback()
    resource_request_token = models_type_token()
    resource_access_scope = models_type_access_scope()

    catalog_callback = models_type_callback()
    catalog_request_token = models_type_token()
    catalog_access_scope = models_type_access_scope()

    resource_access_token = models_type_token()
    resource_validate_code = models_type_validate_code()
    
    catalog_access_token = models_type_token()
    catalog_validate_code = models_type_validate_code()

    def __unicode__(self):
        return self.catalog_callback

    
