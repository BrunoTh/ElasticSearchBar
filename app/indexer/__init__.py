from abc import ABC, abstractmethod
from elasticsearch import Elasticsearch


class Indexer(ABC):
    def __init__(self, es_server: str, es_index: str, **kwargs):
        self.es = Elasticsearch(es_server)
        self.es_index = es_index

    @abstractmethod
    def run(self):
        """
        Starts the indexer which collects data and writes it to the Elasticsearch instance.
        """
