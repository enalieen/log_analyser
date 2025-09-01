from os import times
from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


# post model
class LogsEntry(BaseModel):
    timestamp: Optional[datetime] = Field(None, description="When log was created")
    message: str


# service, host, tags to be added


# get model
class LogEntry(BaseModel):
    timestamp: datetime
    message: str
    level: str
