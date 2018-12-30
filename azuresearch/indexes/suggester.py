from azuresearch.service import Endpoint


class Suggester(object):
    endpoint = Endpoint("index")

    def __init__(self, name, source_fields, search_mode="analyzingInfixMatching"):
        self.name = name
        self.source_fields = source_fields
        self.search_mode = search_mode

    def __repr__(self):
        return "<Suggester: {name}>".format(
            name=self.name
        )

    def to_dict(self):
        return {
            "name": self.name,
            "sourceFields": [field for field in self.source_fields],
            "searchMode": self.search_mode
        }

    def suggest(self, query, extra=None):
        query = {
            "search": query,
            "queryType": "full",
            "searchMode": "analyzingInfixMatching"
        }
        self.results = self.endpoint.post(query, endpoint=self.name + "/docs/suggest")
        return self.results
