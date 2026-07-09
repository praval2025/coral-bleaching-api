from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .risk import calculate_bleaching_risk

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
        raise HTTPException(status_code = 404, detail = "Reef not found")

    observation_data = observation.model_dump()

    risk_result = calculate_bleaching_risk(
        sst_anomaly = observation.sst_anomaly,
        hotspot = observation.hotspot,
        degree_heating_weeks = observation.degree_heating_weeks,
        bleaching_percent = observation.bleaching_percent,
        mortality_percentage = observation.mortality_percentage,
        recent_storm = observation.recent_storm
    )

    observation_data["risk_score"] = risk_result["risk_score"]

    observation_data["risk_level"] = risk_result["risk_level"]
    new_observation = models.Observation(**observation_data)
    db.add(new_observation)
    db.commit()
    db.refresh(new_observation)

    return new_observation

@router.get("/", response_model = list[schemas.ObservationResponse])

def get_observations(db: Session = Depends(get_db)):
    return db.query(models.Observation).all()

@router.get("/reef/{reef_id}", response_model = list[schemas.ObservationResponse])

def get_observations_for_reef(reef_id: int, db: Session = Depends(get_db)):
    reef = db.query(models.Reef).filter(models.Reef.id == reef_id).first()

    if reef is None:
        raise HTTPException(status_code = 404, detail = "Reef not found")
    
    return db.query(models.Observation).filter(models.Observation.reef_id == reef_id).all()


