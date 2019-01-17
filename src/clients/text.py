from ..abs.client_abc import ClientABC
from ..utils.adapters import ShuttleAdapter

from ..utils.adapters import convert_to_string
from ..utils.adapters import read_from_file
from ..utils.adapters import save_to_file
from ..utils.adapters import append_client_to_name

from ..utils.converters import byte_converters


__all__ = ["Text"]

class Text(ClientABC):

    def read(self,shuttle):

        shuttle.data = shuttle.meta.get('data')

        shuttle.client = self

        shuttle.name = append_client_to_name(shuttle=shuttle)

        return shuttle

    def edit(self,shuttle, exec_func, **kwargs):
        raise NotImplementedError('Use a transform client to edit data')

    def write(self,shuttle): 
        raise NotImplementedError('Use a storage client to write data')

    def delete(self,shuttle):
        raise NotImplementedError('Use a storage client to delete data')

    def merge(self, shuttle, data, exec_func):
        shuttle.client = self

        shuttle.data = exec_func(self.data)
        shuttle.name = append_client_to_name(shuttle=shuttle)

        return shuttle
