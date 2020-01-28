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


    @staticmethod
    def parse_updated_fields(updated_fields):

        response = {}

        for k, v in updated_fields.items():
            if v:
                response[k] = v
        
        return response


    def create_new_order(self, parameters):
        '''
        This method receives the order's parameters set by the user and saves them as a new object in the database
        The new order will not be created if the informed order code already exists in the database
        '''
        order_check = self.mongo.find_one({'order_code': parameters['order_code']}, self.collection)
        if order_check:
            self.response['http_code'] = 409
            self.response['message'] = 'Cannot create new order - Order with informed code already exists'
        else:
            parameters['status'] = 'Em validação' if parameters['seller_cpf'] != '15350946056' else 'Aprovado'
            self.mongo.insert(parameters, self.collection)
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

        for order in order_list:
            order['cashback_percentage'] = percentage
            order['cashback_value'] = round((order['order_value'] * coeficient), 2)

        self.response['http_code'] = 200
        self.response['message'] = 'Request successful'
        self.response['payload'] = order_list
        return self.response


    def delete_order(self, parameters):
        '''
        This method will delete the order with the specified order code if its status is 
        different than "Aprovado" and it's owned by the informed CPF
        '''
        status_check = self.mongo.find_one(parameters, self.collection)
        if status_check:
            if status_check['status'] != 'Aprovado':
                self.mongo.find_one_and_delete(parameters, self.collection)
                self.response['status_code'] = 200
                self.response['message'] = 'Order deleted with success'
            else:
                self.response['status_code'] = 400
                self.response['message'] = 'Could not delete order - Status is "Aprovado"'
        else:
            self.response['status_code'] = 400
            self.response['message'] = f'The order with order code {parameters["order_code"]} does not exists for the CPF {parameters["cpf"]}'
        return self.response


    def update_order(self, parameters):
        '''
        This method extracts the query and update information from the parameters and updates the specified order if its
        status is not "Aprovado" and is owned by the informed CPF
        '''
        query = {
            'seller_cpf': parameters['seller_cpf'],
            'order_code': parameters['order_code']
        }

        status_check = self.mongo.find_one(query, self.collection)
        if status_check:
            if status_check['status'] != 'Aprovado':
                updated_fields = self.parse_updated_fields(parameters['updated_fields'])
                self.mongo.update_one(query, updated_fields, self.collection)
                self.response['status_code'] = 200
                self.response['message'] = 'Order updated with success'
            else:
                self.response['status_code'] = 400
                self.response['message'] = 'Could not update order - Status is "Aprovado"'
        else:
            self.response['status_code'] = 400
            self.response['message'] = f'The order with order code {parameters["order_code"]} does not exists for the CPF {parameters["seller_cpf"]}'
        return self.response
