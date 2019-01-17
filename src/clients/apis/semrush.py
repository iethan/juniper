from ...abs.client_abc import ClientABC

from ...utils.adapters import append_client_to_name
from ...utils.adapters import save_to_file

from ...utils.converters import byte_converters

from urllib.parse import urlparse
from urllib.parse import parse_qs
from urllib.parse import quote
from urllib.parse import unquote

from collections import namedtuple
import operator
import json

from pprint import pprint as p

import requests

__all__ = ["SEMRushClient"]


COLUMN_MAP = {'domain_organic':'Ph,Po,Pp,Nq,Kd,Cp,Ur,Tr,Tc,Co,Nr,Td,Ts',
              'domain_adwords':'Tt,Ds,Ph,Po,Pp,Nq,Cp,Vu,Ur,Tr,Tc,Co,Nr,Td,Ts,Kd'
}

REPORT_MAP = {'organic':'domain_organic',
              'adwords': 'domain_adwords'
}

parsers = {
    dict : None
}

REQUEST_DEFAULT_FIELDS = {
    'domain' : None,
    'database' : 'us',
    'device' : 'desktop',
    'type' : 'domain_organic',
    'display_filter' : '',
    'display_limit' : 10,
    'key' : None,
    'export_columns' : None,
}

REQUEST_FIELDS = tuple(REQUEST_DEFAULT_FIELDS.keys())

REQUEST_FIELD_DEFAULTS = tuple(REQUEST_DEFAULT_FIELDS.values())

SEMRushRequest = namedtuple('SEMRushRequest',REQUEST_FIELDS)
SEMRushRequest.__new__.__defaults__ = REQUEST_FIELD_DEFAULTS

class SEMRushClient(ClientABC):
    
    BASE_URL = 'https://api.semrush.com/'

    def __init__(self,api_key,display_limit=10):
        self.api_key = api_key
        self.display_limit = display_limit or 10

    def read(self, shuttle):

        shuttle.client = self
        shuttle.name = append_client_to_name(shuttle)

        params = shuttle.meta

        self.display_limit = params.get('display_limit',10)                

        semrush_url = params['report_url']

        if semrush_url:
            request_params = SEMRushURLAdapter(semrush_url=semrush_url, 
                        display_limit=self.display_limit).parse()
            request_params.update({'key' : self.api_key})

        request_params = SEMRushRequest(**request_params)

        request_params = request_params._replace(export_columns=COLUMN_MAP[request_params.type])
        request_params = request_params._replace(key=self.api_key)

        display_filter = request_params.display_filter
        if display_filter:
            request_params._replace(display_filter=unquote(display_filter))

        req = requests.get(self.BASE_URL,request_params._asdict())  

        param_dict = request_params._asdict()
        param_dict.pop('key')
        param_dict.update({'mime_type' : 'txt'}) #will always be text

        shuttle.meta = param_dict
        shuttle.data = req.text
        
        return shuttle

    def write(self, shuttle): 
        raise NotImplementedError('Cannot write to the SEMRush API')

    def delete(self, shuttle): 
        raise NotImplementedError('Cannot delete on the SEMRush API')

    def merge(self, shuttle): 
        raise NotImplementedError('Cannot merge on the SEMRush API')

class UndefinedReport(Exception):
    pass

class DisplayFilterParseError(Exception):
    pass



class SEMRushURLAdapter:

    DICT_MAP = {
        '>':'Gt',
        '=':'Eq',
        '<':'Lt',
        'containing':'Co',
        'wordMatch':'Wm',
        'exactMatch':'Eq',
        'begins':'Bw',
        'ends':'Ew',
        'phr': 'Ph', #keyword
        'pos': 'Po', #position
        'vol': 'Nq', #volume
        'cpc': 'Cp', #cpc
        'url': 'Ur', #url
        'tf': 'Tr', #traffic
        'tfc': 'Tc', #costs
        'com': 'Co', #competitive density
        'kd': 'Kd', #keyword difficulty
        'res': 'Nr', #number of results        

    }

    #params not API doesn't support: keyword type, categories, serp features, word count, last updated

    def __init__(self,semrush_url, display_limit):
        self._semrush_url = semrush_url
        self._display_limit = display_limit
    

    @property
    def semrush_url(self,):
        """SEMRush URL"""        
        return self._semrush_url

    @property
    def display_limit(self,):
        """Number of results"""
        return self._display_limit
 
    @staticmethod
    def _make_filter(*args):
        """Ensures all fields are strings with no white spaces and joined by '|'
        
        Example:
        >>> SEMRushURLAdapter._make_filter(1,2,' hi')
        1|2|hi
        """
        convert_to_string = [str(field).strip() for field in args]
        return '|'.join(convert_to_string)

    @staticmethod
    def _parse_one_filter(filters):               
        """Converts the URL string to API format. Will pass if 'fld' and 'cri'
        are not present, which typically happens with unsupported filters.

        Params:
        :param filters: dict of the filter data

        Example:
        >>> filters = {'inc': True, 'fld': 'phr', 'cri': 'containing', 'val': 'bhhs firefly'}
        >>> SEMRushURLAdapter._parse_one_filter(filters=filters)
        +|Ph|Co|bhhs firefly
        """

        field = filters.get('fld')
        criteria = filters.get('cri')
        
        if field and criteria:                
            try:
                return SEMRushURLAdapter._make_filter('+' if filters.get('inc') else '-',
                                            SEMRushURLAdapter.DICT_MAP[field],
                                            SEMRushURLAdapter.DICT_MAP[criteria],
                                            filters['val'])        
            except KeyError as e:                
                print('The filter key is not in the static SEMRushURLAdapter class dictionary: {}'.format(e))
                return

    @staticmethod   
    def _get_report(parsed_url_path):
        """Parses the report name from the path
        Params:
        :param parsed_url_path: url path with the report name in it

        Example
        >>> SEMRushURLAdapter._get_report('/analytics/organic/positions/')
        organic

        Raises
        UndefinedReport: if the URL is not the correct length or the 
        report is not in the REPORT_MAP dictionary in settings
        """

        try:
            report = parsed_url_path.split('/')[2]   
            return REPORT_MAP[report]     
        except Exception as e:
            raise UndefinedReport('Error in report URL: {}'.format(e))

    @staticmethod
    def _parse_filters(display_filter):
        """Parses list of dictionaries in the filter
        Params
        :param display_filter: the dict list in the URL

        Example:
        >>> display_filter = ['{"search":"bhhs firefly","advanced":{"0":{"inc":true,"fld":"phr","cri":"containing","val":"bhhs firefly"},"1":{"inc":true,"fld":"url","cri":"containing","val":"firefly"}}}']
        >>> SEMRushURLAdapter._get_report(display_filter=display_filter)
        +|Ph|Co|bhhs firefly|+|Ur|Co|firefly
        """
        try:
            if display_filter:                       
                filter_dict = json.loads(display_filter[0]).get('advanced') #get dict data to process         
                parsed_filter = [SEMRushURLAdapter._parse_one_filter(filters)  
                                        for _, filters in filter_dict.items()] #parse each filter
                remove_empty_filters = list(filter(None, parsed_filter)) #remove null filters                           
                return '|'.join(remove_empty_filters) #join the filter
        except Exception as e:
            raise DisplayFilterParseError('Error in parsing filter: {}'.format(e))
            
    def parse(self):
        """Provides the meta data required to make an API request
        """

        parsed_url = urlparse(self.semrush_url)            

        query = parse_qs(parsed_url.query)
        
        display_filter = SEMRushURLAdapter._parse_filters(display_filter=query.get('filter'))

        return {
            'domain' : query.get('q')[0],
            'database' : query.get('db',['us'])[0],
            'device' :  query.get('device',['desktop'])[0],
            'type' :  SEMRushURLAdapter._get_report(parsed_url.path),
            'display_filter' : quote(display_filter) if display_filter else '',
            'display_limit' : str(self.display_limit),
        }
