from app.utils.config import (
    INDEX_NAME,
    es_client as es,
)
from app.models import LogEntry


def create_index():
    if not es.indices.exists(index=INDEX_NAME).body:
        es.indices.create(index=INDEX_NAME)
    return INDEX_NAME


def save_log(log: dict):
    response = es.index(index=INDEX_NAME, document=log)
    return response, response["_id"]


def get_logs():
    query = {"query": {"match_all": {}}}
    response = es.search(index=INDEX_NAME, body=query)
    hits = response["hits"]["hits"]
    # return list of dicts with id + log data
    return [{"id": hit["_id"], **hit["_source"]} for hit in hits]


def upd_log(id: str, entry):
    es.update(index=INDEX_NAME, id=id, body={"doc": entry.dict()})
    updated = es.get(index=INDEX_NAME, id=id)["_source"]
    return LogEntry(**updated)


def del_log(id: str):
    try:
        es.get(index=INDEX_NAME, id=id)
        return {"message": "log deleted"}
    except:
        return {"message": "log not found"}
