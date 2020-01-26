from helpers.rest_handler import http_response
from functools import wraps
import jwt
import datetime


def jwt_required(func):

    @wraps(func)
    def decorated(*args, **kwargs):
        return func(*args, **kwargs)
    
    return decorated

def generate_jwt_token(app, cpf):
    jwt_token = jwt.encode({'cpf': cpf, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
    print(jwt_token)
    return jwt_token
