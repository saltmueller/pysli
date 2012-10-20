from bottle import route, run
from bottle import static_file
from middleware import OAuthMiddleware
from beaker.middleware import SessionMiddleware

import bottle 

class OAuth(object):
    def __init__(self):
        pass

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            print "Wrapper called"
            return func(*args, **kwargs)
        return wrapper
auth = OAuth()

@route('/app/<filename:path>')
def send_static(filename):
    return static_file(filename, root='./teachers/app')

@route('/callback')
def oauth_callback():
    return "Callback "

@route('/restricted')
@auth
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
    oauth_app = OAuthMiddleware(bottle.app())
    app = SessionMiddleware(oauth_app, session_opts)
    run(app=app, host='localhost', port=8080, debug=True)

if __name__=="__main__":
    main() 