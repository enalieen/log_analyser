from ast import Index
from datetime import datetime, timedelta
from typing import Optional, List
from app.main import index
from app.utils.helpers import classify_log

from app.utils.config import (
    INDEX_NAME,
    es_client as es,
)
from app.models import LogEntry
from app.services.ml import get_tags


def create_index(index: str = INDEX_NAME):
    # service, host, tags to be added
    mappings = {
        "mappings": {
            "properties": {
                "timestamp": {"type": "date"},
                "message": {"type": "text"},
                "level": {"type": "keyword"},
                "tags": {"type": "keyword"},
            }
        }
    }
    if not es.indices.exists(index=index):
        es.indices.create(index=index, body=mappings)
    return index


def save_log(log: dict):
    log["level"] = classify_log(log)
    log["tags"] = get_tags(log["message"])
    response = es.index(index=INDEX_NAME, document=log)
    if log["level"] == "error":
        trigger_alert(log)
    return response, response["_id"]


def get_logs():
    query = {"query": {"match_all": {}}}
    try:
        response = es.search(index=INDEX_NAME, body=query)
        hits = response["hits"]["hits"]

        # return list of dicts with id + log data
        return [{"id": hit["_id"], "log": LogEntry(**hit["_source"])} for hit in hits]
    except:
        return {"message": "No logs found"}


def upd_log(id: str, entry):
    # convert to dict if it's a Pydantic model
    if hasattr(entry, "dict"):
        entry = entry.dict()
    entry["level"] = classify_log(entry)
    entry["tags"] = get_tags(entry["message"])
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


def filter_logs(
    time: Optional[datetime.datetime] = None,
    level: Optional[str] = None,
    tags: Optional[List[str]] = None,
    limit: Optional[int] = 10,
    starttime: Optional[datetime.datetime] = None,
    endtime: Optional[datetime.datetime] = None,
):
    must = []
    limit = 10 if limit is None else limit
    if time:
        must.append({"term": {"timestamp": time.isoformat()}})
    if level:
        must.append({"term": {"level": level}})
    if tags:
        for tag in tags:
            # each tag must be present
            must.append({"term": {"tags": tag}})
    if starttime or endtime:
        range_query = {}
        if starttime:
            range_query["gte"] = starttime.isoformat()
        if endtime:
            range_query["lte"] = endtime.isoformat()
        must.append({"range": {"timestamp": range_query}})

    body = {
        "size": limit,
        "query": {"bool": {"must": must}},
        "sort": {"timestamp": "desc"},
    }
    hits = es.search(index=INDEX_NAME, body=body)
    result = hits["hits"]["hits"]
    for hit in result:
        return {"id": hit["_id"], "log": LogEntry(**hit["_source"])}


# with JSON, frontend the graphs can be created
def aggregate_by_level():
    # to return only aggregation results, set size to 0, without search hits:
    body = {"size": 0, "aggs": {"by_level": {"terms": {"field": "level.keyword"}}}}
    resp = es.search(index=INDEX_NAME, body=body)
    buckets = resp.get("aggregations", {}).get("by_level", {}).get("buckets", [])
    return buckets


def search_logs(query: str, limit: int = 10):
    body = {
        "size": limit,
        "query": {
            "match": {
                "message": {"query": query, "auto_generate_synonyms_phrase_query": True}
            }
        },
        "sort": {"timestamp": "desc"},
    }
    resp = es.search(index=INDEX_NAME, body=body)["hits"]["hits"]
    if not resp:
        return {"message": "No logs found"}
    return [{"id": hit["_id"], "log": LogEntry(**hit["_source"])} for hit in resp]


def get_alerts():
    body = {
        "query": {"term": {"level.keyword": "error"}},
        "sort": {"timestamp": "desc"},
    }
    resp = es.search(index=INDEX_NAME, body=body)["hits"]["hits"]
    return [hit["_source"] for hit in resp]


def trigger_alert(log: LogEntry):
    alert = {
        "time": log.get("timestamp"),
        "message": log.get("message"),
        "level": log.get("level"),
        "tags": log.get("tags", []),
        "alert": True,
    }
    print(alert)
    return alert


def delete_old_logs(days):
    # timedelta is a time range
    cutoff_date = datetime.now() - datetime.timedelta(days=days)
    body = {"query": {"range": {"timestamp": {"lt": cutoff_date.isoformat()}}}}
    old_logs = {}
    old_logs = es.search(index=INDEX_NAME, body=body)["hits"]["hits"]
    if old_logs:
        for log in old_logs:
            res = es.delete(index=INDEX_NAME, id=log["_id"])
            return res
    return {"message": "No old logs found"}


def archive_old_logs(days: int = 30):
    cutoff = datetime.now() - datetime.timedelta(days=days)
    body = {"query": {"range": {"timestamp": {"lt": cutoff.isoformat()}}}}
    logs = es.search(index=INDEX_NAME, body=body, size=500)["hits"]["hits"]
    if logs:
        create_index("logs_archive")  # ensure archive index exists
        for log in logs:
            es.index(index="logs_archive", document=log["_source"])
    else:
        return {"message": "No old logs to archive"}
    res = es.delete_by_query(index=INDEX_NAME, body=body)
    return res
