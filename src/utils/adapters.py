import os
import zlib
from PIL import Image
from .converters import convert_to_string
import json
import csv

from .converters import byte_converters

__all__ = [
    "ParamAdapter",
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
    

class ParamAdapter:

    def __init__(self, shuttle, params, client=None):
        self.params = params or {}
        self.shuttle = shuttle
        self.client = client

    def run(self,):      

        shuttle = self.shuttle
        params = self.params
        client = self.client
        
        shuttle.client = client

        drop_params = self.params.get('drop_params')
        if isinstance(drop_params,list):
            shuttle.meta = {k:v for k,v in params.items() \
                        if not k in drop_params}

        elif drop_params == 'all':
            shuttle.meta = {}

        elif params:
            shuttle.meta = params
        
        mime_type = shuttle.meta.get('mime_type')
        data = shuttle.meta.get('data')  
   
        if data:
            shuttle.data = data
        if mime_type:
            shuttle.mime_type = mime_type

        shuttle.meta.pop('data',None)

        if params:
            shuttle.meta.pop('mime_type',None)
            shuttle.meta.pop('drop_params',None)

        return shuttle        

