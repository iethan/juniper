import os
import zlib
from PIL import Image
from .converters import convert_to_string

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


# 	@property
#     def shuttle_name(self):
#         self.shuttle.name = '-'.join([self.shuttle.name,
#                 self.shuttle.client.__class__.__name__])
#         return self._shuttle_name

#     @shuttle_name.setter
#     def shuttle_name(self,value):
#         self._shuttle_name = value
#         return value

#     def execute_cache(self,):
#         if not os.path.exists('cache'):
#             os.makedirs('cache')

#     @property
#     def compressed_data(self):
#         data = self.shuttle.data.encode('utf-8')
#         return zlib.compress(data)

#     @compressed_data.setter
#     def compressed_data(self,value):
#         self._compressed_data = value
#         return value

#     @property
#     def cache_path(self):

#         operator_name = self.shuttle.client.__class__.__name__
        
#         compressed_str = self.compressed_data[:15].decode('utf-8')
        
#         cache_dir = self.shuttle.cache.cache_dir
#         cache_path = '{}/cache/{}-{}-{}.txt'.format(cache_dir,
#                     self.shuttle.name,operator_name,compressed_str)

#         return cache_path

#     @cache_path.setter
#     def cache_path(self,value):
#         self._cache_path = value
#         return value

#     def read(self,):

#         if self.shuttle.cache.history:
#             cache_path = self.shuttle.cache.cache_path
#             self.cache_path = cache_path

#             with open(cache_path,'w+') as f:
#                 data = f.read()
#             self.shuttle.data = zlib.decompress(data).decode('utf-8')

#         return self.shuttle

#     def write(self,):

#         if self.shuttle.cache.history:
#             self.shuttle.cache.cache_path = self.cache_path

#             with open(self.cache_path,'w+') as f:
#                 f.write(self.compressed_data)

#         return self.shuttle


# def shuttle_adapter(shuttle, client, data, write_path=None):

#     if shuttle.cache.history:
#         if not os.path.exists('cache'):
#             os.makedirs('cache')

#         compressed_str = zlib.compress(data.encode('utf-8'))
#         compressed_str = compressed_str[:15].decode('utf-8')
#         operator_name = client.__class__.__name__

#         cache_dir = shuttle.cache.cache_dir
#         cache_path = '{}/cache/{}-{}-{}.txt'.format(cache_dir,shuttle.name,operator_name,encoded_str)
#         shuttle.cache.cache_path  = cache_path

#         with open(cache_path,'w+') as f:
#             f.write(data)

#     shuttle.name = '-'.join([shuttle.name,
#                 client.__class__.__name__])

#     if shuttle.cache.mem:
#         shuttle.mem = data

#     return shuttle