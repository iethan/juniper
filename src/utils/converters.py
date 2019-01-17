import json
import io
from PIL import Image

def convert_to_string(data):
    try:
        return json.dumps(data)
    except:
        return str(data)

def bytes_to_dict(bytes_io):
    data = bytes_io.read()
    return json.loads(data.decode('utf-8'))

def bytes_to_str(bytes_io):
    data = bytes_io.read()
    try:
        return json.loads(data.decode('utf-8'))
    except:
        return data.decode('utf-8')

def str_to_bytes(str_data):
    bytes_io = io.BytesIO()
    try:
        str_data = json.dumps(str_data)
    except:
        pass
    bytes_io.write(str_data.encode('utf-8'))
    bytes_io.seek(0)
    return bytes_io

def dict_to_bytes(dict_data):
    bytes_io = io.BytesIO()
    dict_to_str = json.dumps(dict_data)
    bytes_io.write(dict_to_str.encode('utf-8'))
    bytes_io.seek(0)
    return bytes_io

def img_to_bytes(img_data,mime_type):
    bytes_io = io.BytesIO()
    img_data.save(bytes_io,mime_type)    
    bytes_io.seek(0)
    return bytes_io

def bytes_to_img(bytes_io,mime_type):
    return Image.open(bytes_io)

to_byte_converters = {
    'dict' : lambda x: dict_to_bytes(x),
    'str' : lambda x: str_to_bytes(x),
    'png' : lambda x: img_to_bytes(x,'png'),
    'jpg' : lambda x: img_to_bytes(x,'jpg'),
    'list' : lambda x: dict_to_bytes(x),
}

from_byte_converters = {
    'dict' : lambda x: bytes_to_dict(x),
    'str' : lambda x: bytes_to_str(x),
    'png' : lambda x: bytes_to_img(x,'png'),
    'jpg' : lambda x: bytes_to_img(x,'jpg'),
    'list' : lambda x: bytes_to_dict(x),
}

byte_converters = {
    'from_bytes' : lambda x,y: from_byte_converters[x](y),
    'to_bytes' : lambda x,y: to_byte_converters[x](y)
}