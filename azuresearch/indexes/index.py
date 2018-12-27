import json

from .field import Field
from azuresearch.connection import Endpoint
from azuresearch.document import Documents


class Index(object):
    endpoint = Endpoint("indexes")
    results = None

    def __init__(self, name, fields=None, suggesters=None, analyzers=None, synonym_maps=None):
        if analyzers is None:
            analyzers = []
        if suggesters is None:
            suggesters = []
        if fields is None:
            fields = []
        if synonym_maps is None:
            synonym_maps = []

        self.name = name
        self.fields = fields
        self.suggesters = suggesters
        self.analyzers = analyzers
        self.synonym_maps = synonym_maps

        for f in self.fields:
            f.index_name = self.name
        self.documents = Documents(self)

    def __repr__(self):
        return "<AzureIndex: {name}>".format(
            name=self.name
        )

    def to_dict(self):
        return {
            "name": self.name,
            "index_name": self.index_name,
            "fields": [field.to_dict() for field in self.fields],
            "scoringProfiles": [],
            "defaultScoringProfile": self.default_scoring_profile,
            "corsOptions": self.cors_options,
            "suggesters": self.suggesters,
            "analyzers": self.analyzers,
            "tokenizers": self.tokenizers,
            "tokenFilters": self.token_filters,
            "charFilters": self.char_filters
            #  "suggesters": [
            #   {
            #   "name": "sg",
            #   "searchMode": "analyzingInfixMatching",
            #   "sourceFields": ["hotelName"]
            #   }
            #  ],
            #  "analyzers": [
            #   {
            #   "name": "tagsAnalyzer",
            #   "@odata.type": "#Microsoft.Azure.Search.CustomAnalyzer",
            #   "charFilters": [ "html_strip" ],
            #   "tokenizer": "standard_v2"
            #   }
            #  ]
        }

    @classmethod
    def load(cls, data):
        if type(data) is str:
            data = json.loads(data)
        if type(data) is not dict:
            raise Exception  # TODO: Exception here
        return cls(name=data['name'], fields=[Field.load(f) for f in data['fields']])

    def create(self):
        return self.endpoint.post(self.to_dict(), needs_admin=True)

    def update(self):
        self.delete()
        return self.create()

    def delete(self):
        return self.endpoint.delete(endpoint=self.name, needs_admin=True)

    @classmethod
    def list(cls):
        return cls.endpoint.get(needs_admin=True)

    def search(self, query):
        query = {
            "search": query,
            "queryType": "full",
            "searchMode": "all"
        }
        self.results = self.endpoint.post(query, endpoint=self.name + "/docs/search")
        return self.results

    def statistics(self):
        response = self.endpoint.get(endpoint=self.name + "/stats", needs_admin=True)
        if response.status_code == 200:
            self.recent_stats = response.json()
            return self.recent_stats
        else:
            return response

    def count(self):
        # https://docs.microsoft.com/en-us/rest/api/searchservice/count-documents
        response = self.endpoint.get(endpoint=self.name + "/docs/$count", needs_admin=True)
        if response.status_code == 200:
            response.encoding = "utf-8-sig"
            self.recent_count = int(response.text)
            return self.recent_count
        else:
            return response
