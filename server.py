from bottle import route, run
from bottle import static_file
from middleware import OAuthMiddleware
from beaker.middleware import SessionMiddleware

from urlparse import urlparse
from sliclient import SLIClient

import bottle
import sys 

class OAuth(object):
    def __init__(self):
        pass

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            print "Wrapper called"
            return func(*args, **kwargs)
        return wrapper
auth = OAuth()

def get_sli_client_factory(client_id, client_secret, api_url, callback_url): 
    """ Creates a SLIClient factory by wrapping params in a closure""" 
    callback_path = urlparse(callback_url).path 

    def sli_client_factory():
        return  SLIClient(client_id, client_secret, api_url, callback_url)

    return (callback_path, sli_client_factory)

@route('/app/<filename:path>')
def send_static(filename):
    return static_file(filename, root='./teachers/app')

@route('/restricted')
def restricted():
    return "Restricted reached !"

def main(): 
    if len(sys.argv) != 5:
        print "Usage:", sys.argv[0],"client_id client_secret api_url callback_url"
        sys.exit(1)

    client_id = sys.argv[1]
    client_secret = sys.argv[2]
    api_url = sys.argv[3]
    callback_url = sys.argv[4]

    # set up beaker sessions 
    session_opts = {
        'session.type': 'file',
        'session.cookie_expires': 300,
        'session.data_dir': './data',
        'session.auto': True
    }

    sli_client_factory = get_sli_client_factory(client_id, client_secret, )
    oauth_app = OAuthMiddleware(bottle.app(), )
    app = SessionMiddleware(oauth_app, session_opts)
    run(app=app, host='localhost', port=8080, debug=True)

if __name__=="__main__":
    main() 