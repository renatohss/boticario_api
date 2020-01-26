from flask import jsonify

def http_response(status_code, message, payload):
    '''
    Method used to build default HTTP responses. 
    Receives the status code, message to the user and payload, if any, as parameters
    '''
    return jsonify({
        'status_code': status_code,
        'message': message,
        'payload': payload
    })

