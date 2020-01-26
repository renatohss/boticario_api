from pymongo import MongoClient

class MongoConnect:
    '''
    Class with all the methods to work with MongoDB
    '''

    def __init__(self):
        self.client = MongoClient('172.17.0.2', 27017)
        self.db = self.client.boticario_api
        self.user_coll = self.db.users
        self.order_coll = self.db.orders


    def collection_fetcher(self, collection):
        '''
        Returns the collection object based on the collection name passed
        '''
        if collection == 'user':
            return self.user_coll
        elif collection == 'order':
            return self.order_coll
        else:
            return None


    def insert(self, parameters, collection):
        '''
        Insert a new document with the parameters passed in the designated collection
        '''
        collection = self.collection_fetcher(collection)
        response = collection.insert_one(parameters)
        return response


    def find_one(self, parameters, collection):
        '''
        Finds a single document with the specified parameters in the designated collection
        '''
        collection = self.collection_fetcher(collection)
        response = collection.find_one(parameters)
        return response

    
    def find_all(self, parameters, collection):
        '''
        Finds all documents which match the specified parameters in the designated collection
        '''
        collection = self.collection_fetcher(collection)
        response = collection.find(parameters)
        return response


    def find_one_and_delete(self, parameters, collection):
        '''
        Finds a single document with the specified parameters and deletes it from the designated collection
        '''
        collection = self.collection_fetcher(collection)
        response = collection.find_one_and_delete(parameters)
        return response

