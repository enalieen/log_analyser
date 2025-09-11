import datetime
from app.utils.config import es, INDEX_NAME


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


""" def bulk_save_logs(logs: list[dict]):
    actions = [
        {
            "_index": "logs",
            "_source": log,
        }
        for log in logs
    ]
    helpers.bulk(es, actions) """
