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

### Enable Vision API

```
gcloud services enable vision.googleapis.com
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

## Operator and client lookup

|                    | Instantiation Parameters     | Return Values                 | Read           | Write         | Edit          | Delete        | Merge                 |
|--------------------|------------------------------|-------------------------------|----------------|---------------|---------------|---------------|-----------------------|
| LocalFileSystem    |           file_path          | str, dict, list, tuple, image |  ✔ - file_path | ✔ - file_path |       x       | ✔ - file_path |     ✔ - file_paths    |
| Text               |             data             | str, dict, list, tuple, image |     ✔ - n/a    |       x       | ✔ - exec_func |       x       |     ✔ - exec_func     |
| Image              |              n/a             |             Image             |        x       |       x       |  ✔ - crop_box |       x       |           x           |
| Camera             |             sleep            |             Image             |     ✔ - n/a    |       x       |       x       |       x       |           x           |
| GoogleCloudStorage | service_account, bucket_name | str, dict, list, tuple, image |  ✔ - blob_name | ✔ - blob_name |       x       | ✔ - blob_name | ✔ - prefix, blob_name |
| BigQuery           |             #TODO            |               --              |       --       |       --      |       --      |       --      |           --          |
| APIs               |        service_account       |              dict             | ✔ - api_params |       x       |       x       |       x       |           x           |

## Example Recipes

```
    #instantiate storage client for use in pipeline
    storage_client = StorageClient(service_account=SERVICE_ACCOUNT, 
                                    bucket_name='mweroisdf')


    Juniper(staging_path='staging') >> ( #you can change the staging path
                Read(LocalFileSystem(file_path='download.jpg'))
                + Read( #apply an operator to client
                    GoogleVisionClient( 
                        service_account=SERVICE_ACCOUNT),
                        report_type='object_localization'
                )
                + Write(storage_client,blob_name='results.json')
)
```

# TODO
- Merge operator
- Logging
- Factory operators and clients for bulk processing
- Caching