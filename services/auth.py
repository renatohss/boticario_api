from helpers.rest_handler import http_response
from adapters.mongoconnection import MongoConnect
from flask import request, current_app
from functools import wraps
import jwt
import datetime

mongo = MongoConnect()

def jwt_required(func):

    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.headers.get('authorization').split(' ')[1]

        if not token:
            return http_response(401, 'JWT token is missing', None)

        data = jwt.decode(token, current_app.config['SECRET_KEY'])
        user_check = mongo.find_one({'cpf': data['user']}, 'user')
        if not user_check:
            return http_response(401, 'JWT token is invalid!', None)

        return func(*args, **kwargs)
    
    return decorated

def generate_jwt_token(cpf):
    token_expiration = datetime.datetime.utcnow() + datetime.timedelta(minutes=5000)
    jwt_token = jwt.encode({'user': cpf, 'exp': token_expiration}, current_app.config['SECRET_KEY'])
    return jwt_token.decode("utf-8")
