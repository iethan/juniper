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

        shuttle,shuttle_data = shuttle, []

        options = self.kwargs.get('options')
        original_name = shuttle.name
        

        try:
            
            for option,data in zip(options,shuttle.data):
                print('aaaaaaaa')
                print('data')
                shuttle.data = data
                shuttle = self.operator(self.client,**option).execute(shuttle)
                shuttle_data.append(shuttle.data)

        except AttributeError as e: #data attribute is not present
            print('bbbbbbbb')
            for option in options:
                shuttle = self.operator(self.client,**option).execute(shuttle)
                shuttle_data.append(shuttle.data)

        except: #no options, only data given
            print('ccccccc')
            for data in shuttle.data:
                shuttle.data = data
                shuttle = self.operator(self.client).execute(shuttle)
                shuttle_data.append(shuttle.data)
        
        print(shuttle.data)
        shuttle.data = shuttle_data
        shuttle.name = '-'.join([original_name,
                                self.operator.__name__,
                                self.client.__class__.__name__])
        return shuttle