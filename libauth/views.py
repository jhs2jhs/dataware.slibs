from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from dwlib import url_keys, request_get, error_response
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

