from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated
from src.database import SessionLocal, engine, Base
from src.models import IncidentStatus
from src.schemas import IncidentCreate, IncidentOut, IncidentUpdate
from src.crud import create, get, update_status

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

DB = Annotated[Session, Depends(get_db)]

@app.post("/incidents", response_model=IncidentOut)
def create_v1(incident: IncidentCreate, db: DB):
    return create(db, incident)

@app.get("/incidents", response_model=list[IncidentOut])
def read_v1(status: IncidentStatus, db: DB):
    return get(db, status)

@app.patch("/incidents/{incident_id}", response_model=IncidentOut)
def update_v1(incident_id: int, update: IncidentUpdate, db: DB):
    incident = update_status(db, incident_id, update.status)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    return incident
