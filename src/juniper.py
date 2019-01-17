import os
import shutil
import io

import json

from pprint import pprint as p

__all__ = [
    "Shuttle",
    "Juniper",
]

class Cache: pass    

class Shuttle:
    def __init__(self,name=None):
        self._name = name
        self._data = {}
        self._meta = {}

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
    def data(self):
        value = self._data or io.BytesIO(
            json.dumps({}).encode('utf-8')
            ) 
        return value

    @data.setter
    def data(self,value):
        self._data = value
        return value

    @property
    def meta(self):
        return self._meta

    @meta.setter
    def meta(self,value):
        self._meta = value
        return value       
        
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