from azuresearch.base_api_call import BaseApiCall


class DataSource(BaseApiCall):

    def __init__(self, name, connection_string, container_name, type='azureblob', description=None):
        super(DataSource, self).__init__(service_name="datasources")
        self.name = name
        self.connection_string = connection_string
        self.container_name = container_name
        self.type = type
        self.description = description

    def to_dict(self):
        dict = {
            "name": self.name,
            "description": self.description,
            "type": self.type,
            "credentials": {"connectionString": self.connection_string},
            "container": {"name": self.container_name}
        }

        # Remove None values
        dict = BaseApiCall.remove_empty_values_from_dict(dict)
        return dict
