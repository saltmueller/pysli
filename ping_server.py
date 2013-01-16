from sliclient import SLIClient

import sys 
import time

API_URL = "https://api.sandbox.slcedu.org"

def ping(api_url, auth_token): 
    client = SLIClient("dummy", "dummy", api_url, "dummy", auth_token)
    while True:
        result = client.get("%s/api/rest/system/session/check" % API_URL) 
        data = result.response.json()
        if not data[u'authenticated']:
            print "Not authenticated: Get a valid session token !"
            sys.exit(1)
        print "Successfully Pinged server with token %s" % auth_token
        time.sleep(60 * 5 - 1)

def main():
    if len(sys.argv[1:2]) != 1:
        print "Usage:", sys.argv[0], "auth_token"
        sys.exit(1)

    auth_token = sys.argv[1]
    ping(API_URL, auth_token)

if __name__=="__main__":
    main() 
