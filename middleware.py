from webob import Request
from webob.exc import HTTPTemporaryRedirect, HTTPUnauthorized

AUTH_TOKEN_SESSION_ID = "oauth.token"

class OAuthMiddleware(object):
    "Example middleware that appends a message to all 200 html responses"

    def __init__(self, app, callback_path, sli_client_factory):
        self.sli_client_factory = lambda self: sli_client_factory()
        self.callback_path = callback_path.rstrip("/") + "/"

    def __call__(self, environ, start_response):       
        session = environ["beaker.session"]
        req = Request(environ)
        oauth_token = session.get(AUTH_TOKEN_SESSION_ID, None)
        if not oauth_token: 
            if (req.path.rstrip("/") + "/") == self.callback_path:
                code = req.GET["code"]
                client = self.sli_client_factory() 
                client.connect(code)
                session[AUTH_TOKEN_SESSION_ID] = client.get_access_token()
                target = session.get("target", "http://localhost:8080/restricted")
                session.save()
                resp = HTTPTemporaryRedirect(location=target)
            else:
                session["target"] = req.url 
                session.save()
                client = self.sli_client_factory()
                auth_url = client.get_login_url()
                resp = HTTPTemporaryRedirect(location=auth_url)
        else:
            resp = req.get_response(self.app)
        return resp(environ, start_response)
