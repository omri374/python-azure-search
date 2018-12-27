import json

class Field(object):
    # "name": "name_of_field",
    # "type": "Edm.String | Collection(Edm.String) | Edm.Int32 | Edm.Int64 | Edm.Double | Edm.Boolean | Edm.DateTimeOffset | Edm.GeographyPoint",
    # "searchable": true (default where applicable) | false (only Edm.String and Collection(Edm.String) fields can be searchable),
    # "filterable": true (default) | false,
    # "retrievable": true (default) | false,
    # "sortable": true (default where applicable) | false (Collection(Edm.String) fields cannot be sortable),
    # "facetable": true (default where applicable) | false (Edm.GeographyPoint fields cannot be facetable),
    # "key": true | false (default, only Edm.String fields can be keys),
    # "indexAnalyzer": "name of the indexing analyzer" (only if 'searchAnalyzer' is set and 'analyzer' is not set)
    # "searchAnalyzer": "name of the search analyzer", (only if 'indexAnalyzer' is set and 'analyzer' is not set)
    # "analyzer": "name of the analyzer used for search and indexing", (only if 'searchAnalyzer' and 'indexAnalyzer' are not set)
    # "synonymMaps": "List of synonym map to use for this index"

    name = None
    index_name = None  # For debugging only, not used by the Azure Search API
    _field_type = None
    python_type = None  # Why python type is this?
    searchable = False  # only Edm.String and Collection(Edm.String) fields can be searchable
    filterable = True
    retrievable = False
    sortable = True
    facetable = False
    key = False
    index_analyzer = None
    search_analyzer = None
    analyzer = None,
    synonym_maps = []

    def __init__(self,
                 name,
                 index_name=None,
                 searchable = True,
                 filterable=True,
                 retrievable=True,
                 sortable=True,
                 facetable=True,
                 key = False,
                 index_analyzer=None,
                 search_analyzer=None,
                 analyzer=None,
                 synonym_maps=None,
                 **kwargs):

        self.name = name
        self.index_name = index_name
        self.searchable = searchable
        self.filterable = filterable
        self.retrievable = retrievable
        self.sortable = sortable
        self.facetable = facetable
        self.key = key
        self.index_analyzer = index_analyzer
        self.search_analyzer = search_analyzer
        self.analyzer = analyzer

        if synonym_maps is None:
            synonym_maps = []
        self.synonym_maps = synonym_maps

    def __repr__(self):
        return "<Azure{cls} : {index}.{name}>".format(
            cls=self.__class__.__name__, index=self.index_name, name=self.name
        )

    @property
    def field_type(self):
        if self._field_type:
            return self._field_type
        else:
            return "Edm.{}".format(self.__class__.__name__.replace('Field', ""))

    def to_dict(self):
        return {
            "name": self.name,
            "type": self.field_type,
            "searchable": self.searchable,
            "filterable": self.filterable,
            "sortable": self.sortable,
            "facetable": self.facetable,
            "key": self.key,
            "retrievable": self.retrievable,
            "analyzer": self.analyzer,
            "searchAnalyzer": self.search_analyzer,
            "indexAnalyzer": self.index_analyzer,
            "synonym_maps": self.synonym_maps
        }

    @classmethod
    def load(cls, data, **kwargs):
        if data:
            if type(data) is str:
                data = json.loads(data)
            if type(data) is not dict:
                raise Exception("Failed to load JSON file with index data")
            field_type = types[data.pop('type')]
            kwargs.update(data)
            return field_type(**kwargs)
        else:
            raise Exception("data is Null")


class StringField(Field):
    python_type = str

    def __init__(self, name, searchable=True, key=False, *args, **kwargs):
        super().__init__(name, *args, **kwargs)
        self.key = key
        self.searchable = searchable


class CollectionField(Field):
    _field_type = "Collection(Edm.String)"

    def __init__(self, name, searchable=True, key=False, *args, **kwargs):
        kwargs['sortable'] = False
        super().__init__(name, *args, **kwargs)
        self.searchable = searchable


class Int32Field(Field):
    python_type = int


class Int64Field(Field):
    python_type = int


class DoubleField(Field):
    python_type = float


class BooleanField(Field):
    python_type = bool


class DateTimeOffsetField(Field):
    python_type = None


class GeographyPointField(Field):
    def __init__(self, name, facetable=False, *args, **kwargs):
        kwargs['facetable'] = False  # Edm.GeographyPoint fields cannot be facetable
        super().__init__(name, *args, **kwargs)


types = {
    "Edm.String": StringField,
    "Collection(Edm.String)": CollectionField,
    "Edm.Int32": Int32Field,
    "Edm.Int64": Int64Field,
    "Edm.Double": DoubleField,
    "Edm.Boolean": BooleanField,
    "Edm.DateTimeOffset": DateTimeOffsetField,
    "Edm.GeographyPoint": GeographyPointField
}
