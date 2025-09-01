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
    log["level"] = classify_log(log)
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
    # convert to dict if it's a Pydantic model
    if hasattr(entry, "dict"):
        entry = entry.dict()
    entry["level"] = classify_log(entry)
    es.update(index=INDEX_NAME, id=id, body={"doc": entry})
    updated = es.get(index=INDEX_NAME, id=id)["_source"]
    return LogEntry(**updated)


def del_log(id: str):
    try:
        es.delete(index=INDEX_NAME, id=id)
        return {"message": "log deleted"}
    except:
        return {"message": "log not found"}


def sort_logs():
    body = {}
    hits = es.search(index=INDEX_NAME, body=body)
    return hits


def classify_log(log: dict) -> str:
    msg = log.get("message", "").lower()

    if any(word in msg for word in ["error", "fail", "exception", "crash"]):
        return "error"
    elif any(word in msg for word in ["warn", "deprecated", "retry"]):
        return "warning"
    elif any(word in msg for word in ["debug", "trace", "verbose"]):
        return "debug"
    elif any(
        word in msg for word in ["login", "logout", "auth", "token", "unauthorized"]
    ):
        return "auth"
    elif any(word in msg for word in ["sql", "database", "query", "connection"]):
        return "database"
    elif any(word in msg for word in ["timeout", "dns", "socket", "network"]):
        return "network"
    elif any(word in msg for word in ["slow", "latency", "performance"]):
        return "performance"
    elif any(word in msg for word in ["payment", "transaction", "billing"]):
        return "payment"
    else:
        return "info"


""" def tag_log(log: dict) -> str:
    msg = log.get("message", "").lower()
    tags = []

    if any(word in msg for word in ["error", "fail", "exception", "crash"]):
        tags.append("error")
    if any(word in msg for word in ["warn", "deprecated", "retry"]):
        tags.append("warning")
    if any(word in msg for word in ["debug", "trace", "verbose"]):
        tags.append("debug") """


""" 
to add: Search with filtering (for example, by ERROR level, by date or by message text):

Aggregations (count the number of logs by levels, by days, etc.).

Pagination (to return logs in parts, not all at once).

Classification/tagging.

(optional) Archiving/cleaning old logs. """
