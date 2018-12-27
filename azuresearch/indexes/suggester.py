def Suggester(object):
    def __init__(self, name, source_fields, search_mode="analyzingInfixMatching" ):
        self.name = name
        self.source_fields = source_fields
        self.search_mode = search_mode

    def to_dict(self):
        return {
            "name": self.name,
            "sourceFields": [field for field in self.source_fields],
            "searchMode": self.search_mode
        }
