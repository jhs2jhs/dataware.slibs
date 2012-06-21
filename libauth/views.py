from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.exceptions import ObjectDoesNotExist
from dwlib import url_keys, request_get, error_response, check_compulsory
from models import *

def hello(request):
    return HttpResponse('hello, libauth')

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
    def regist_finish(self): pass


def regist_steps(regist_dealer, request):
    regist_status = request_get(request.REQUEST, url_keys.regist_status)
    if regist_status == None:
        #return error_response(1, url_keys.regist_status)
        return regist_dealer.regist_init()
    if regist_status == REGIST_STATUS['init']: # may not be necessary
        return regist_dealer.regist_init()
    if regist_status == REGIST_STATUS['registrant_request']:
        return regist_dealer.registrant_request()
    if regist_status == REGIST_STATUS['register_owner_redirect']:
        return regist_dealer.register_owner_redirect()
    if regist_status == REGIST_STATUS['register_owner_grant']:
        return regist_dealer.register_owner_grant()
    if regist_status == REGIST_STATUS['register_grant']:
        return regist_dealer.register_grant()
    if regist_status == REGIST_STATUS['registrant_owner_redirect']:
        return regist_dealer.registrant_owner_redirect()
    if regist_status == REGIST_STATUS['registrant_owner_grant']:
        return regist_dealer.registrant_owner_grant()
    if regist_status == REGIST_STATUS['registrant_confirm']:
        return regist_dealer.registrant_confirm()
    if regist_status == REGIST_STATUS['finish']: ## may not be necessary
        return regist_dealer.regist_finish()
    return error_response(2, (url_keys.regist_status, regist_status))


def get_context_base_regist():
    c = {
        'regist_type':{
            'label': url_keys.regist_type,
            'catalog_resource': REGIST_TYPE['catalog_resource'],
            'client_catalog': REGIST_TYPE['client_catalog'],
            'mutual': REGIST_TYPE['mutual'],
            'one_way': REGIST_TYPE['one_way'],
            },
        'regist_status':{
            'label': url_keys.regist_status,
            'value': '',
            },
        'regist_init_action': {
            'label': url_keys.regist_init_action,
            'request': url_keys.regist_init_action_request,
            'generate': url_keys.regist_init_action_generate,
            },
        'register_callback':{
            'label': url_keys.regist_callback,
            'value': '',
            },
        'registrant_request_scope':{
            'label': url_keys.registrant_request_scope,
            'value': '',
            },
        'registrant_request_reminder': {
            'label': url_keys.registrant_request_reminder,
            'value': '',
            },
        'registrant_request_user_public': {
            'label': url_keys.registrant_request_user_public,
            'value': '',
            },
        }
    return c

##### method to call for each regist_steps

@login_required
def method_regist_init(request):
    user = request.user # user has to login, so that it would reduce the man-in-the middle attack
    #registrant_init_action = request_get(request.REQUEST, url_keys.registrant_init_action)
    #register_callback = request_get(request.REQUEST, url_keys.regist_callback)
    #regist_type = request_get(request.REQUEST, url_keys.regist_type)
    #registrant_request_scope = request_get(request.REQUEST, url_keys.registrant_request_scope)
    #registrant_request_reminder = request_get(request.REQUEST, url_keys.registrant_request_reminder)
    #registrant_request_user_public = request_get(request.REQUEST, url_keys.registrant_request_user_public)
    #if (check_compulsory()) == True:
    #    return error_response(5, ())
    register_callback = 'http://localhost:8001/resource/regist'
    registrant_request_scope = "{'action':'read, write', 'content':'blog, status'}" # to be confirmed
    registrant_request_reminder = ''
    registrant_request_user_public = ''
    c = get_context_base_regist()
    c['register_callback']['value'] = register_callback
    c['regist_status']['value'] = REGIST_STATUS['registrant_request']
    c['registrant_request_reminder']['value'] = registrant_request_reminder
    c['registrant_request_scope']['value'] = registrant_request_scope
    c['registrant_request_user_public']['value'] = registrant_request_user_public
    print c
    context = RequestContext(request, c)
    return render_to_response('regist_init.html', context)
