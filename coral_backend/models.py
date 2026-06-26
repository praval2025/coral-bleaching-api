from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from .database import Base


class Reef(Base):
    __tablename__ = "reefs"

    id = Column(Integer, primary_key = True, index = True)
    name = Column(String, nullable = False)
    location = Column(String, nullable = False)
    latitude = Column(Float, nullable = True)
    longitude = Column(Float, nullable = True)

    observations = relationship("Observation", back_populates = "reef")

class Observation(Base):
    __tablename__ = "observations"

    id = Column(Integer, primary_key = True, index = True)
    reef_id = Column(Integer, ForeignKey("reefs.id"), nullable = False)

    water_temperature = Column(Float, nullable = False)
    bleaching_percent = Column(Float, nullable = False)
    notes = Column(String, nullable = True)

    reef = relationship("Reef", back_populates = "observations")