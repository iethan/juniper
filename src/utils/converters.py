import json

def convert_to_string(data):
    try:
        return json.dumps(data)
    except:
        return str(data)
    