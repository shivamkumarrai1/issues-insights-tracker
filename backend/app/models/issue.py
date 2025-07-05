from sqlalchemy import Column, String, Enum, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base
import enum

class StatusEnum(str, enum.Enum):
    OPEN = "OPEN"
    TRIAGED = "TRIAGED"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"

class SeverityEnum(str, enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class Issue(Base):
    __tablename__ = "issues"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    file_path = Column(String, nullable=True)
    status = Column(Enum(StatusEnum), default=StatusEnum.OPEN)
    severity = Column(Enum(SeverityEnum), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    reporter_id = Column(String, ForeignKey("users.id"))
    reporter = relationship("User")
