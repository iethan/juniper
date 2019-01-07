"""
Juniper is a wrapper for I/O with Google Cloud. The Juniper 
context implements read, write, delete, merge strategies from
the API-specific clients.

Example usage:

Juniper() >> (
              Read(LocalFileSystem(file_path='cow.jpg'))
              + Edit(ImageClient(), crop=(1,1,100,100))
              + Write(StorageClient(bucket_name='hi-12394',
                              service_account=SERVICE_ACCOUNT), 
                              blob_name='brown-cow.jpg',
                              )

"""

from setuptools import setup

setup(
    name='juniper', 
    version='1.0', 
    description='ETL manager', 
    author='Ethan Lyon', 
    author_email='ethanlyon@gmail.com',
    package_dir={'juniper':'src'},
    packages=[
              'juniper.abs','juniper.clients.storage',
              'juniper.clients.storage.google',
              'juniper.clients.apis',
              'juniper.operators','juniper.utils',
    ],
    install_requires=[
        'google-api-python-client>=1.6.5',
        'pillow>=5.3.0',
        'requests>=2.21.0',
        'google-cloud-vision>=0.35.0'
    ]
    
    ) 
__author__ = 'Ethan Lyon' 