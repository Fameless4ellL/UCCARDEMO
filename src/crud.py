from sqlalchemy.orm import Session
from src.models import Incident, IncidentStatus
from src.schemas import IncidentCreate

def create(db: Session, incident: IncidentCreate):
    db_incident = Incident(**incident.model_dump())
    db.add(db_incident)
    db.commit()
    db.refresh(db_incident)
    return db_incident

def get(db: Session, status: IncidentStatus):
    if status:
        return db.query(Incident).filter(Incident.status == status).all()
    return db.query(Incident).all()

def update_status(db: Session, incident_id: int, status: IncidentStatus):
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        return None
    incident.status = status
    db.commit()
    db.refresh(incident)
    return incident
