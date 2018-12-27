import json

from azuresearch.document import Documents
from azuresearch.service import Endpoint
from .field import Field


class Index(object):
    endpoint = Endpoint("indexes")
    results = None

    def __init__(self,
                 name,
                 fields,
                 suggesters=None,
                 analyzers=None,
                 char_filters=None,
                 tokenizers=None,
                 token_filters=None,
                 scoring_profiles=None,
                 default_scoring_profile=None,
                 cors_options=None
                 ):
        if analyzers is None:
            analyzers = []
        if suggesters is None:
            suggesters = []
        if scoring_profiles is None:
            scoring_profiles = []
        if tokenizers is None:
            tokenizers = []
        if token_filters is None:
            token_filters = []
        if char_filters is None:
            char_filters = []

        self.name = name
        self.fields = fields
        self.suggesters = suggesters
        self.analyzers = analyzers
        self.scoring_profiles = scoring_profiles
        self.tokenizers = tokenizers
        self.token_filters = token_filters
        self.char_filters = char_filters
        self.default_scoring_profile = default_scoring_profile
        self.cors_options = cors_options

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
            "fields": [field.to_dict() for field in self.fields],
            "scoringProfiles": [sp.to_dict() for sp in self.scoring_profiles],
            "corsOptions": self.cors_options,
            "suggesters": self.suggesters,
            "analyzers": self.analyzers,
            "tokenizers": self.tokenizers,
            "tokenFilters": self.token_filters,
            "charFilters": self.char_filters,
            "defaultScoringProfile": self.default_scoring_profile
        }

    @classmethod
    def load(cls, data):
        if type(data) is str:
            data = json.loads(data)
        if type(data) is not dict:
            raise Exception("Failed to parse input as Dict")

        if data['suggesters'] is None:
            data['suggesters'] = []
        if data['analyzers'] is None:
            data['analyzers'] = []
        if data['scoringProfiles'] is None:
            data['scoringProfiles'] = []
        if data['tokenizers'] is None:
            data['tokenizers'] = []
        if data['tokenFilters'] is None:
            data['tokenFilters'] = []
        if data['charFilters'] is None:
            data['charFilters'] = []
        if data['corsOptions'] is None:
            data['corsOptions'] = None
        if data['defaultScoringProfile'] is None:
            data['defaultScoringProfile'] = None

        return cls(name=data['name'],
                   fields=[Field.load(f) for f in data['fields']],
                   scoring_profiles=data['scoringProfiles'],
                   suggesters=data['suggesters'],
                   analyzers=data['analyzers'],
                   char_filters=data['char_filters'],
                   tokenizers=data['tokenizers'],
                   token_filters=data['tokenFilters'],
                   cors_options=data['corsOptions'],
                   default_scoring_profile=data['defaultScoringProfile']
                   )

    def create(self):
        return self.endpoint.post(self.to_dict(), needs_admin=True)

    def update(self):
        self.delete()
        return self.create()

    def get(self):
        return self.endpoint.get(endpoint=self.name, needs_admin=True)

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
