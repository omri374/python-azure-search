class ScoringProfile(object):
    '''
    A scoring profile for an index. See this link for more information:
    taken from https://docs.microsoft.com/en-us/rest/api/searchservice/add-scoring-profiles-to-a-search-index
    '''


    def __init__(self, name, text=None, functions=None):

        if text is None:
            text = []
        if functions is None:
            functions = []

        self.name = name
        self.text = text
        self.functions = functions

    def to_dict(self):
        return {
            "name": self.name,
            "text": [txt.to_dict() for txt in self.text],
            "functions": [func.to_dict() for func in self.functions]
        }


class ScoringProfileText(object):
    '''
    A text value for a scoring profile. Holds the weights of different fields.
    See this link for more information:
    https://docs.microsoft.com/en-us/rest/api/searchservice/add-scoring-profiles-to-a-search-index
    @:param weights: a list of field name : weight value pairs
    '''
    def __init__(self, weights):
        self.weights = weights

    def to_dict(self):
        return {
            "weights": [w.to_dict() for w in self.weights],
        }


class ScoreProfileTextWeights(object):
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
        return {self.searchable_field_name: self.relative_weight_value}


class ScoringProfileFunction(object):
    '''
    A function to perform for scoring.
    See this link for more information:
    https://docs.microsoft.com/en-us/rest/api/searchservice/add-scoring-profiles-to-a-search-index#bkmk_indexref    '''
    def __init__(self,
                 function_type,
                 boost,
                 field_name,
                 interpolation='linear',
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

    def to_dict(self):
        return {
            "type": self.function_type,
            "fieldName": self.field_name,
            "interpolation": self.interpolation,
            "magnitude": self.magnitude,
            "freshness": self.freshness,
            "distance": self.distance,
            "tag": self.tag,
        }


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
