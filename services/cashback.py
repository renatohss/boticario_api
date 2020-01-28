import requests
import json

def cashback_request():
    response = {
            'http_code': None,
            'message': None,
            'payload': None
        }

    url = 'https://mdaqk8ek5j.execute-api.us-east-1.amazonaws.com/v1/cashback?cpf=12312312323'
    headers = {'token': 'ZXPURQOARHiMc6Y0flhRC1LVlZQVFRnm' }
    try:
        req = requests.get(url, headers=headers)
    except ConnectionError:
        response['status_code'] = 500
        response['message'] = 'Could not connect to external API - Check URI'

    status_code = req.status_code
    print(status_code)
    if status_code != 200:
        pass
    else:
        payload = json.loads(req.text)
        response['http_code'] = status_code
        response['message'] = 'Request was successful!'
        response['payload'] = payload['body']

    return response
