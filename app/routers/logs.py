# endpoints
from fastapi import APIRouter
from app.models import LogsEntry, LogEntry
from app.services import elastic as es_funcs
from app.services.ml import classify_log

router = APIRouter()


@router.get("/")
async def get_logs():
    es_funcs.get_logs()
    return {"message": "logs"}


@router.post("/add", response_model=LogEntry)
async def post_logs(entry: LogsEntry):
    # later: save to us + classify w. ML
    es_funcs.save_log(entry)
    classify_log(entry)
    return {"log": entry.dict()}


@router.get("/classifications")
async def get_classifications():
    return {"message": "classifications"}
