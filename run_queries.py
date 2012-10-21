from sliclient import SLIClient, extract_id

import json
import sys

def get_client(client_id, client_secret, api_url, callback_url, access_token): 
    return SLIClient(client_id, client_secret, api_url, callback_url, access_token)

def pretty_print(response, content):
    if response: 
        print "STATUS:", response.response.status_code  
    print "RESPONSE:"
    print json.dumps(response.content, sort_keys=True, indent=4)

def main():
    if len(sys.argv) != 6:
        print "Usage:", sys.argv[0],"client_id client_secret api_url callback_url access_token"
        sys.exit(1)

    client_id = sys.argv[1]
    client_secret = sys.argv[2]
    api_url = sys.argv[3]
    callback_url = sys.argv[4]
    access_token = sys.argv[5]

    client = get_client(client_id, client_secret, api_url, callback_url, access_token)

    q = "teachers"
    r = client.get(q)
    pretty_print(r, r.content)

    learningStandard = {
        'learningStandardId': {
                       'contentStandardName' : 'Common Core',
                       'identificationCode'  : 'CC RL.K.1'
                      }, 
        'description': 'Common Core RL.K.1',
        'contentStandard': 'National Standard',
        'gradeLevel': 'Kindergarten',
        'subjectArea': 'Reading'
    }
    headers = {'content-type': 'application/json'}
    q = client.post("learningStandards", data=json.dumps(learningStandard), headers=headers)
    if q.response.status_code == 201: 
        new_id = extract_id(q.response)
        print "ID of newly created item:" + new_id 

    student_ids = [s['id'] for s in client.get('students').content]
    first = student_ids[0]
    import pdb; pdb.set_trace() 
    gb = client.get('students/' + first + '/reportCards')


if __name__=="__main__":
    main() 