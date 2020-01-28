from .rest_handler import http_response

def validate_json_format(obj):
    '''
    Receives an object and check to see if it is a instance of dict
    '''
    if not isinstance(obj, dict):
        return http_response(400, 'Invalid request - Expecting a JSON body', None)