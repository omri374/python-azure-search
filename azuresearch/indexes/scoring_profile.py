import json
import warnings

from azuresearch.azure_search_object import AzureSearchObject


class ScoringProfile(AzureSearchObject):
    '''
    A scoring profile for an index. See this link for more information:
    taken from https://docs.microsoft.com/en-us/rest/api/searchservice/add-scoring-profiles-to-a-search-index
    '''

    def __init__(self, name, text=None, functions=None):

        if functions is None:
            functions = []

        self.name = name
        self.text = text
        self.functions = functions

    def __repr__(self):
        return "<{classname}: {name}>".format(
            classname=self.__name__, name=self.name
        )

    def to_dict(self):
        return_dict = {
            "name": self.name,
            "text": self.text,
            "functions": [func.to_dict() for func in self.functions]
        }

        # Remove None values
        return_dict = ScoringProfile.remove_empty_values(return_dict)
        return return_dict

    @classmethod
    def load(cls, data):
        if type(data) is str:
            data = json.loads(data)
        if type(data) is not dict:
            raise Exception("Failed to parse input as Dict")
        if 'name' not in data:
            data['name'] = None
        if 'text' not in data:
            data['text'] = None
        else:
            data['text'] = ScoringProfileText.load(data['text'])
        if 'functions' not in data:
            data['functions'] = []
        else:
            data['functions'] = [ScoringProfileFunction.load(spf) for spf in data['functions']]

        return cls(name=data['name'], text=data['text'], functions=data['functions'])


class ScoringProfileText(AzureSearchObject):
    '''
    A text value for a scoring profile. Holds the weights of different fields.
    See this link for more information:
    https://docs.microsoft.com/en-us/rest/api/searchservice/add-scoring-profiles-to-a-search-index
    @:param weights: a list of field name : weight value pairs
    '''

    def __init__(self, weights):
        self.weights = weights

    def to_dict(self):
        return_dict = {
            "weights": [w.to_dict() for w in self.weights],
        }

        # Remove None values
        return_dict = ScoringProfileText.remove_empty_values(return_dict)
        return return_dict

    @classmethod
    def load(cls, data):
        if type(data) is str:
            data = json.loads(data)
        if type(data) is not dict:
            raise Exception("Failed to parse input as Dict")
        if 'weights' not in data:
            data['weights'] = None

        return cls(weights=data['weights'])


class ScoreProfileTextWeights(AzureSearchObject):
    '''
    A weight for a field.
    See this link for more information:
    https://docs.microsoft.com/en-us/rest/api/searchservice/add-scoring-profiles-to-a-search-index
    @:param searchable_field_name: name of field
    @:param relative_weight_value: weight value
    '''

    def __init__(self, searchable_field_name, relative_weight_value):
        self.searchable_field_name = searchable_field_name
        self.relative_weight_value = relative_weight_value

    def to_dict(self):
        return_dict= {self.searchable_field_name: self.relative_weight_value}

        # Remove None values
        return_dict = ScoreProfileTextWeights.remove_empty_values(return_dict)
        return return_dict

    @classmethod
    def load(cls, data):
        if type(data) is str:
            data = json.loads(data)
        if type(data) is not dict:
            raise Exception("Failed to parse input as Dict")
        if 'searchableFieldName' not in data:
            data['searchableFieldName'] = None
        if 'relativeWeightValue' not in data:
            data['relativeWeightValue'] = None

        return cls(searchable_field_name=data['searchableFieldName'], relative_weight_value=data['relativeWeightValue'])


class ScoringProfileFunction(AzureSearchObject):
    '''
    A function to perform for scoring.
    See this link for more information:
    https://docs.microsoft.com/en-us/rest/api/searchservice/add-scoring-profiles-to-a-search-index#bkmk_indexref    '''

    def __init__(self,
                 function_type,
                 field_name,
                 boost=None,
                 interpolation=None,
                 magnitude=None,
                 freshness=None,
                 distance=None,
                 tag=None):
        self.function_type = function_type
        self.field_name = field_name
        self.boost = boost
        self.interpolation = interpolation
        self.magnitude = magnitude
        self.freshness = freshness
        self.distance = distance
        self.tag = tag

        self._validate_interpolation()

    def to_dict(self):
        dict = {
            "type": self.function_type,
            "boost": self.boost,
            "fieldName": self.field_name,
            "interpolation": self.interpolation,
            "magnitude": self.magnitude,
            "freshness": self.freshness,
            "distance": self.distance,
            "tag": self.tag,
        }
        # Remove None values
        dict = ScoringProfileFunction.remove_empty_values(dict)
        return dict

    @classmethod
    def load(cls, data):
        if type(data) is str:
            data = json.loads(data)
        if type(data) is not dict:
            raise Exception("Failed to parse input as Dict")

        if 'function_type' not in data:
            data['function_type'] = None
        if 'field_name' not in data:
            data['field_name'] = None
        if 'boost' not in data:
            data['boost'] = None
        if 'interpolation' not in data:
            data['interpolation'] = None
        if 'magnitude' not in data:
            data['magnitude'] = None
        if 'freshness' not in data:
            data['freshness'] = None
        if 'distance' not in data:
            data['distance'] = None
        if 'tag' not in data:
            data['tag'] = None

        return cls(function_type=data['function_type'],
                   field_name=data['field_name'],
                   boost=data['boost'],
                   interpolation=data['interpolation'],
                   magnitude=data['magnitude'],
                   freshness=data['freshness'],
                   distance=data['distance'],
                   tag=data['tag'])

    def _validate_interpolation(self):
        if self.interpolation and self.interpolation not in interpolations:
            warnings.warn("{interpolation} not in list of supported interpolations: {interpolations}".format(
                interpolation=self.interpolation, interpolations=interpolations))


function_types = {
    "magnitude",
    "freshness",
    "distance",
    "tag"
}

interpolations = {
    "constant",
    "linear",
    "quadratic",
    "logarithmic"
}
# ``` https://docs.microsoft.com/en-us/rest/api/searchservice/add-scoring-profiles-to-a-search-index#bkmk_template

# "magnitude": {
#     "boostingRangeStart":  # ,
#         "boostingRangeEnd":  # ,
# "constantBoostBeyondRange": true | false(default)
# }
#
# // (- or -)
#
# "freshness": {
#     "boostingDuration": "..."(value representing timespan over which boosting occurs)
# }
#
# // (- or -)
#
# "distance": {
#     "referencePointParameter": "...", (parameter to be passed in queries to use as reference location)
#         "boostingDistance":  # (the distance in kilometers from the reference location where the boosting range ends)
# }
#
# // (- or -)
#
# "tag": {
#     "tagsParameter": "..."(parameter to be passed in queries to specify a list of tags to compare against target field)
# }
