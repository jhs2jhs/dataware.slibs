from models import *
from options import get_context_base_regist
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
    c['regist_type']['value'] = regist_type
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
    c['regist_redirect_token']['value'] = register_redirect_token
    c['regist_redirect_url']['value'] = url
    c['regist_status']['value'] = REGIST_STATUS['register_owner_grant'] # do I need to pass it in?
    c['regist_type']['value'] = regist_type
    context = RequestContext(request, c)
    return render_to_response("regist_owner_redirect.html", context)


####
@login_required
def method_register_owner_grant(request, regist_callback_me):
    user = request.user
    regist_type = request_get(request.REQUEST, url_keys.regist_type)
    register_redirect_token = request_get(request.REQUEST, url_keys.register_redirect_token)
    if (check_compulsory((regist_type, register_redirect_token))) == False:
        return error_response(5, ())
    if (check_choice(REGIST_TYPE, regist_type)) == False:
        return error_response(2, (url_keys.regist_type, regist_type))
    ##
    try:
        registration = Registration.objects.get(register_redirect_token=register_redirect_token)
    except ObjectDoesNotExist:
        return error_response(3, (url_keys.register_redirect_token, register_redirect_token))
    regist_status_key = find_key_by_value_regist_status(REGIST_STATUS['register_owner_grant'])
    registration.regist_status = regist_status_key
    registration.user = user
    registration.save()
    ##
    register_grant_user_token = dwlib.token_create_user(registration.registrant_callback, regist_callback_me, TOKEN_TYPE['grant'], user)
    registration.register_grant_user_token = register_grant_user_token
    registration.save()
    ##
    params = {
        url_keys.regist_status: REGIST_STATUS['register_grant'],
        url_keys.regist_type: regist_type,
        url_keys.register_redirect_token:register_redirect_token,
        url_keys.regist_grant_user_token: register_grant_user_token,
        }
    url_params = dwlib.urlencode(params)
    url = '%s?%s'%(regist_callback_me, url_params)
    ##
    c = get_context_base_regist()
    c['regist_callback']['value'] = registration.registrant_callback
    c['regist_request_token']['value'] = registration.registrant_request_token
    c['regist_request_scope']['value'] = registration.registrant_request_scope
    c['regist_request_reminder']['value'] = registration.registrant_request_reminder
    c['regist_request_user_public']['value'] = registration.registrant_request_user_public
    c['regist_status']['value'] = REGIST_STATUS['register_grant']
    c['register_redirect_token']['value'] = register_redirect_token
    c['regist_grant_user_token']['value'] = register_grant_user_token
    c['regist_redirect_url']['value'] = url
    c['regist_type']['value'] = regist_type
    context = RequestContext(request, c)
    return render_to_response("regist_owner_grant.html", context)


####
@login_required
def method_register_grant(request, regist_callback_me):
    #print request.REQUEST
    user = request.user
    register_redirect_token = request_get(request.REQUEST, url_keys.register_redirect_token)
    register_grant_user_token = request_get(request.REQUEST, url_keys.regist_grant_user_token)
    regist_type = request_get(request.REQUEST, url_keys.regist_type)
    if (check_compulsory((regist_type, register_redirect_token, register_grant_user_token))) == False:
        return error_response(5, ())
    if (check_choice(REGIST_TYPE, regist_type)) == False:
        return error_response(2, (url_keys.regist_type, regist_type))
    ##
    try:
        registration = Registration.objects.get(register_redirect_token=register_redirect_token, register_grant_user_token=register_grant_user_token)
    except ObjectDoesNotExist:
        return error_response(5, ())
    if registration.user != user:
        return error_response(6, ())
    regist_status_key = find_key_by_value_regist_status(REGIST_STATUS['register_grant'])
    registration.regist_status = regist_status_key
    registration.save()
    ##
    register_access_token = dwlib.token_create_user(registration.registrant_callback, regist_callback_me, TOKEN_TYPE['access'], user)
    register_access_validate = registration.registrant_request_scope #TODO need to expand here, enable to edit here
    register_request_token = dwlib.token_create_user(registration.registrant_callback, regist_callback_me, TOKEN_TYPE['request'], user)
    register_request_scope = '' # need to dyanmic generated here, for example using javascript
    register_request_reminder = registration.registrant_request_reminder ## may need to be changed
    register_request_user_public = registration.registrant_request_user_public
    registration.register_access_token = register_access_token
    registration.register_access_validate = register_access_validate
    registration.register_request_token = register_request_token
    registration.register_request_scope = register_request_scope
    registration.save()
    ##
    params = {
        url_keys.regist_status: REGIST_STATUS['registrant_owner_redirect'], #if mutual, it can come to register,etc???
        url_keys.regist_type: regist_type,
        url_keys.regist_callback: regist_callback_me,
        url_keys.register_access_token:register_access_token,
        url_keys.register_access_validate: register_access_validate,
        url_keys.register_request_token: register_request_token,
        url_keys.register_request_scope: register_request_scope,
        url_keys.register_request_reminder: url_keys.register_request_reminder,
        url_keys.register_request_user_public: url_keys.register_request_user_public,
        url_keys.registrant_request_token: registration.registrant_request_token,
        }
    url_params = dwlib.urlencode(params)
    url = '%s?%s'%(registration.registrant_callback, url_params)
    print url
    ##
    c = get_context_base_regist()
    c['registrant_callback']['value'] = registration.registrant_callback
    c['registrant_request_token']['value'] = registration.registrant_request_token
    c['registrant_request_scope']['value'] = registration.registrant_request_scope
    c['registrant_request_reminder']['value'] = registration.registrant_request_reminder
    c['registrant_request_user_public']['value'] = registration.registrant_request_user_public
    c['register_access_token']['value'] = register_access_token
    c['register_access_validate']['value'] = register_access_validate
    c['register_request_token']['value'] = register_request_token
    c['register_request_scope']['value'] = register_request_token
    c['register_request_reminder']['value'] = register_request_reminder
    c['register_request_user_public']['value'] = register_request_user_public
    c['regist_status']['value'] = REGIST_STATUS['registrant_owner_redirect']
    c['regist_redirect_url']['value'] = url
    c['regist_type']['value'] = regist_type
    context = RequestContext(request, c)
    return render_to_response("regist_grant.html", context) #TODO how user can change their scope, and reminder, and user public information here. 


####
@login_required
def method_registrant_owner_redirect(request, regist_callback_me):
    user = request.user
    regist_type = request_get(request.REQUEST, url_keys.regist_type)
    registrant_request_token = request_get(request.REQUEST, url_keys.registrant_request_token)
    register_access_token = request_get(request.REQUEST, url_keys.register_access_token)
    register_access_validate = request_get(request.REQUEST, url_keys.register_access_validate)
    if (check_compulsory((regist_type, registrant_request_token, register_access_token, register_access_validate))) == False:
        return error_response(5, ())
    if (check_choice(REGIST_TYPE, regist_type)) == False:
        return error_response(2, (url_keys.regist_type, regist_type))
    try:
        registration = Registration.objects.get(registrant_request_token=registrant_request_token)
    except ObjectDoesNotExist:
        return error_response(3, (url_keys.registrant_request_token, registrant_request_token))
    if registration.user != user:
        return error_response(6, ())
    ## 
    register_request_token = request_get(request.REQUEST, url_keys.register_request_token)
    register_request_scope = request_get(request.REQUEST, url_keys.register_request_scope)
    register_request_reminder = request_get(request.REQUEST, url_keys.register_request_reminder)
    register_request_user_public = request_get(request.REQUEST, url_keys.register_request_user_public)
    ##
    registrant_redirect_token = dwlib.token_create(registration.registrant_callback, regist_callback_me, TOKEN_TYPE['redirect'])
    ##
    regist_type_key = find_key_by_value_regist_type(regist_type)
    regist_status_key = find_key_by_value_regist_status(REGIST_STATUS['registrant_owner_redirect'])
    registration.regist_status=regist_status_key
    registration.register_access_token = register_access_token
    registration.register_access_validate = register_access_validate
    registration.register_request_token = register_request_token
    registration.register_request_scope = register_request_scope
    registration.register_request_reminder = register_request_reminder
    registration.register_request_user_public = register_request_user_public ## look like it not need here
    registration.registrant_redirect_token = registrant_redirect_token
    registration.save()
    ##
    params = {
        url_keys.regist_status: REGIST_STATUS['registrant_owner_grant'],
        url_keys.regist_type: regist_type,
        url_keys.register_redirect_token:registrant_redirect_token,
        }
    url_params = dwlib.urlencode(params)
    url = '%s?%s'%(regist_callback_me, url_params)
    ##
    c = get_context_base_regist()
    c['regist_redirect_token']['value'] = registrant_redirect_token
    c['regist_redirect_url']['value'] = url
    c['regist_status']['value'] = REGIST_STATUS['registrant_owner_grant'] # do I need to pass it in?
    c['regist_type']['value'] = regist_type
    context = RequestContext(request, c)
    print c
    return render_to_response("regist_owner_redirect.html", context)
   

####
@login_required
def method_registrant_owner_grant(request, regist_callback_me):
    user = request.user
    regist_type = request_get(request.REQUEST, url_keys.regist_type)
    registrant_redirect_token = request_get(request.REQUEST, url_keys.regist_redirect_token)
    if (check_compulsory((regist_type, registrant_redirect_token))) == False:
        return error_response(5, ())
    if (check_choice(REGIST_TYPE, regist_type)) == False:
        return error_response(2, (url_keys.regist_type, regist_type))
    ##
    try:
        registration = Registration.objects.get(registrant_redirect_token=registrant_redirect_token)
    except ObjectDoesNotExist:
        return error_response(3, (url_keys.register_redirect_token, register_redirect_token))
    if registration.user != user:
        return error_response(6, ())
    regist_status_key = find_key_by_value_regist_status(REGIST_STATUS['registrant_owner_grant'])
    registration.regist_status = regist_status_key
    registration.save()
    ##
    registrant_grant_user_token = dwlib.token_create_user(registration.register_callback, regist_callback_me, TOKEN_TYPE['grant'], user)
    registration.registrant_grant_user_token = registrant_grant_user_token
    registration.save()
    ##
    params = {
        url_keys.regist_status: REGIST_STATUS['registrant_confirm'],
        url_keys.regist_type: regist_type,
        url_keys.registrant_redirect_token:registrant_redirect_token,
        url_keys.regist_grant_user_token: registrant_grant_user_token,
        }
    url_params = dwlib.urlencode(params)
    url = '%s?%s'%(regist_callback_me, url_params)
    ##
    c = get_context_base_regist()
    c['regist_callback']['value'] = registration.register_callback
    c['regist_request_token']['value'] = registration.register_request_token
    c['regist_request_scope']['value'] = registration.register_request_scope
    c['regist_request_reminder']['value'] = registration.register_request_reminder
    c['regist_request_user_public']['value'] = registration.register_request_user_public
    c['regist_status']['value'] = REGIST_STATUS['registrant_confirm']
    c['registrant_redirect_token']['value'] = registrant_redirect_token
    c['regist_grant_user_token']['value'] = registrant_grant_user_token
    c['regist_redirect_url']['value'] = url
    c['regist_type']['value'] = regist_type
    context = RequestContext(request, c)
    return render_to_response("regist_owner_grant.html", context)

####
@login_required
def method_registrant_confirm(request, regist_callback_me):
    return HttpResponse('hello confirm')
    
    
    
