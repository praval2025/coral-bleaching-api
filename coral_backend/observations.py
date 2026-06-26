from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from . import models, schemas
from .database import get_db

router = APIRouter(
    prefix = "/observations",
    tags = ["observations"],
)

@router.post("/", response_model = schemas.ObservationResponse)
def create_observation(
    observation: schemas.ObservationCreate,
    db: Session = Depends(get_db)
):
    reef = db.query(models.Reef).filter(models.Reef.id == observation.reef_id).first()

    if reef is None:
        raise HTTPException(status_code = 404, details = "Reef not found")
    
    db_observation = models.Observation(**observation.model_dump())

    db.add(db_observation)
    db.commit()
    db.refresh(db_observation)

    return db_observation

@router.get("/", response_model = list[schemas.ObservationResponse])

def get_observations(db: Session = Depends(get_db)):
    return db.query(models.Observation).all()

@router.get("/reef/{reef_id}", response_model = list[schemas.ObservationResponse])

def get_observations_for_reef(reef_id: int, db: Session = Depends(get_db)):
    reef = db.query(models.Reef).filter(models.Reef.id == reef_id).first()

    if reef is None:
        raise HTTPException(status_code = 404, detail = "Reef not found")
    
    return db.query(models.Observation).filter(models.Observation.reef_id == reef_id).all()



