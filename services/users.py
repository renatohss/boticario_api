from adapters.mongoconnection import MongoConnect
from werkzeug.security import generate_password_hash, check_password_hash
from bson import json_util
from services.auth import generate_jwt_token

class UserServices:    

    def __init__(self):
        self.mongo = MongoConnect()
        self.collection = 'user'
        self.response = {
            'http_code': None,
            'message': None,
            'payload': None
        }


    def create_new_user(self, parameters):
        '''
        This method creates a new user using the parameters passed by the user's request. 
        The new user will not be created if the CPF passed already exists in the database.
        '''

        user_check = self.mongo.find_one({'cpf': parameters['cpf']}, self.collection)
        if user_check:
            self.response['http_code'] = 409
            self.response['message'] = 'Request failed - User with this CPF already registered'
        else:
            password_hash = generate_password_hash(parameters['password'], method='sha256')
            parameters['password'] = password_hash
            self.mongo.insert(parameters, self.collection)
            self.response['http_code'] = 200
            self.response['message'] = 'User created successfully!' 
        
        return self.response

    
    def get_all_users(self):
        '''
        This method retrieves all users registered in the database
        '''
        job = self.mongo.find_all({}, self.collection)

        user_list = []
        for user in job:
            user['_id'] = str(user['_id'])
            user_list.append(user)

        self.response['http_code'] = 200
        self.response['message'] = 'Request OK!'
        self.response['payload'] = user_list
        return self.response


    def authenticate_user(self, app, parameters):

        userdata = self.mongo.find_one({'cpf': parameters['cpf']}, self.collection)
        check_hash = check_password_hash(userdata['password'], parameters['password'])
        if check_hash:
            self.response['http_code'] = 200
            self.response['message'] = 'Authentication OK'
        else:
            token = generate_jwt_token(app, parameters['cpf'])
            print(token)
            self.response['http_code'] = 400
            self.response['message'] = 'Invalid credentials - Check CPF number or password'
        return self.response




