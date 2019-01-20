import os
import shutil
import io

import json

from pprint import pprint as p

from .utils.converters import byte_converters

__all__ = [
    "Shuttle",
    "Juniper",
]

class Cache: pass    

class Shuttle(Exception):

    MIME_TYPES = ['dict', 'str', 'png',
                  'jpg', 'list']

    def __init__(self,):
        self._name = None
        self._data = None
        self._meta = {}
        self._encoded_data = None
        self._decoded_data = None
        self._mime_type = None

    @property
    def meta(self):
        return self._meta

    @meta.setter
    def meta(self,value):
        self._meta = value
        return value   

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self,value):
        self._name = value
        return value

    @property
    def client(self):
        return self._client

    @client.setter
    def client(self,value):
        self._client = value
        return value

    @property
    def mime_type(self,):
        return self._mime_type or 'str'

    @mime_type.setter
    def mime_type(self,value):
        if value not in Shuttle.MIME_TYPES:
            raise Exception('{} not a valid mime_type'.format(value))
        else:
            self._mime_type = value
            return value

    @property
    def data(self,):
        return self._data

    @data.setter
    def data(self,value):  
        self._data = value     
        return value

    @staticmethod
    def encode_data(data,mime_type):
        if isinstance(data,bytes):
            return data  
        else: 
            return byte_converters['to_bytes'](mime_type, data or '')

    @property
    def encoded_data(self,):            
        return Shuttle.encode_data(self.data,self.mime_type)    

    @encoded_data.setter
    def encoded_data(self, value): 
        print(self.mime_type)  
        encoded_value = Shuttle.encode_data(value,self.mime_type)    
        self._encoded_data = encoded_value
        return encoded_value
    
    @staticmethod
    def decode_data(data,mime_type):
        return byte_converters['from_bytes'](mime_type, data or '')
        
    @property
    def decoded_data(self,):
        return Shuttle.decode_data(self.data,self.mime_type)

    @decoded_data.setter
    def decoded_data(self,value):   
        decoded_value = Shuttle.decode_data(self.data,self.mime_type)  
        self._decoded_data = decoded_value   
        return decoded_value
        
class Juniper:

    def __init__(self,cache=None,logging=None):        
        #todo implement 
        self.cache = cache
        self.logging = logging
    
    def __rshift__(self,io):
        
        shuttle = Shuttle()

        for step,obj in enumerate(io.objs):            
            step = '{0:03d}'.format(step)
            shuttle.name = '-'.join([step,obj.__class__.__name__])
            shuttle = obj.execute(shuttle)

            print(shuttle.name)