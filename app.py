from flask import Flask, request
from helpers.rest_handler import http_response
from services import UserServices

app = Flask(__name__)

userservices = UserServices()

@app.route('/health_check')
def health_check():
    return http_response(200, 'Server up!', None)
    

@app.route('/new_user', methods=['POST'])
def create_user():

    if request.method == 'POST':
        body = request.json
        
        try:
            data = {
                'full_name': body['full_name'],
                'cpf': str(body['cpf']),
                'email': body['email'],
                'password': str(body['password'])
            }

        except KeyError as error:
            return http_response(422, 'Missing {} key on JSON body'.format(str(error)), None)

    response = userservices.create_new_user(data)
    
    return http_response(response['http_code'], response['message'], response['payload'])


@app.route('/auth', methods=['POST'])
def auth_user():
    pass