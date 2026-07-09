from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

class ReefBase(BaseModel):
    name: str
    location: str
    latitude: float | None = None
    longitude: float | None = None

class ReefCreate(ReefBase):
    pass

class ReefResponse(ReefBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

class ObservationBase(BaseModel):
    reef_id: int
    observation_date: date | None = None

    sea_surface_temperature: Optional[float] = None
    sst_anomaly: Optional[float] = None
    hotspot: Optional[float] = None
    degree_heating_weeks: Optional[float] = None
    bleaching_alert_level: Optional[str] = None

    bleaching_percent: float = Field(..., ge=0, le=100)
    coral_cover_percentage: Optional[float] = None
    mortality_percentage: Optional[float] = Field(default=None, ge=0, le=100)
    disease_presence: bool = False

    water_depth: Optional[float] = None
    turbidity: Optional[float] = None
    water_clarity: Optional[str] = None
    recent_storm: bool = False

    notes: Optional[str] = None



class ObservationCreate(ObservationBase):
    pass

class ObservationResponse(ObservationBase):
    id: int 
    risk_score: Optional[float] = None
    risk_level: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
