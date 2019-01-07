class FieldMapping(object):

    def __init__(self, source_field_name, target_field_name=None, mapping_function=None):
        """
        :param source_field_name: which represents a field in your data source. This property is required.
        :param target_field_name: which represents a field in your search index. If omitted, the same name as in the data source is used.
        :param mapping_function: Transforms your data using one of several predefined functions. See here for more info: https://docs.microsoft.com/en-us/azure/search/search-indexer-field-mappings#mappingFunctions
        """
        self.source_field_name = source_field_name
        self.target_field_name = target_field_name
        self.mapping_function = mapping_function

