from app.utils.config import (
    INDEX_NAME,
    es_client as es,
)
from app.models import LogEntry


def create_index():
    # service, host, tags to be added
    mappings = {
        "mappings": {
            "properties": {
                "timestamp": {"type": "date"},
                "message": {"type": "text"},
                "level": {"type": "text"},
            }
        }
    }
    if not es.indices.exists(index=INDEX_NAME).body:
        es.indices.create(index=INDEX_NAME, body=mappings)
    return INDEX_NAME


def save_log(log: dict):
    response = es.index(index=INDEX_NAME, document=log)
    return response, response["_id"]


def get_logs():
    query = {"query": {"match_all": {}}}
    try:
        response = es.search(index=INDEX_NAME, body=query)

        hits = response["hits"]["hits"]
        # return list of dicts with id + log data
        return [{"id": hit["_id"], **hit["_source"]} for hit in hits]
    except:
        return {"message": "No logs found"}


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
