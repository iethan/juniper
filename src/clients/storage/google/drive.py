from apiclient import errors
import io
import os
import re
import json
import uuid 

from pprint import pprint as p

from googleapiclient.discovery import build
from google.oauth2 import service_account
from apiclient import http

from time import sleep

from ....abs.client_abc import ClientABC
from ....utils.adapters import append_client_to_name
from ....utils.adapters import save_to_file
from ....utils.adapters import read_from_file

def build_service(SERVICE_ACCOUNT):
    SCOPES = ['https://www.googleapis.com/auth/drive'] 
    credentials = service_account.Credentials \
        .from_service_account_file(SERVICE_ACCOUNT, 
                                    scopes=SCOPES)

    return build('drive', 'v3', credentials=credentials,
                                cache_discovery=False)


class Query:
    def __init__(self, service_account=None, service=None, query=None, http=None):
        self.service = service if service else build_service(service_account)
        self.http = http or {} 
        self.query = query
        self.result = self.service.files().list(q=self.query or None)\
                                .execute(http=self.http.get('result')) 

    @property
    def files(self):          
        return [file for file in self.result.get('files',[])]    

    @property
    def ids(self):
        return [file.get('id') for file in self.files]

    @property
    def names(self):
        return [file.get('name') for file in self.files]

    def get_file_info(self,file_id):
        return self.service.files().get(fileId=file_id,
                    fields='name,id,parents').execute()

    def get_parents(self,file_id):
        parents = []
        for parent in self.get_file_info(file_id).get('parents',[]):
            parents.append(self.get_file_info(parent))
        return parents
            
    @property
    def parents(self):
        files = []
        for file in self.files:
            file.update(
                {
                    'parent_info': 
                    self.get_parents(file['id'])
                })
            files.append(file)

        return files
                                                            
 

class File:

    MEME_TYPES = {
        'txt' : {
            'drive' : 'text/plain',#application/vnd.google-apps.document',
            'mime' : 'text/plain'
        },                
        'csv' : {
            'drive' : 'text/csv',#'application/vnd.google-apps.spreadsheet',
            'mime' : 'text/csv'
        },
        'json' : {
            'drive' : 'application/json',
            'mime' : 'application/json'
        },
        'png' : {
            'drive' : 'image/png',
            'mime' : 'application/vnd.google-apps.photo'
        },
        'jpg' : {
            'drive' : 'image/jpeg',
            'mime' : 'application/vnd.google-apps.photo'
        }
    }

    def __init__(self,file_name,mime_type,service_account=None,service=None,parent_id=None,http=None):
        self.service = service if service else build_service(service_account)
        self.http = http or {}                
        self.parent_id = parent_id
        self.__file_name = file_name
        self.mime_type = mime_type or 'txt'
        self.__query = self.query()   
    
    @property
    def data(self,):
        return self.__data

    @data.setter
    def data(self,value):        
        self.__data = str(value)

    @property
    def file_name(self,):              
        # return re.sub(r'\..*',f'.{self.mime_type}',
        #                 self.__file_name)        
        return self.__file_name
    
    def query(self):
        query = "name = '{}'".format(self.file_name)
        if self.parent_id:
            query += " and parents in '{}'".format(self.parent_id)
        return Query(query=query,service=self.service,http={'result' :self.http.get('query')})        

    @property
    def ids(self):    
        return self.__query.ids
   
    @ids.setter
    def ids(self,value):
        self.__ids = value

    @property
    def names(self):
        return self.__query.names
   
    @names.setter
    def names(self,value):
        self.__names = value
        
    def delete(self,):
        ids = self.ids
        names = self.names
        self.service.files().delete(fileId=ids[0]).execute(http=self.http.get('delete'))        
        return {
                'id' : ids[0],
                'name' : names[0],
                'status' : 'deleted'            
        }
        
    def write(self,file_path):        
        
        drive_mime = File.MEME_TYPES[self.mime_type]['drive']
        file_mime = File.MEME_TYPES[self.mime_type]['mime']


        file_service = self.service.files()        

        file_metadata = {
            'name': self.file_name,
            'mimeType': drive_mime,            
        }                                  

        media = http.MediaFileUpload(file_path, mimetype=file_mime,
                    chunksize=1024*1024, resumable=True)        
        
        #update
        if self.ids:
            file_service.update(fileId=self.ids[0],
                                body=file_metadata,                                
                                media_body=media).execute(http=self.http.get('update'))                        
            return {
                    'id' : self.ids[0],
                    'name' :self.names[0],
                    'status' : 'updated'
                }

        #create
        else:
            if self.parent_id:
                file_metadata.update(
                    {
                        'parents': [self.parent_id]
                    }
                )

            file_data = file_service.create(body=file_metadata,
                        media_body=media,
                        fields='name,id').execute(http=self.http.get('create'))
            self.ids = [file_data.get('id')]
            self.names = [file_data.get('name')]

            return {
                    'id' : file_data.get('id'),
                    'name' : file_data.get('name'),
                    'status' : 'created'

                }
            


class Folder:
    
    def __init__(self, folder_name, parent_id=None, service_account=None, service=None, http=None):
        self.service = service if service else build_service(service_account)
        self.folder_name = folder_name
        self.http = http or {}   
        self._ids = [] 
        self._names = []
        self._parents = []
        self._raw_query = "name = '{}' and '{}' in parents" if parent_id else "name = '{}'"
        self.query = Query(service=self.service, 
                    query=self._raw_query.format(self.folder_name,parent_id),
                    http={'result' :self.http.get('query')}) 

    @property
    def ids(self):
        return self.query.ids or self._ids

    @ids.setter
    def ids(self,value):
        self._ids = value

    @property
    def names(self):
        return self.query.names or self._names

    @names.setter
    def names(self,value):
        self._names = value

    @property
    def parents(self):
        return self.query.parents or self._parents

    @parents.setter
    def parents(self,value):
        self._parents = value

    def create(self,parent_folder_id=None,force=False):

        if self.ids:
            return self
        else:     
            file_metadata = {
            'name': self.folder_name,
            'mimeType': 'application/vnd.google-apps.folder',       
                }
            if parent_folder_id:
                file_metadata.update({'parents': [parent_folder_id]})

            folder_ids = self.service.files().create(
                body=file_metadata,fields='name,id,parents'
            ).execute(http=self.http.get('create'))  

            self.ids = [folder_ids.get('id')]
            self.names = [folder_ids.get('name')]  
            self.parents = [folder_ids.get('parents')]                 

            return self            

    def delete(self,):
        try:            
            self.service.files().delete(fileId= self.ids[0],
                        fields='id').execute(http=self.http.get('delete'))
                                                        
            return 'Deleted {}'.format(self.folder_name)
        except:
            return 'Not a valid delete for {}'.format(self.folder_name)


class Permissions:
    def __init__(self, object_id, collaborator_emails, service_account=None, service=None, http=None):
        self.service = service if service else build_service(service_account)
        self.object_id = object_id
        self.collaborator_emails = collaborator_emails
        self.http = http or {}
    
    def _grant_permission(self,email_address,notify):

        file_metadata = {
                "type": 'user',
                "emailAddress": email_address,
                "role": 'reader',
            }  
        response = self.service.permissions().create(body=file_metadata,
                    fileId=self.object_id,sendNotificationEmail=notify).\
                    execute(http=self.http.get('permission'))                                     
        return response           
        

    def create(self,notify=False):
        if self.collaborator_emails:
            return [self._grant_permission(email_address=email_address,notify=notify) \
                            for email_address in self.collaborator_emails]
        else:
            return 'No permissions to grant'
        
            


class DriveClient(ClientABC):

    def __init__(self, drive_name, service_account=None, service=None, collaborator_emails=None, folder_path=None):
    
        self.service = service if service else build_service(service_account)
                    
        self.collaborator_emails = collaborator_emails

        #create folders
        self.folder_path = folder_path
        self.drive_name = drive_name
        self.top_level_parent_id = None
        self.folder_info = []
        if folder_path:
            self.get_or_create_folders()

        #for testing
        self.http = {}  

    def merge(self,shuttle):
        raise NotImplementedError('Download file locally or into Cloud Storage')

    def get_or_create_folders(self):
        top_level_parent_id = self.create_master_folder()  
        self.create_sub_folders(top_level_parent_id)


    def create_master_folder(self,):
        master_folder = self.folder_path[0]
        master_parents = Query(service=self.service,
                        query="name = '{}'".format(master_folder)).parents

        top_level_parent_id = None

        #file doesn't exist
        if not master_parents:
            f = Folder(service=self.service, folder_name=master_folder)
            f.create()
            top_level_parent_id = f.ids[0]

        #file exists and need to get top parent or create
        for parents in master_parents:
            for parent in parents['parent_info']:
                
                #if parent exists at top level
                if parent['name'] == self.drive_name:
                    top_level_parent_id = parents['id']
                
                #parent doesn't exist at top level but child of another parent
                else:
                    f = Folder(service=self.service, folder_name=master_folder)
                    f.create(force=True)
                    top_level_parent_id = f.ids[0]
    
        perm = Permissions(service=self.service, object_id=top_level_parent_id,
                    collaborator_emails=self.collaborator_emails)
        perm.create(notify=False)
        
        self.folder_info.append(top_level_parent_id)

        return top_level_parent_id

    def create_sub_folders(self,top_level_parent_id):
        #create subfolders
        sub_folders = self.folder_path[1:]      

        parent_id = top_level_parent_id
        for sub_folder in sub_folders:
            f = Folder(service=self.service, parent_id=parent_id, folder_name=sub_folder)
            f.create(parent_folder_id=parent_id)
            parent_id = f.ids[0]
            self.folder_info.append(parent_id)

    def query(self, shuttle, query=None, parents=False):

        result = Query(service=self.service,query=query)
        if parents:
            shuttle.data = result.parents
        else:
            shuttle.result = result.names
                
        return shuttle


    def write(self, shuttle, file_name, mime_type='txt', notify=False):

        shuttle.client = self
        shuttle.name = append_client_to_name(shuttle=shuttle) 

        tmp_file = '{}/{}-{}'.format(shuttle.staging_path,uuid.uuid4().hex,file_name)
        save_to_file(data=shuttle.data,file_path=tmp_file)

        try:
            parent_id = self.folder_info[-1]
        except:
            parent_id = None            

        f = File(service=self.service, file_name=file_name, 
                    parent_id=parent_id, mime_type=mime_type)
        
        f.write(file_path=tmp_file)

        os.remove(tmp_file)
        
        return shuttle


    def delete(self, shuttle, object_names=None):

        shuttle.client = self
        shuttle.name = append_client_to_name(shuttle=shuttle) 

        if object_names:
            for object_name in object_names:
                f = Folder(service=self.service, folder_name = object_name)
                f.delete()
        else:
            q = Query(service=self.service)
            [Folder(service=self.service, folder_name=object_name).delete() for object_name in q.names]

        return shuttle


    def read(self, shuttle, file_name, parent_name=None):
        shuttle.client = self
        shuttle.name = append_client_to_name(shuttle=shuttle) 

        tmp_file = '{}/{}-{}'.format(shuttle.staging_path,uuid.uuid4().hex,file_name)

        query = "name = '{}'".format(file_name)

        if parent_name:

            parent_ids = Query(service=self.service,
                        query="name = '{}'".format(parent_name)).ids
            
            file_id = None
            for parent_id in parent_ids:
                query += "and parents in {}".format(parent_id)

                try:
                    file_id = Query(service=self.service,
                                    query=query).ids[0]
                except:
                    pass
        else:
            file_id = Query(service=self.service,
                                query=query).ids[0]

        request = self.service.files().get_media(fileId=file_id)
        fh = io.FileIO(tmp_file, 'wb')
        media_request = http.MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = media_request.next_chunk()

        shuttle.data = read_from_file(tmp_file)

        return shuttle