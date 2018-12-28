# Juniper

Juniper is a lightweight ETL service that borrows from
several visual / coding elements of Apache Beam to 
reduce small but long, verbose ETL jobs.

## Install
### Virtualenv for Python3 on Mac / Linux

```
pip3 install virtualenv
python3 virtualenv env
source env/bin/activate
```

### Installing Juniper

```
pip3 install git+https://github.com/iethan/juniper.git
```

## What it can do
- Light transformations
### Functionality
- Storage: Google Cloud Storage, LocalFileSystem, 
    Text(in memory)
- Camera: PiCamera
- Operators: Read, Write, Delete, Edit
- Utils: MockIter

## What it cannot do
- It's not an Apache Beam replacement
- It's limited to the scope of your computer memory
- It's not distributed

## Example Recipes

```
Juniper() >> (
            # take a picture with PiCamera*
            Write(CameraClient,file_path='old_image.jpg')  
            
            # write the file to Cloud Storage
            + Write(StorageClient,bucket_name='hi-12394',
                            service_account=SERVICE_ACCOUNT,
                            blob_name='old_image.jpg',
                            file_path='old_image.jpg',
            )

            # read the saved local file into memory
            + Read(LocalFileSystem,file_path='old_image.jpg')

            # crop the image
            + Edit(ImageClient,file_path='old_image.jpg',
                                crop_box=(1,1,200,200))

            # write the new image to the local file system**
            + Write(LocalFileSystem,file_path='new_image-2.jpg')

            # upload the new image to Google Cloud Storage      
            + Write(StorageClient,bucket_name='hi-12394',
                            service_account=SERVICE_ACCOUNT,
                            blob_name='new_image-2.jpg',
                            file_path='new_image-2.jpg',
            )
)
```
*If PiCamera is not installed locally, a mock is instatiated. This 
can help with testing on systems without PiCamera installed.

**The Edit operatator does not automatically save the file locally,
instead, it saves it into memory and can be used to save. This enables
multiple edits on the same image. To upload the edited image, you must
first save it.

# TODO
- Merge operator
- Logging
- Factory operators and clients for bulk processing
- Caching