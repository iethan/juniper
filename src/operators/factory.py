from ..abs.io_abc import IoABC

__all__ = ["Factory"]

class Factory(IoABC):
    def __init__(self,operator,client,**kwargs):
        self.operator = operator
        self.client = client
        self.kwargs = kwargs
        self.objs = [self]
    
    def __add__(self,obj):
        self.objs.append(obj)
        return self 

    def execute(self,shuttle):

        shuttle,shuttle_data,shuttle_meta = shuttle, [], []

        options = self.kwargs.get('options')
        original_name = shuttle.name
        
        if isinstance(shuttle.data,list) and isinstance(options,list):

            for option,data in zip(options,shuttle.data):
                
                shuttle.data = data
                shuttle = self.operator(self.client,**option).execute(shuttle)
                shuttle_data.append(shuttle.data)
                shuttle_meta.append(shuttle.meta)

        elif isinstance(options,list) and not isinstance(shuttle.data,list):

            for option in options:
                shuttle = self.operator(self.client,**option).execute(shuttle)
                shuttle_data.append(shuttle.data)
                shuttle_meta.append(shuttle.meta)

        elif not isinstance(options,list) and isinstance(shuttle.data,list):

            for data in shuttle.data:
                shuttle.data = data
                shuttle = self.operator(self.client).execute(shuttle)
                shuttle_data.append(shuttle.data)
                shuttle_meta.append(shuttle.meta)

        
        shuttle.data = shuttle_data
        shuttle.meta = shuttle_meta

        shuttle.name = '-'.join([original_name,
                                self.operator.__name__,
                                self.client.__class__.__name__])

        return shuttle