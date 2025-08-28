from elasticsearch import Elasticsearch
import os

ELASTICSEARCH_HOST = os.getenv("ELASTICSEARCH_HOST", "http://elastic:9200")
INDEX_NAME = os.getenv("INDEX_NAME", "logs_tests")

if not ELASTICSEARCH_HOST:
    raise ValueError("ELASTICSEARCH_HOST is not set")

es_client = Elasticsearch(ELASTICSEARCH_HOST)
