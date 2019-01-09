import json

from azuresearch.service import Endpoint
from .abstract_analyzer import AbstractAnalyzer


class CustomAnalyzer(AbstractAnalyzer):

    def __init__(self,
                 index_name,
                 analyzer_name,
                 analyzer_type="#Microsoft.Azure.Search.CustomAnalyzer",
                 char_filters=None,
                 tokenizer=None,
                 token_filters=None
                 ):
        super(CustomAnalyzer, self).__init__(index_name, analyzer_name, analyzer_type)

        self.tokenizer = tokenizer

        if char_filters is None:
            char_filters = []
        self.char_filters = char_filters

        if token_filters is None:
            token_filters = []
        self.token_filters = token_filters

    def to_dict(self):
        dict = {
            "name": self.analyzer_name,
            "@odata.type": self.analyzer_type,
            "searchMode": self.search_mode,
            "charFilters": self.char_filters,
            "tokenizer": self.tokenizer,
            "token_filters": self.token_filters
        }
        # Remove None values
        dict = CustomAnalyzer.remove_empty_values(dict)
        return dict

    @classmethod
    def load(cls, data):
        if type(data) is str:
            data = json.loads(data)
        if type(data) is not dict:
            raise Exception("Failed to parse input as Dict")

        if 'indexName' not in data:
            data['indexName'] = None
        if 'name' not in data:
            data['name'] = None
        if '@odata.type' not in data:
            data['@odata.type'] = None
        if 'charFilters' not in data:
            data['charFilters'] = []
        if 'tokenizer' not in data:
            data['tokenizer'] = None
        if 'token_filters' not in data:
            data['tokenFilters'] = []
        return cls(index_name=data['indexName'], analyzer_name=data['name'], analyzer_type=data['@odata.type'],
                   char_filters=data['charFilters'], token_filters=data['tokenFilters'], tokenizer=data['tokenizer'])
