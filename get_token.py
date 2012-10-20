from sliclient import SLIClient

import sys 

def get_access_token(client_id, client_secret, api_url, callback_url): 
    client = SLIClient(client_id, client_secret, api_url, callback_url)
    request_url = client.get_login_url()

    # open it in a webbrowser and paste the returned code
    print "Open this URL in your browser: %s" % request_url
    print "Then cut-and-paste the code below."
    code = raw_input("Code from query string:")

    # connect to he server 
    client.connect(code)

    r_1 = client.get("https://api.sandbox.slcedu.org/api/rest/system/session/check") 
    if r_1.response.status_code != 200:
        print "Unable to perform session check. Status code: %s" % r_1.response.status_code
        sys.exit(1)

    r_2 = client.get("https://api.sandbox.slcedu.org/api/rest/v1/students")
    if r_2.response.status_code != 200:
        print "Unable to perform session check. Status code: %s" % r_2.response.status_code
        sys.exit(1)

    # print out the auth token 
    return client.get_access_token()

def main():
    if len(sys.argv) != 5:
        print "Usage:", sys.argv[0],"client_id client_secret api_url callback_url"
        sys.exit(1)

    client_id = sys.argv[1]
    client_secret = sys.argv[2]
    api_url = sys.argv[3]
    callback_url = sys.argv[4]

    print "Access token: %s" % get_access_token(client_id, client_secret, api_url, callback_url)

if __name__=="__main__":
    main() 