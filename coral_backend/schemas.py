from pydantic import BaseModel

class ReefBase(BaseModel):
    name: str
    location: str
    latitude: float | None = None
    longitude: float | None = None

class ReefCreate(ReefBase):
    pass


class ReefResponse(ReefBase):
    id: int

    class Config:
        from_attributes = True

class ObservationBase(BaseModel):
    reef_id: int
    water_temperature: float
    bleaching_percent: float
    notes: str | None = None

class ObservationCreate(ObservationBase):
    pass

class ObservationResponse(ObservationBase):
    id: int 

    class Config:
        from_attributes = True

