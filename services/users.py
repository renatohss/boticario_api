from adapters.mongoconnection import MongoConnect
from werkzeug.security import generate_password_hash, check_password_hash
from services.auth import generate_jwt_token
from flask import current_app

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
        For security, user's password will be hashed using SHA256
        '''

        user_check = self.mongo.find_one({'cpf': parameters['cpf']}, self.collection)
        if user_check:
            self.response['http_code'] = 409
            self.response['message'] = 'Cannot create new user - User with informed CPF already registered'
        else:
            password_hash = generate_password_hash(parameters['password'], method='sha256')
            parameters['password'] = password_hash
            try:
                self.mongo.insert(parameters, self.collection)
            except:
                self.response['http_code'] = 500
                self.response['message'] = 'Could not create new user - Error with MongoDB Connection'
                return self.response
                
            self.response['http_code'] = 200
            self.response['message'] = 'User created successfully!' 
        
        return self.response

    
    def get_all_users(self):
        '''
        This method retrieves all users registered in the database
        '''
        query = self.mongo.find_all({}, self.collection)

        user_list = []
        for user in query:
            user['_id'] = str(user['_id'])
            user_list.append(user)

        self.response['http_code'] = 200
        self.response['message'] = 'Request successful'
        self.response['payload'] = user_list
        return self.response


    def authenticate_user(self, parameters):
        '''
        This method receives the user's CPF and password to validate his credentials and returns a JWT token if valid
        '''
        userdata = self.mongo.find_one({'cpf': parameters['cpf']}, self.collection)
        if not userdata:
            self.response['http_code'] = 401
            self.response['message'] = 'Invalid credentials - Check CPF number or password'
            return self.response

        check_hash = check_password_hash(userdata['password'], parameters['password'])
        if check_hash:
            token = generate_jwt_token(parameters['cpf'])
            self.response['http_code'] = 200
            self.response['message'] = 'Authentication OK'
            self.response['payload'] = {
                                        'auth_token': token
                                        }
        else:
            self.response['http_code'] = 401
            self.response['message'] = 'Invalid credentials - Check CPF number or password'
        return self.response




