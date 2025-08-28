from app.utils.config import (
    INDEX_NAME,
    es_client as es,
)


def create_index():
    if not es.indices.exists(index=INDEX_NAME).body:
        es.indices.create(index=INDEX_NAME)
    return INDEX_NAME


def save_log(log: dict):
    response = es.index(index=INDEX_NAME, body=log)
    return response


def get_logs():
    query = {"query": {"match_all": {}}}
    response = es.search(index=INDEX_NAME, body=query)
    hits = response["hits"]["hits"]
    return [hit["_source"] for hit in hits]
