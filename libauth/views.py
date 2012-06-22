from models import *
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.exceptions import ObjectDoesNotExist
from dwlib import url_keys, request_get, error_response, check_compulsory, check_choice
import dwlib

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
        'regist_redirect_url': {
            'label': url_keys.regist_redirect_url,
            'value': '',
            },
        'regist_request_action': {
            'label': url_keys.regist_request_action,
            'request': url_keys.regist_request_action_request,
            },
        'regist_redirect_action':{
            'label': url_keys.regist_redirect_action,
            'login_redirect': url_keys.regist_redirect_action_login_redirect,
            'redirect': url_keys.regist_redirect_action_redirect,
            'grant': url_keys.regist_redirect_action_grant,
            'modify_scope': url_keys.regist_redirect_action_modify_scope,
            'wrong_user': url_keys.regist_redirect_action_wrong_user, # I remember it is not wrong user, should be worng reminder, etc??
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
        "register_redirect_token":{
            'label': url_keys.register_redirect_token,
            'value': '',
            },
        }
    return c

##### method to call for each regist_steps
####
@login_required
def method_regist_init(request):
    register_callback = 'http://localhost:8001/resource/regist'
    registrant_request_scope = "{'action':'read, write', 'content':'blog, status'}" # to be confirmed
    registrant_request_reminder = ''
    registrant_request_user_public = ''
    ##
    c = get_context_base_regist()
    c['regist_status']['value'] = REGIST_STATUS['registrant_request']
    c['register_callback']['value'] = register_callback
    c['registrant_request_reminder']['value'] = registrant_request_reminder
    c['registrant_request_scope']['value'] = registrant_request_scope
    c['registrant_request_user_public']['value'] = registrant_request_user_public
    print c
    context = RequestContext(request, c)
    return render_to_response('regist_init.html', context)

####
@login_required
def method_registrant_request(request, regist_callback_me):
    user = request.user # user has to login, so that it would reduce the man-in-the middle attack
    register_callback = request_get(request.REQUEST, url_keys.regist_callback)
    regist_type = request_get(request.REQUEST, url_keys.regist_type)
    registrant_request_scope = request_get(request.REQUEST, url_keys.registrant_request_scope)
    registrant_request_reminder = request_get(request.REQUEST, url_keys.registrant_request_reminder)
    registrant_request_user_public = request_get(request.REQUEST, url_keys.registrant_request_user_public) # it is not compuslary at monent
    print register_callback, regist_type, registrant_request_scope, registrant_request_reminder, registrant_request_user_public
    if (check_compulsory((register_callback, regist_type, registrant_request_scope, registrant_request_reminder))) == False:
        return error_response(5, ())
    if (check_choice(REGIST_TYPE, regist_type)) == False:
        return error_response(2, (url_keys.regist_type, regist_type))
    ##
    registrant_request_token = dwlib.token_create_user(register_callback, regist_callback_me, TOKEN_TYPE['request'], user) # should I user.id or just user here?
    ##
    params = {
        url_keys.regist_status: REGIST_STATUS['register_owner_redirect'], #
        url_keys.regist_type: regist_type,
        url_keys.regist_callback: regist_callback_me,
        url_keys.registrant_request_token: registrant_request_token,
        url_keys.registrant_request_scope: registrant_request_scope,
        url_keys.registrant_request_reminder: registrant_request_reminder,
        url_keys.registrant_request_user_public: registrant_request_user_public,
        }
    url_params = dwlib.urlencode(params)
    url = '%s?%s'%(register_callback, url_params) # attack: if one takes a correct user session, will it keep request here to explore the database? whether it should set up the protection to protect the register speed?
    ##
    regist_type_key = find_key_by_value_regist_type(regist_type) ##what happened if not correct here?
    regist_status_key = find_key_by_value_regist_status(REGIST_STATUS['registrant_request']) 
    obj, created = Registration.objects.get_or_create(
        regist_type=regist_type_key, 
        regist_status=regist_status_key, 
        registrant_request_token=registrant_request_token, 
        registrant_request_scope=registrant_request_scope, 
        registrant_callback=regist_callback_me, 
        register_callback=register_callback, 
        registrant_request_reminder=registrant_request_reminder, 
        registrant_request_user_public=registrant_request_user_public,
        user=user)
    ##
    c = get_context_base_regist()
    c['regist_redirect_url']['value'] = url
    c['regist_status']['value'] = REGIST_STATUS['register_owner_redirect'] # do I need to pass it in?
    context = RequestContext(request, c)
    return render_to_response('registrant_request.html', context)

####
def method_register_owner_redirect(request, regist_callback_me):
    # check whether user has login in or not
    registrant_callback = request_get(request.REQUEST, url_keys.regist_callback)
    regist_type = request_get(request.REQUEST, url_keys.regist_type)
    registrant_request_token = request_get(request.REQUEST, url_keys.registrant_request_token)
    registrant_request_scope = request_get(request.REQUEST, url_keys.registrant_request_scope) # may check it is in scope or not
    registrant_request_reminder = request_get(request.REQUEST, url_keys.registrant_request_reminder)
    registrant_request_user_public = request_get(request.REQUEST, url_keys.registrant_request_user_public) # may not be compulsory
    #print register_callback, regist_type, registrant_request_scope, registrant_request_reminder, registrant_request_user_public
    if (check_compulsory((registrant_callback, regist_type, registrant_request_token, registrant_request_scope, registrant_request_reminder))) == False:
        return error_response(5, ())
    if (check_choice(REGIST_TYPE, regist_type)) == False:
        return error_response(2, (url_keys.regist_type, regist_type))
    ##
    register_redirect_token = dwlib.token_create(registrant_callback, regist_callback_me, TOKEN_TYPE['redirect'])
    ##
    regist_type_key = find_key_by_value_regist_type(regist_type)
    regist_status_key = find_key_by_value_regist_status(REGIST_STATUS['register_owner_redirect'])
    obj, created = Registration.objects.get_or_create(
        regist_type=regist_type_key, 
        regist_status=regist_status_key, 
        registrant_request_token=registrant_request_token, 
        registrant_request_scope=registrant_request_scope, 
        registrant_callback=registrant_callback, 
        register_callback=regist_callback_me, 
        registrant_request_reminder=registrant_request_reminder, 
        registrant_request_user_public=registrant_request_user_public,
        register_redirect_token=register_redirect_token)
    ##
    params = {
        url_keys.regist_status: REGIST_STATUS['register_owner_grant'],
        url_keys.regist_type: regist_type,
        url_keys.register_redirect_token:register_redirect_token,
        }
    url_params = dwlib.urlencode(params)
    url = '%s?%s'%(regist_callback_me, url_params)
    ##
    c = get_context_base_regist()
    c['register_redirect_token']['value'] = register_redirect_token
    c['regist_redirect_url']['value'] = url
    c['regist_status']['value'] = REGIST_STATUS['register_owner_grant'] # do I need to pass it in?
    context = RequestContext(request, c)
    return render_to_response("regist_owner_redirect.html", context)


####
def method_register_owner_grant(request, regist_callback_me):
    print request.REQUEST
    return HttpResponse("hello grant")
