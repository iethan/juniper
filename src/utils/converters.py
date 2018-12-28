import json

def convert_to_string(data):
    if isinstance(data,dict):
        return json.dumps(data)
    if isinstance(data,(float,str)):
        return str(data)
    