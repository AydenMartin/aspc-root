import json
import RequestBodies as rq
import requests

def get_account_info():
    header = "X-Plex-Connect-Api-Key"
    consumer_key = 'wBBsPULQUmgVIVu8QPFN068iDsTz58Rm'
    consumer_secret = 'qOA8QyAkjqYuAuGa'
    api_url_base = "https://connect.plex.com/"
    my_header1 = {'Content-Type': 'application/json',
               'X-Plex-Connect-Api-Key': 'sb5GlSUdLsb1DGksq9BPz0wBQwEuKXJp'}

    header2 = {'Content-Type': 'application/json',
               'Authorization': 'Bearer {wBBsPULQUmgVIVu8QPFN068iDsTz58Rm}'}

    partBase = "https://connect.plex.com/mdm/v1/parts"


    response = requests.get(partBase, headers=my_header1)
    print(response)
    print(response.content)
    print(response.request.url)
    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None

get_account_info()