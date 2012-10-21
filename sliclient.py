from rauth.service import OAuth2Service
from rauth.service import Request, Response
from urlparse import urlparse

import copy
import os 
import requests

class ExtendedRequest(Request):
    def patch(self, url, **kwargs):
        '''Sends a PATCH request. Returns :class:`Response` object.

        :param url: The resource to be requested.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        '''
        return self.request('PATCH', url, **kwargs)

class SLIClient(ExtendedRequest):

    API_ACCESS_TOKEN_PATH = '/api/oauth/token'
    API_AUTHORIZE_PATH = '/api/oauth/authorize'
    API_PATH_PREFIX = "/api/rest/v1/"

    def __init__(self, client_id, client_secret, api_uri, callback_uri, access_token=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.api_uri = api_uri.rstrip("/")
        self.base_uri = self.api_uri + self.API_PATH_PREFIX
        self.access_token_uri = self.api_uri + self.API_ACCESS_TOKEN_PATH
        self.authorize_uri = self.api_uri + self.API_AUTHORIZE_PATH
        self.callback_uri = callback_uri
        self.access_token = access_token
        self.oauth_service = OAuth2Service(
                       name='sli-oauth-client',
                       consumer_key = client_id, 
                       consumer_secret = client_secret, 
                       access_token_url = self.access_token_uri, 
                       authorize_url = self.authorize_uri)
        self.session = requests.session()

    def get_login_url(self):
        return self.oauth_service.get_authorize_url(redirect_uri=self.callback_uri, response_type='code')

    def connect(self, code):
        data = dict(code=code,
                   grant_type='authorization_code',
                   redirect_uri=self.callback_uri)
                           
        resp = self.oauth_service.get_access_token('POST', data=data)
        self.access_token = resp.content[u'access_token']

    def get_access_token(self): 
        return self.access_token

    def request(self, method, url, **kwargs):
        '''Sends a request to an OAuth 2.0 endpoint, properly wrapped around
        requests. (Copied from RAuth library)
        The authtoken is automatically injected if available.

        :param method: A string representation of the HTTP method to be used.
        :param url: The resource to be requested.
        :param \*\*kwargs: Optional arguments. Same as Requests.
        '''
        # make sure the url is absolute
        if not url.startswith("http"): 
            url = self.base_uri + url.lstrip("/")

        # inject the access token into the headers
        use_kwargs = copy.deepcopy(kwargs)
        headers = (use_kwargs.get("headers", {})).copy() 
        if self.access_token and (("authorization" not in headers) or (not headers["authorization"].strip().lower().startswith("bearer"))):
            headers["authorization"] = "bearer %s" % self.access_token
            use_kwargs["headers"] = headers

        use_kwargs['timeout'] = use_kwargs.get('timeout', 300)
        response = self.session.request(method, url, **use_kwargs)
        return Response(response)


def extract_id(response):
    location = response.headers['location']
    path = urlparse(location).path 
    return os.path.split(path)[1]
