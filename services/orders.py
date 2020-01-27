from adapters.mongoconnection import MongoConnect

class OrderServices:

    def __init__(self):
        self.mongo = MongoConnect()
        self.collection = 'order'
        self.response = {
            'http_code': None,
            'message': None,
            'payload': None
        }

    @staticmethod
    def calculate_cashback(total_value):
        '''
        This static method receives the total value of the sales and returns the 
        cashback percentage as a string and the cashback coeficient to calculate the value
        '''
        if total_value <= 1000:
            cashback_percentage = '10%'
            cashback = 0.1
        elif total_value >= 1001 and total_value <= 1500:
            cashback_percentage = '15%'
            cashback = 0.15
        else:
            cashback_percentage = '20%'
            cashback = 0.2

        return (cashback_percentage, cashback)


    def create_new_order(self, parameters):
        '''
        This method receives the order's parameters set by the user and saves them as a new object in the database
        The new order will not be created if the informed order code already exists in the database
        '''
        order_check = self.mongo.find_one({'order_code': parameters['order_code']}, self.collection)
        if order_check:
            self.response['http_code'] = 409
            self.response['message'] = 'Cannot create new order - Order with informed code already exists'
            return self.response
        else:
            parameters['status'] = 'Em validação' if parameters['seller_cpf'] != '15350946056' else 'Aprovado'
            try:
                self.mongo.insert(parameters, self.collection)
            except:
                self.response['http_code'] = 500
                self.response['message'] = 'Could not create new order - Error with MongoDB Connection'
                return self.response
            
            self.response['http_code'] = 200
            self.response['message'] = 'Order created successfully!' 
            return self.response

    def get_orders(self, parameters):
        '''
        This method returns all the orders made by the informed seller's CPF and within the date range set by the user.
        It returns the list with all orders and all the cashback due already calculated
        '''
        query_params = {
            'seller_cpf': parameters['seller_cpf'],
            'order_date': {'$gte': parameters['start_date'], "$lte": parameters['end_date']}
        }
        query = self.mongo.find_all(query_params, self.collection)

        order_list = []
        order_total = 0.0
        for order in query:
            order['_id'] = str(order['_id'])
            order_total += order['order_value'] if order['order_value'] else 0.0
            order_list.append(order)

        percentage, coeficient = self.calculate_cashback(order_total)

        self.response['http_code'] = 200
        self.response['message'] = 'Request successful'
        self.response['payload'] = order_list
        return self.response
