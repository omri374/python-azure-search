import logging
from abc import ABC, abstractmethod

from azuresearch.azure_search_object import AzureSearchObject


class AbstractAnalyzer(AzureSearchObject):

    def __init__(self, index_name, analyzer_name, analyzer_type):
        self.index_name = index_name
        self.analyzer_name = analyzer_name
        self.analyzer_type = analyzer_type

    def test(self, text):
        body = {"analyzer": self.analyzer_type, "text": text}
        logging.info("Testing analyzer: {analyzer} with text: {text}".format(analyzer=self.analyzer_type, text=text))
        return self.endpoint.get(data=body, endpoint=self.index_name, needs_admin=True)

    def update(self, allow_index_downtime=False):

        if allow_index_downtime:
            logging.warning(
                "Updating analyzer: {analyzer}. Index will be down until update is complete".format(
                    analyzer=self.name))
            return self.endpoint.put(data=self.to_dict(),
                                     endpoint=self.index_name,
                                     extra={"allowIndexDowntime": allow_index_downtime})
        else:
            logging.error(
                "Cannot update analyzer unless the index is turned off")
