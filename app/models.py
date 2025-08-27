from pydantic import BaseModel
from datetime import datetime


class LogsEntry(BaseModel):
    timestamp: datetime
    message: str
    level: str


class LogEntry(BaseModel):
    message: str
    level: str
