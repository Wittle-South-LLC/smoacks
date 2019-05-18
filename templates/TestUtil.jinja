"""TestUtil.py - Utility methods for test cases"""
import os.path
import logging
import requests
from http import cookiejar

LOGGER = logging.getLogger()

# Set base URL, which will should only vary by port number
BASE_URL = 'http://' + os.environ['TEST_HOST'] + ':' + os.environ['APPSERVER_SPORT'] + '/api/v1'

class AcceptAll(cookiejar.CookiePolicy):
    return_ok = set_ok = domain_return_ok = path_return_ok = lambda self, *args, **kwargs: True
    netscape = True
    rfc2965 = hide_cookie2 = False

def get_new_session():
    """Sets up a new session object that contains a requests session and a saved csrf token"""
    my_session = requests.session()
    my_session.cookies.set_policy(AcceptAll())
    return {
        'session': my_session,
        'csrf_token': None,
        'csrf_refresh_token': None
    }

def log_response_error(resp, log_success=False):
    """Shared method for logging response errors"""
    if resp.status_code >= 400 or log_success:
        LOGGER.debug('Response text = %s', resp.text)

def get_response_with_jwt(test_session, method, url, payload=None, use_refresh_csrf=False):
    """Returns response for desired method with optional payload, adding JWT auth"""
    # If test_session is defined, then use it, otherwise use requests
    req = test_session['session'] if test_session else requests
    args = {}
    if method == 'PUT' or method == 'POST':
        args['json'] = payload
    if test_session and (test_session['csrf_token'] or test_session['csrf_refresh_token']):
        if use_refresh_csrf:
            args['headers'] = {'X-CSRF-TOKEN': test_session['csrf_refresh_token']}
        else:
            args['headers'] = {'X-CSRF-TOKEN': test_session['csrf_token']}
    LOGGER.debug("\nBase URL:\n" + str(BASE_URL))
    LOGGER.debug('args = ' + str(args))
    resp = None
    if method == 'GET':
        resp = req.get(BASE_URL + url, **args)
    elif method == 'PUT':
        resp = req.put(BASE_URL + url, **args)
    elif method == 'POST':
        resp = req.post(BASE_URL + url, **args)
    elif method == 'DELETE':
        resp = req.delete(BASE_URL + url, **args)
    if resp and test_session and 'csrf_access_token' in resp.cookies:
        test_session['csrf_token'] = resp.cookies['csrf_access_token']
    if resp and test_session and 'csrf_refresh_token' in resp.cookies:
        test_session['csrf_refresh_token'] = resp.cookies['csrf_refresh_token']
    return resp
