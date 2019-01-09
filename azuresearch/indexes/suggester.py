import json

from azuresearch.base_api_call import BaseApiCall


class Suggester(BaseApiCall):

    def __init__(self, name, source_fields, search_mode="analyzingInfixMatching"):
        super(Suggester, self).__init__("indexes")
        self.name = name
        self.source_fields = source_fields
        self.search_mode = search_mode

    def __repr__(self):
        return "<Suggester: {name}>".format(
            name=self.name
        )

    def to_dict(self):
        return_dict = {
            "name": self.name,
            "sourceFields": [field for field in self.source_fields],
            "searchMode": self.search_mode
        }

        # Remove None values
        return_dict = Suggester.remove_empty_values(return_dict)
        return return_dict

    @classmethod
    def load(cls, data):
        if type(data) is str:
            data = json.loads(data)
        if type(data) is not dict:
            raise Exception("Failed to parse input as Dict")
        if 'name' not in data:
            data['name'] = None
        if 'sourceFields' not in data:
            data['sourceFields'] = []
        if 'searchMode' not in data:
            data['searchMode'] = None
        return cls(name=data['name'], source_fields=data['sourceFields'], search_mode=data['searchMode'])

    def suggest(self, query, extra=None):
        query = {
            "search": query,
            "queryType": "full",
            "searchMode": "analyzingInfixMatching"
        }
        self.results = self.endpoint.post(query, endpoint=self.name + "/docs/suggest")
        return self.results
