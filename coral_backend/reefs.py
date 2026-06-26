from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from . import models, schemas
from .database import get_db

router = APIRouter(
    prefix = "/reefs",
    tags = ["reefs"],
)

@router.post("/", response_model = schemas.ReefResponse)

def create_reef(reef: schemas.ReefCreate,db: Session = Depends(get_db)):
    db_reef = models.Reef(**reef.model_dump())

    db.add(db_reef)
    db.commit()
    db.refresh(db_reef)

    return db_reef

@router.get("/", response_model = list[schemas.ReefResponse])
def get_reefs(db: Session = Depends(get_db)):
    return db.query(models.Reef).all()

@router.get("/{reef_id}", response_model = schemas.ReefResponse)
def get_reef(reef_id: int, db: Session = Depends(get_db)):
    reef = db.query(models.Reef).filter(models.Reef.id == reef_id). first()

    if reef is None:
        raise HTTPException(status_code = 404, detail = "Reef not found")
    
    return reef