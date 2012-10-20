from webob import Request
from webob.exc import HTTPTemporaryRedirect, HTTPUnauthorized
from rauth.service import OAuth2Service

CLIENT_SESSION_ID = "oauth.client"

CLIENT_ID = ""
CLIENT_SECRET = ""
API_URL = "https://api.sandbox.slcedu.org/"
AUTHORIZE_URL = API_URL + "api/oauth/authorize"
ACCESS_TOKEN_URL = API_URL + "api/oauth/token"
CALLBACK_URL = "http://local.slidev.org:8080/callback"
CALLBACK_PATH = "/callback"
TARGET_URL = "http://local.slidev.org:8080/restricted"

class OAuthMiddleware(object):
    "Example middleware that appends a message to all 200 html responses"    
    def __init__(self, app):
        self.app = app
    def __call__(self, environ, start_response):       

        session = environ["beaker.session"]
        req = Request(environ)
        client = session.get(CLIENT_SESSION_ID, None)
        if not client:
            client = OAuth2Service(
                       name='example',
                       consumer_key = CLIENT_ID,
                       consumer_secret = CLIENT_SECRET,
                       access_token_url = ACCESS_TOKEN_URL,
                       authorize_url = AUTHORIZE_URL)
            session[CLIENT_SESSION_ID] = client
            session.save()
            auth_url = client.get_authorize_url(redirect_uri=CALLBACK_URL, response_type='code')
            resp = HTTPTemporaryRedirect(location=auth_url)
        elif (req.path == CALLBACK_PATH):
            code = req.GET["code"]
            data = dict(code=code,
                   grant_type='authorization_code',
                   redirect_uri=CALLBACK_URL)
            token = client.get_access_token('POST', data=data).content[u'access_token']
            session['token'] = token
            session.save()
            resp = HTTPTemporaryRedirect(location=TARGET_URL)
        elif 'token' in session:
            resp = req.get_response(self.app)
        else:
            resp = HTTPUnauthorized()
        return resp(environ, start_response)
