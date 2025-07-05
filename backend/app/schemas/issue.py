from pydantic import BaseModel
from enum import Enum
from typing import Optional
from datetime import datetime

class StatusEnum(str, Enum):
    OPEN = "OPEN"
    TRIAGED = "TRIAGED"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"

class SeverityEnum(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class IssueBase(BaseModel):
    title: str
    description: Optional[str]
    severity: SeverityEnum

class IssueCreate(IssueBase):
    file_path: Optional[str] = None

class IssueUpdate(BaseModel):
    status: Optional[StatusEnum] = None
    severity: Optional[SeverityEnum] = None
    title: Optional[str] = None
    description: Optional[str] = None

class IssueRead(IssueBase):
    id: str
    status: StatusEnum
    created_at: datetime
    updated_at: datetime
    file_path: Optional[str]
    reporter_id: str

    class Config:
        orm_mode = True
