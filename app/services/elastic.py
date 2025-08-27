from app.utils.config import (
    INDEX_NAME,
    es_client as es,
)


def create_index():
    if not es.indices.exists(index=INDEX_NAME).body:
        es.indices.create(index=INDEX_NAME)


def save_log(log: dict):
    pass


def get_logs():
    pass
