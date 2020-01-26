from flask import Flask, request, make_response
from helpers.rest_handler import http_response
from services import UserServices

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkeytest'

userservices = UserServices()

@app.route('/health_check')
def health_check():
    return http_response(200, 'Server up!', None)
    

@app.route('/users', methods=['POST', 'GET', 'DELETE'])
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
    
    elif request.method == 'GET':
        response = userservices.get_all_users()
        return http_response(response['http_code'], response['message'], response['payload'])



@app.route('/login', methods=['GET'])
def login():

    body = request.get_json()

    if not isinstance(body, dict):
        return http_response(400, 'Invalid request - Expecting a JSON body', None)
    else:
        try:
            data = {
                'cpf': body['cpf'],
                'password': body['password']
            }
        except KeyError as error:
            return http_response(422, 'Missing {} key on JSON body'.format(str(error)), None)
        
        response = userservices.authenticate_user(app, data)

        return http_response(response['http_code'], response['message'], None)



    return 'body'


if __name__ == "__main__":
    app.run(debug=True)