
from typing import Optional, List

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
    sst_anomaly: Optional[float] = None
    hotspot: Optional[float] = None
    degree_heating_weeks: Optional[float] = None
    bleaching_percent: Optional[float] = Field(default=None, ge=0, le=100)

    mortality_percentage: Optional[float] = Field(default=None, ge=0, le=100)

    recent_storm: bool = False


class RiskResponse(BaseModel):
    risk_level: str
    risk_score: int
    reasons: List[str]


def calculate_bleaching_risk(
    sst_anomaly = None,
    hotspot = None,
    degree_heating_weeks = None,
    bleaching_percent = None,
    mortality_percentage = None,
    recent_storm = False):

    score = 0
    reason = []

    if sst_anomaly is not None:
        if sst_anomaly >= 1.5:
            score +=3
            reason.append("Very high sea surface temperature anomaly")
        
        elif sst_anomaly >=1.0:
            score +=2
            reason.append("High sea surface temperature anomaly")

        elif sst_anomaly >=0.5:
            score +=1
            reason.append("Moderate sea surface temperature anomaly")

    if hotspot is not None:
        if hotspot >= 2.0:
            score +=3
            reason.append("Severe thermal hotsopt detected")
        
        elif hotspot >= 1.0:
            score +=2
            reason.append("Thermal hotspot above bleaching threshold")
        
        elif hotspot > 0:
            score +=1
            reason.append("Minor thermal hotspot detected")
    
    if degree_heating_weeks is not None:

        if degree_heating_weeks >= 8:
            score += 4
            reason.append("Severe accumulated heat stress")

        elif degree_heating_weeks >= 4:
            score += 3
            reason.append("Significant accumulated heat stress")

        elif degree_heating_weeks >= 1:
            score += 1
            reason.append("Early accumulated heat stress")

    if bleaching_percent is not None:
        if bleaching_percent >= 50:
            score += 4
            reason.append("High observed bleaching percentage")

        elif bleaching_percent >= 20:
            score += 2
            reason.append("Moderate observed bleaching percentage")

        elif bleaching_percent > 0:
            score += 1
            reason.append("Minor observed bleaching present")

    if mortality_percentage is not None:
        if mortality_percentage >= 20:
            score += 3
            reason.append("High coral mortality observed")

        elif mortality_percentage > 0:
            score += 1
            reason.append("Some coral mortality observed")

    if recent_storm:
        score += 1
        reason.append("Recent storm may have added environmental stress")

    if score >= 10:
        risk_level = "High"

    elif score >= 5:
        risk_level = "Medium"

    else:
        risk_level = "Low"

    return {
        "risk_score": score,
        "risk_level": risk_level,
        "reasons": reason
    }



@router.post("/calculate", response_model=RiskResponse)
def calculate_risk(risk_input: RiskInput):
    return calculate_bleaching_risk(
        sst_anomaly=risk_input.sst_anomaly,
        hotspot=risk_input.hotspot,
        degree_heating_weeks=risk_input.degree_heating_weeks,
        bleaching_percent=risk_input.bleaching_percent,
        mortality_percentage=risk_input.mortality_percentage,
        recent_storm=risk_input.recent_storm,
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

        sst_anomaly=observation.sst_anomaly,
        hotspot=observation.hotspot,
        degree_heating_weeks=observation.degree_heating_weeks,
        bleaching_percent=observation.bleaching_percent,
        mortality_percentage=observation.mortality_percentage,
        recent_storm=observation.recent_storm)
