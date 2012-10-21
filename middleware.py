from webob import Request
from webob.exc import HTTPTemporaryRedirect, HTTPUnauthorized
from urlparse import urlparse
from sliclient import SLIClient

CLIENT_SESSION_ID = "oauth.client"

class OAuthMiddleware(object):
    "Example middleware that appends a message to all 200 html responses"    

    def __init__(self, app, client_id, client_secret, api_url, callback_url):
        self.app = app
        self.client_id = client_id
        self.client_secret = client_secret
        self.api_url = api_url.rstrip('/') + '/'
        self.callback_url = callback_url 
        self.callback_path = urlparse(self.callback_url).path 

    def __call__(self, environ, start_response):       
        session = environ["beaker.session"]
        req = Request(environ)
        client = session.get(CLIENT_SESSION_ID, None)
        if not client:
            client = SLIClient(self.client_id, 
                               self.client_secret, 
                               self.api_url, 
                               self.callback_url)
            session[CLIENT_SESSION_ID] = client
            session["target"] = req.url 
            session.save()
            auth_url = client.get_login_url()
            resp = HTTPTemporaryRedirect(location=auth_url)
        elif (req.path == self.callback_path):
            code = req.GET["code"]
            client.connect(code)
            session['token'] = client.get_access_token()
            target = session.get("target", "http://localhost:8080/restricted")
            session.save()
            resp = HTTPTemporaryRedirect(location=target)
        elif 'token' in session:
            resp = req.get_response(self.app)
        else:
            resp = HTTPUnauthorized()
        return resp(environ, start_response)
