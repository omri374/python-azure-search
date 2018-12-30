from azuresearch.service import Endpoint
from .abstract_analyzer import AbstractAnalyzer


class CustomAnalyzer(AbstractAnalyzer):
    __name__ = 'CustomAnalyzer'
    endpoint = Endpoint("indexes")

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
        return {
            "name": self.analyzer_name,
            "@odata.type": self.analyzer_type,
            "searchMode": self.search_mode
        }
