import os
import zlib
from PIL import Image
from .converters import convert_to_string
import json
import csv

from .converters import byte_converters

__all__ = [
    "ShuttleAdapter",
]

def convert_to_dict(data):
    try:
        return json.loads(data)
    except:
        return data

class Save:
    
    @classmethod
    def txt_file(cls,data,file_name): 
        with open(file_name,'+w') as f:
            f.write(data)

    @classmethod
    def csv_file(cls,data,file_name):
        with open(file_name,'+w') as f:
            writer = csv.writer(f)
            for row in data:
                writer.writerow(row)

WRITE_FILE_TYPES = {
    'jpg' : lambda obj, fn: obj.save(fn),
    'png' : lambda obj, fn: obj.save(fn),
    'json': lambda data, fn: Save.txt_file(json.dumps(data), fn), 
    'txt' : lambda data, fn: Save.txt_file(data, fn), 
    'csv' : lambda data, fn: Save.csv_file(data, fn),
}

def save_to_file(data,file_path):
    try:
        _,tail = os.path.splitext(file_path)
        _, ext = tail.split('.')
        WRITE_FILE_TYPES[ext](data,file_path)
    except:
        return data

class Open:

    @classmethod
    def txt_file(cls,file_path):
        with open(file_path,'r') as f:
            data = f.read()
            try:
                return json.loads(data)
            except ValueError:
                new_rows = []
                rows = data.split('"}{"')
                for pos,row in enumerate(rows):
                    if pos == 0: 
                        new_rows.append('{}}}'.format(row))
                    elif pos == (len(rows)-1):
                        new_rows.append('{{{}'.format(row))
                    else:
                        new_rows.append('{{{}}}'.format(row))
                return new_rows
            except:
                return data
    @classmethod
    def csv_file(cls,file_path):
        with open(file_path, 'r') as f:
            data = []
            for row in list(csv.reader(f)):
                data.append(row)
            return data

READ_FILE_TYPES = {
    'jpg' : lambda x: Image.open(x),
    'png' : lambda x: Image.open(x),
    'json': lambda x: Open.txt_file(x),
    'txt' : lambda x: Open.txt_file(x), 
    'csv' : lambda x: Open.csv_file(x)
}

def read_from_file(data):
    try:
        _, tail = os.path.splitext(data)
        _, ext = tail.split('.')
        return READ_FILE_TYPES[ext](data)
    except (ValueError, TypeError):
        return data



def append_client_to_name(shuttle):
    return '-'.join([shuttle.name,
                shuttle.client.__class__.__name__])
    

class ExecuteClient:

    @staticmethod
    def decode_shuttle(shuttle, mime_type, params):
        # if params:
        shuttle.meta = params
        from_bytes = byte_converters['from_bytes'](mime_type,shuttle.data)
        shuttle.data = params.get('data') or from_bytes        
        return shuttle

    @staticmethod
    def encode_shuttle(shuttle, mime_type):
        shuttle.data = byte_converters['to_bytes'](mime_type,shuttle.data)
        return shuttle

    @staticmethod
    def run(client, shuttle, mime_type, params):
        #inherited from base
        decoded_shuttle = ExecuteClient.decode_shuttle(shuttle=shuttle,
                                              mime_type=mime_type,
                                              params=params)

        shuttle = client(decoded_shuttle)
        
        encoded_shuttle = ExecuteClient.encode_shuttle(shuttle=shuttle,
                                              mime_type=mime_type)
        return encoded_shuttle


#TO DELETE

class ShuttleAdapter:
    def __init__(self,shuttle):
        self._shuttle = shuttle
        self._original_name = self._shuttle.name
        self._client_name = self._shuttle.client.__class__.__name__

    @property
    def shuttle(self):
        #append client to operator name
        self._shuttle.name = '-'.join([self._original_name,
                self._client_name])
        return self._shuttle

    @shuttle.setter
    def shuttle(self,value):
        self._shuttle = value
        return value

    def write(self):
        try:
            with open(self.shuttle.write_path,'+w') as f:
                data = convert_to_string(self.shuttle.data)
                f.write(data)

        except TypeError: #implementing PIL image save
            self.shuttle.data.save(self.shuttle.write_path)

        return self.shuttle

    def read(self):
        
        try:
            with open(self.shuttle.write_path,'r') as f:
                self.shuttle.data = f.read()

        except UnicodeDecodeError:
            self.shuttle.data = Image.open(self.shuttle.write_path)
        
        except FileNotFoundError:
            pass

        return self.shuttle