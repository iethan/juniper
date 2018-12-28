from ..abs.client_abc import ClientABC
from ..utils.adapters import ShuttleAdapter
from ..utils.adapters import convert_to_string
from google.cloud import storage

import json
import os

class Bucket:
    def __init__(self,service_account=None,bucket_name=None,service=None):
        self._bucket_name = bucket_name
        self._service_account = service_account
        self._service = service or storage.Client()\
                .from_service_account_json(self.service_account)        
 
    def __repr__(self,):
        return 'Project: {service.project}, Bucket: {bucket.name}'.format(
                        service=self.service,bucket=self.bucket_instance)

    @property
    def service_account(self,):
        return self._service_account

    @property
    def bucket_name(self,):
        if self._bucket_name:
            return self._bucket_name
        else:
            return self.bucket_instance.name

    @property
    def service(self,):       
        return self._service

    @property
    def bucket_instance(self,):       
        if not self.service.lookup_bucket(self.bucket_name):
            self.service.create_bucket(self.bucket_name)
            bucket = self.service.get_bucket(self.bucket_name)
            bucket.storage_class = 'REGIONAL'
        return self.service.get_bucket(self.bucket_name)
        

    def delete(self,):
        return self.bucket_instance.delete(force=True)
    
    def create(self,):
        return self.bucket_instance

class File:

    MIME_TYPES = {
        'json' : 'application/json',
        'csv' : 'text/csv',
        'txt' : 'text/plain',
        'png' : 'image/png',
        'jpg' : 'image/jpeg'
    }
    def __init__(self,bucket,blob_name):
        self._bucket = bucket
        self._blob_name = blob_name
        self._blob = None

    @property
    def blob_name(self,):
        return self._blob_name  

    @property
    def bucket(self,):
        return self._bucket 

    @property
    def blob_path(self):
        return "gs://{}/{}".format(self.bucket.name,self.blob_name)

    @property
    def blob(self,):
        return self._blob
    
    @blob.setter
    def blob(self,value):
        self._blob = value
        return value

    @property
    def exists(self,):
        return self.bucket.blob(self.blob_name).exists()      

    def get_blob(self,):
        blob = self.bucket.blob(self.blob_name)
        self.blob = blob
        return blob

    def read(self,file_path=None):

        if file_path:
            self.bucket.blob(self.blob_name)\
                .download_to_filename(file_path)
            return
        else:
            data = self.bucket.blob(self.blob_name)\
                .download_as_string()
            return data.decode('utf-8')

    def write(self, data=None, content_type='txt',file_path=None):
        
        try:
            data = convert_to_string(data)
            self.bucket.blob(self.blob_name)\
                .upload_from_string(data,File.MIME_TYPES[content_type])            
        except:
            pass
        if file_path:
            head,tail = os.path.splitext(file_path)
            tail = tail.replace('.','')
            self.bucket.blob(self.blob_name)\
                .upload_from_filename(file_path,File.MIME_TYPES[tail])
        
        return self.get_blob()

    def delete(self,):  
        return self.bucket.delete_blob(self.blob_name)

class StorageClient(ClientABC):

    def __init__(self,bucket_name,service_account,blob_name=None,file_path=None,content_type='txt'): 
        self._file_path = file_path
        self._bucket_name = bucket_name
        self._content_type = content_type
        self._blob_name = blob_name
        self._service_account = service_account
        self._service = storage.Client()\
                .from_service_account_json(self.service_account)        

    @property
    def file_path(self,):
        return self._file_path

    @property
    def blob_name(self,):
        return self._blob_name

    @property
    def content_type(self,):
        return self._content_type

    @property
    def service_account(self,):
        return self._service_account

    @property
    def service(self,):
        return self._service

    @property
    def bucket_name(self,):
        return self._bucket_name

    @property
    def bucket(self,):        
        return Bucket(bucket_name=self.bucket_name, 
                service_account=self.service_account)

    @bucket.setter
    def bucket(self,bucket_name):
        return Bucket(bucket_name=bucket_name, 
                service_account=self.service_account)

    @property
    def bucket_instance(self,):
        return self.bucket.bucket_instance

    def read(self,shuttle):

        shuttle.client = self

        shuttle = ShuttleAdapter(shuttle=shuttle).shuttle

        f = File(bucket=self.bucket_instance,
                 blob_name=self.blob_name)

        shuttle.data = f.read(file_path=self.file_path)
        shuttle.write_path = f.blob_path
        
        return shuttle

    def write(self, shuttle):

        shuttle.client = self
        
        shuttle = ShuttleAdapter(shuttle=shuttle).shuttle

        f = File(bucket=self.bucket_instance,
                                    blob_name=self.blob_name)
        f.write(data=shuttle.data, content_type=self.content_type,
                                        file_path=self.file_path)
        
        shuttle.write_path = f.blob_path

        return shuttle

    def delete(self,shuttle):
        # blob_name=None,bucket=None
        shuttle.client = self
        
        shuttle = ShuttleAdapter(shuttle=shuttle).shuttle

        if self.blob_name:
            f = File(bucket=self.bucket_instance,blob_name=self.blob_name)            
            f.delete()
            shuttle.write_path = f.blob_path
        else:
            self.bucket.delete()
        
        return shuttle
        


    def merge(self,new_file_name,prefix=None):

        blobs = self.bucket_instance.list_blobs(prefix=prefix)
        self.bucket_instance.blob(new_file_name).compose(blobs)

        f = File(bucket=self.bucket_instance,blob_name=new_file_name)

        return f.get_blob()