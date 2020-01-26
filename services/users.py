from adapters.mongoconnection import MongoConnect

class UserServices:

    def __init__(self):
        self.mongo = MongoConnect()
        self.collection = 'user'


    def create_new_user(self, params):
        '''
        This method creates a new user using the params passed by the user's request. 
        The new user will not be created if the CPF passed already exists in the database.
        '''

        response = {
            'http_code': None,
            'message': None,
            'payload': None
        }

        user_check = self.mongo.find_one({'cpf': params['cpf']}, self.collection)
        if user_check:
            response['http_code'] = 409
            response['message'] = 'Request failed - User with this CPF already registered'
        else:
            self.mongo.insert(params, self.collection)
            response['http_code'] = 200
            response['message'] = 'User created successfully!' 
        
        return response