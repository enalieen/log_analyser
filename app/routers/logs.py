# endpoints
from fastapi import APIRouter, HTTPException
from app.models import LogsEntry, LogEntry
from app.services import elastic as es_funcs
from datetime import datetime

router = APIRouter()


@router.get("/")
async def get_logs():
    logs = es_funcs.get_logs()
    if not logs:
        raise HTTPException(status_code=404, detail="No logs found")
    return {"message": logs}


@router.post("/add", response_model=LogEntry)
async def post_logs(entry: LogsEntry):
    log_data = entry.dict()
    if log_data["timestamp"] is None:
        log_data["timestamp"] = datetime.now()
    # later: save to us + classify w. ML
    es_funcs.save_log(log_data)
    # return normalized log
    return LogEntry(**log_data)


@router.put("/upd/{id}", response_model=LogEntry)
def upd_log_endpoint(id: str, entry: LogsEntry):
    upd = es_funcs.upd_log(id, entry)
    return upd


@router.get("/classifications")
async def get_classifications():
    return {"message": "classifications"}


@router.delete("/del/{id}")
async def del_log_endpoint(id: str):
    msg = es_funcs.del_log(id)
    return msg
