"""
Juniper is a wrapper for I/O with Google Cloud. The Juniper 
context implements read, write, delete, merge strategies from
the API-specific clients.

Example usage:

Juniper() >> (
              Read(ImageClient, file_path='cow.jpg')
              + Write(LocalFileSystem, file_path='hi.jpg')
              + Write(StorageClient, bucket_name='hi-12394',
                              service_account=SERVICE_ACCOUNT,
                              blob_name='hi.jpg',
                              file_path='hi.jpg'
                              )

"""

from setuptools import setup 
import setuptools

setup(
    name='juniper', 
    version='1.0', 
    description='ETL manager', 
    author='Ethan Lyon', 
    author_email='ethanlyon@gmail.com',
    package_dir={'juniper':'src'},
    packages=['juniper','juniper.abs','juniper.clients',
              'juniper.operators','juniper.utils'
    ],
    
    ) 
__author__ = 'Ethan Lyon' 