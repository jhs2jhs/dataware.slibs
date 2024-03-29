from models import *

def get_context_base_regist():
    c = {
        'regist_callback':{
            'label': url_keys.regist_callback,
            'value': '',
            },
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
        'regist_status_current':{
            'label':url_keys.regist_status_current,
            'value':'',
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
            'confirm': url_keys.regist_redirect_action_confirm,
            },
        'regist_grant_user_token':{
            'label': url_keys.regist_grant_user_token,
            'value':'',
            },
         'regist_request_scope': {
            'label': url_keys.regist_request_scope,
            'value': '',
            },
        'regist_request_token': {
            'label': url_keys.regist_request_token,
            'value': '',
            },
        'regist_request_reminder': {
            'label': url_keys.regist_request_reminder,
            'value': '',
            },
        'regist_request_user_public': {
            'label': url_keys.regist_request_user_public,
            'value': '',
            },
        'regist_redirect_token':{
            'label':url_keys.regist_redirect_token,
            'value': '',
            },
        'register_callback':{
            'label': url_keys.regist_callback,
            'value': '',
            },
        'register_access_token': {
            'label': url_keys.register_access_token,
            'value': '',
            },
        'register_access_validate': {
            'label': url_keys.register_access_validate,
            'value': '',
            },
        'register_request_scope': {
            'label': url_keys.register_request_scope,
            'value': '',
            },
        'register_request_token': {
            'label': url_keys.register_request_token,
            'value': '',
            },
        "register_redirect_token":{
            'label': url_keys.register_redirect_token,
            'value': '',
            },
        'register_request_reminder': {
            'label': url_keys.register_request_reminder,
            'value': '',
            },
        'register_request_user_public': {
            'label': url_keys.register_request_user_public,
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
        'registrant_callback': {
            'label': url_keys.registrant_callback,
            'value': '',
            },
        'registrant_request_token': {
            'label': url_keys.registrant_request_token,
            'value':'',
            },
        "registrant_redirect_token":{
            'label': url_keys.registrant_redirect_token,
            'value': '',
            },
        'registrant_access_token': {
            'label': url_keys.registrant_access_token,
            'value': '',
            },
        'registrant_access_validate': {
            'label': url_keys.registrant_access_validate,
            'value': '',
            },
        }
    return c
