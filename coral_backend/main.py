from fastapi import FastAPI

from . import models, reefs, observations, risk
from .database import engine

models.Base.metadata.create_all(bind = engine)

app = FastAPI(
    title = " Coral Breaching API",
    description = " API for tracking reef observation and estimating coral breaching risk.",
    version = "0.1.0",
    )

app.include_router(reefs.router)
app.include_router(observations.router)
app.include_router(risk.router)
@app.get("/")
def root():
    return {
        "message": "Coral Breaching API is running",
        "docs": "/docs",
    }

@app.get("/health")
def health_check():
    return {"status": "ok"}



    
