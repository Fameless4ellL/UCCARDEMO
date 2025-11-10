from pydantic import BaseModel
from datetime import datetime
from src.models import IncidentStatus, IncidentSource

class IncidentCreate(BaseModel):
    description: str
    status: IncidentStatus
    source: IncidentSource

class IncidentUpdate(BaseModel):
    status: IncidentStatus

class IncidentOut(BaseModel):
    id: int
    description: str
    status: IncidentStatus
    source: IncidentSource
    created_at: datetime

    class Config:
        from_attributes = True
