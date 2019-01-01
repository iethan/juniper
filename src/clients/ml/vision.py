from ...abs.client_abc import ClientABC

from ...utils.adapters import append_client_to_name
from ...utils.adapters import save_to_file

import uuid

from PIL import Image

from google.cloud import vision
from google.cloud.vision import types
from google.api_core.exceptions import PermissionDenied

from pprint import pprint as p

import io
import os

__all__ = ["GoogleVisionClient"]

def object_localization(objects):

    data = []
    for object_ in objects:
        obj_data = {
            object_.name : {'confidence' : object_.score}
        }            
        for vertex in object_.bounding_poly.normalized_vertices:
            obj_data[object_.name].setdefault('vertices', []).append([vertex.x, vertex.y])
        data.append(obj_data)

    return data

parsers = {
    'object_localization' : object_localization
}


class GoogleVisionClient(ClientABC):

    def __init__(self,service_account):
        self.client = vision.ImageAnnotatorClient()\
                    .from_service_account_json(service_account)

    REPORTS = {'object_localization' : lambda client, image: client.object_localization(
        image=image).localized_object_annotations
        }

    def get_response(self, file_path, report_type):

        try:
            with io.open(file_path, 'rb') as image_file:
                content = image_file.read()
            image = vision.types.Image(content=content)
        except:
            try:
                image = vision.types.Image()
                image.source.image_uri = self.file_path
            except PermissionDenied:
                raise PermissionDenied("Ensure Vision API is enabled")
        
        objects = self.REPORTS[report_type](self.client,image)

        return parsers[report_type](objects)


    def read(self, shuttle, report_type, gcs_file_path=None):

        shuttle.client = self

        shuttle.name = append_client_to_name(shuttle=shuttle)

        if gcs_file_path: #in the cloud
            shuttle.data = self.get_response(file_path=gcs_file_path, report_type=report_type)
        else: #using image obj
            tmp_file = '{}/{}.jpg'.format(shuttle.staging_path, uuid.uuid4().hex)
            save_to_file(data=shuttle.data,file_path=tmp_file)
            shuttle.data = self.get_response(file_path=tmp_file, report_type=report_type)
            os.remove(tmp_file)

        return shuttle

    def write(self,shuttle):
        raise NotImplementedError('Cannot write to the Google VisionAPI')

    def delete(self,shuttle):
        raise NotImplementedError('Cannot delete on the Google VisionAPI')

    def edit(self,shuttle):
        raise NotImplementedError('Cannot edit the Google VisionAPI')        

    def merge(self,shuttle):
        raise NotImplementedError('Cannot merge on the Google VisionAPI')