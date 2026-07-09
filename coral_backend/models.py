from sqlalchemy import Column, Float, ForeignKey, Integer, String, Date, Boolean
from sqlalchemy.orm import relationship
from .database import Base


class Reef(Base):
    __tablename__ = "reefs"

    id = Column(Integer, primary_key = True, index = True)
    name = Column(String, nullable = False)
    country = Column(String, nullable = False)
    region = Column(String, nullable = False)

    latitude = Column(Float, nullable = True)
    longitude = Column(Float, nullable = True)

    source = Column(String, nullable = True)
    external_site_id = Column(String, nullable = True)


    observations = relationship("Observation", back_populates = "reef")

class Observation(Base):
    __tablename__ = "observations"

    id = Column(Integer, primary_key = True, index = True)
    reef_id = Column(Integer, ForeignKey("reefs.id"), nullable = False)
    observation_date = Column(Date, nullable = False)

    # Satellite/ environmental data
    sea_surface_temperature = Column(Float, nullable = True)
    sst_anomaly = Column(Float, nullable = True)
    hotspot = Column(Float, nullable = True)
    degree_heating_weeks = Column(Float, nullable = True)
    bleaching_alert_level = Column(String, nullable = True)

    #Field observation data
    bleaching_percent = Column(Float, nullable = False)
    coral_cover_percentage = Column(Float, nullable = True)
    mortality_percentage = Column(Float, nullable = True)
    disease_presence = Column(Boolean, default = False )

    #Local condition data
    water_depth = Column(Float, nullable = True)
    turbidity = Column(Float,  nullable = True)
    water_clarity = Column(String, nullable=True)
    recent_storm = Column(Boolean, default=False)

    #apps calculated output
    risk_score = Column(Float, nullable = True)
    risk_level = Column(String, nullable = True)


   
    
    notes = Column(String, nullable = True)

    reef = relationship("Reef", back_populates = "observations")