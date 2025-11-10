from sqlalchemy import Column, Integer, String, DateTime, Enum
from datetime import datetime, timezone
from enum import Enum as PyEnum
from src.database import Base

class IncidentStatus(PyEnum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"

class IncidentSource(PyEnum):
    OPERATOR = "operator"
    MONITORING = "monitoring"
    PARTNER = "partner"

class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String(length=500), nullable=False)
    status: Column[IncidentStatus] = Column(Enum(IncidentStatus), default=IncidentStatus.NEW)
    source: Column[IncidentSource] = Column(Enum(IncidentSource), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
