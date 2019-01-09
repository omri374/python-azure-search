import json

from azuresearch.base_api_call import BaseApiCall
from azuresearch.document import Documents
from .field import Field


class Index(BaseApiCall):
    results = None

    def __init__(self,
                 name,
                 fields=None,
                 suggesters=None,
                 analyzers=None,
                 char_filters=None,
                 tokenizers=None,
                 token_filters=None,
                 scoring_profiles=None,
                 default_scoring_profile=None,
                 cors_options=None, **params
                 ):
        super(Index, self).__init__("indexes")
        if fields is None:
            fields = []
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
        if params:
            self.params = params['kwargs']
        else:
            self.params = {}

        for f in self.fields:
            f.index_name = self.name

        self.documents = Documents(self)

    def __repr__(self):
        return "<AzureIndex: \n" \
               "index name: {name}\n" \
               "fields: {fields}\n" \
               "scoringProfiles: {scoringProfiles}\n" \
               "corsOptions: {corsOptions}\n" \
               "suggesters: {suggesters}\n" \
               "analyzers: {analyzers}\n" \
               "tokenizers: {tokenizers}\n" \
               "tokenFilters: {tokenFilters}\n" \
               "charFilters: {charFilters}\n" \
               "defaultScoringProfile: {defaultScoringProfile}>" \
            .format(name=self.name,
                    fields="\n".join(str(field) for field in self.fields),
                    scoringProfiles=[sp for sp in self.scoring_profiles],
                    corsOptions=self.cors_options,
                    suggesters=[sg for sg in self.suggesters],
                    analyzers=[an for an in self.analyzers],
                    tokenizers=[tk for tk in self.tokenizers],
                    tokenFilters=[tkf for tkf in self.token_filters],
                    charFilters=[chf for chf in self.char_filters],
                    defaultScoringProfile=self.default_scoring_profile)

    def to_dict(self):
        dict = {
            "name": self.name,
            "fields": [field.to_dict() for field in self.fields],
            "scoringProfiles": [sp.to_dict() for sp in self.scoring_profiles],
            "corsOptions": self.cors_options,
            "suggesters": [sg.to_dict() for sg in self.suggesters],
            "analyzers": [an.to_dict() for an in self.analyzers],
            "tokenizers": [tk.to_dict() for tk in self.tokenizers],
            "tokenFilters": [tkf.to_dict() for tkf in self.token_filters],
            "charFilters": [cf.to_dict() for cf in self.char_filters],
            "defaultScoringProfile": self.default_scoring_profile
        }
        # Add additional arguments
        dict.update(self.params)

        # Remove None values and empty lists
        dict = Index.remove_empty_values(dict)
        return dict

    @classmethod
    def load(cls, data):
        from .suggester import Suggester
        from azuresearch.analyzers.custom_analyzer import CustomAnalyzer
        from azuresearch.indexes import ScoringProfile

        if type(data) is str:
            data = json.loads(data)
        if type(data) is not dict:
            raise Exception("Failed to parse input as Dict")

        if 'suggesters' not in data:
            data['suggesters'] = []
        else:
            data['suggesters'] = [Suggester.load(sg) for sg in data['suggesters']]
        if 'analyzers' not in data:
            data['analyzers'] = []
        else:
            data['analyzers'] = [CustomAnalyzer.load(sg) for sg in data['analyzers']]
        if 'scoringProfiles' not in data:
            data['scoringProfiles'] = []
        else:
            data['scoringProfiles'] = [ScoringProfile.load(sp) for sp in data['scoringProfiles']]
        if 'tokenizers' not in data:
            data['tokenizers'] = []
        if 'tokenFilters' not in data:
            data['tokenFilters'] = []
        if 'charFilters' not in data:
            data['charFilters'] = []
        if 'corsOptions' not in data:
            data['corsOptions'] = None
        if 'defaultScoringProfile' not in data:
            data['defaultScoringProfile'] = None

        return cls(name=data['name'],
                   fields=[Field.load(f) for f in data['fields']],
                   scoring_profiles=data['scoringProfiles'],
                   suggesters=data['suggesters'],
                   analyzers=data['analyzers'],
                   char_filters=data['charFilters'],
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

    def verify(self):
        return self.get()

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
