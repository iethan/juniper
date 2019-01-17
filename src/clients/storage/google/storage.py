from ....abs.client_abc import ClientABC

from google.cloud import storage

from ....utils.adapters import append_client_to_name
from ....utils.adapters import save_to_file
from ....utils.adapters import convert_to_string
from ....utils.adapters import read_from_file

from ....utils.converters import byte_converters

import uuid 
import json
import os

__all__ = ["CloudStorageClient"]

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

    def write(self, data, content_type='txt'):

        self.bucket.blob(self.blob_name)\
            .upload_from_string(data.read(),File.MIME_TYPES[content_type])            
        
        return self.get_blob()

    def delete(self,):  
        return self.bucket.delete_blob(self.blob_name)

class CloudStorageClient(ClientABC):

    def __init__(self,bucket_name,service_account): 
        self._bucket_name = bucket_name
        self._service_account = service_account
        self._service = storage.Client()\
                .from_service_account_json(self.service_account)        

    @property
    def blob_name(self,):
        return self._blob_name

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


    @property
    def bucket_instance(self,):
        return self.bucket.bucket_instance

    def read(self,shuttle,blob_name,content_type='txt'):

        shuttle.client = self
        shuttle.name = append_client_to_name(shuttle=shuttle)

        tmp_file = '{}/{}-{}'.format(shuttle.staging_path, uuid.uuid4().hex,blob_name)

        f = File(bucket=self.bucket_instance,
                 blob_name=blob_name)

        f.read(file_path=tmp_file) #saves file to staging
        shuttle.data = read_from_file(tmp_file) #stores on shuttle

        os.remove(tmp_file) #removes from staging
        
        return shuttle

    def write(self, shuttle):

        shuttle.client = self
        shuttle.name = append_client_to_name(shuttle=shuttle)

        blob_name = shuttle.meta['blob_name']
        content_type = shuttle.meta['content_type']

        f = File(bucket=self.bucket_instance,
                blob_name=blob_name)

        f.write(content_type=content_type,
                    data=shuttle.encoded_data)

        return shuttle

    def delete(self,shuttle,blob_name=None,bucket=False):

        shuttle.client = self
        shuttle.name = append_client_to_name(shuttle=shuttle)

        if blob_name:
            f = File(bucket=self.bucket_instance,blob_name=blob_name)            
            f.delete()
        elif bucket:
            self.bucket.delete()
        
        return shuttle

    def merge(self,shuttle, blob_name ,prefix=None):

        shuttle.client = self
        shuttle.name = append_client_to_name(shuttle=shuttle)

        tmp_file = '{}/{}-{}'.format(shuttle.staging_path,uuid.uuid4().hex,blob_name)

        blobs = self.bucket_instance.list_blobs(prefix=prefix)
        self.bucket_instance.blob(blob_name).compose(blobs)

        f = File(bucket=self.bucket_instance,blob_name=blob_name)

        f.read(file_path=tmp_file) #saves file to staging
        shuttle.data = read_from_file(tmp_file) #stores on shuttle

        os.remove(tmp_file) #removes from staging        

        return shuttle