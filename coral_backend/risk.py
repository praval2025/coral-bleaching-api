from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from . import models
from .database import get_db


router = APIRouter(
    prefix="/risk",
    tags=["risk"],
)


class RiskInput(BaseModel):
    water_temperature: float = Field(..., ge=0)
    bleaching_percent: float = Field(..., ge=0, le=100)


class RiskResponse(BaseModel):
    risk_level: str
    risk_score: int
    water_temperature: float
    bleaching_percent: float
    message: str


def calculate_bleaching_risk(
    water_temperature: float,
    bleaching_percent: float,
) -> RiskResponse:
    risk_score = 0

    if water_temperature >= 31:
        risk_score += 50
    elif water_temperature >= 29:
        risk_score += 30
    elif water_temperature >= 27:
        risk_score += 15

    if bleaching_percent >= 50:
        risk_score += 50
    elif bleaching_percent >= 25:
        risk_score += 30
    elif bleaching_percent >= 10:
        risk_score += 15

    if risk_score >= 70:
        risk_level = "high"
        message = "High bleaching risk. The reef needs urgent monitoring."
    elif risk_score >= 40:
        risk_level = "medium"
        message = "Medium bleaching risk. Conditions should be watched closely."
    else:
        risk_level = "low"
        message = "Low bleaching risk based on the current observation."

    return RiskResponse(
        risk_level=risk_level,
        risk_score=risk_score,
        water_temperature=water_temperature,
        bleaching_percent=bleaching_percent,
        message=message,
    )


@router.post("/calculate", response_model=RiskResponse)
def calculate_risk(risk_input: RiskInput):
    return calculate_bleaching_risk(
        water_temperature=risk_input.water_temperature,
        bleaching_percent=risk_input.bleaching_percent,
    )


@router.get("/observation/{observation_id}", response_model=RiskResponse)
def get_observation_risk(
    observation_id: int,
    db: Session = Depends(get_db),
):
    observation = (
        db.query(models.Observation)
        .filter(models.Observation.id == observation_id)
        .first()
    )

    if observation is None:
        raise HTTPException(status_code=404, detail="Observation not found")

    return calculate_bleaching_risk(
        water_temperature=observation.water_temperature,
        bleaching_percent=observation.bleaching_percent,
    )
