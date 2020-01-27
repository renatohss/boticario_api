from flask import Flask, request, make_response
from helpers.rest_handler import http_response
from services.users import UserServices
from services.orders import OrderServices
from services.auth import jwt_required
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkeytest'
# app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY')

userservices = UserServices()
orderservices = OrderServices()

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
        
        response = userservices.authenticate_user(data)
        return http_response(response['http_code'], response['message'], response['payload'])


@app.route('/orders', methods=['GET', 'DELETE', 'POST', 'PUT'])
@jwt_required
def orders():
    if request.method == 'GET':
        body = request.get_json()

        if not isinstance(body, dict):
            return http_response(400, 'Invalid request - Expecting a JSON body', None)

        else:
            try:
                data = {
                    'seller_cpf': str(body['seller_cpf']),
                    'start_date': body['start_date'],
                    'end_date': body['end_date']
                }
            except KeyError as error:
                return http_response(422, 'Missing {} key on JSON body'.format(str(error)), None)

            response = orderservices.get_orders(data)
        
            return response
        
    if request.method == 'DELETE':
        pass
    if request.method == 'POST':
        body = request.get_json()

        try:
            data = {
                'order_code': str(body['order_code']),
                'order_value': body['order_value'],
                'order_date': body['order_date'],
                'seller_cpf': str(body['seller_cpf'])
            }            
        except KeyError as error:
            return http_response(422, 'Missing {} key on JSON body'.format(str(error)), None)

        response = orderservices.create_new_order(data)

        return http_response(response['http_code'], response['message'], response['payload'])

    if request.method == 'PUT':
        pass


@app.route('/health_check')
@jwt_required
def health_check():
    return http_response(200, 'Server up!', None)