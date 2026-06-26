# Coral Reef Early Warning API

This is a FastAPI backend project for tracking coral reef observations and estimting coral bleaching risk. 

This project is currently in Phase 1, where the backend supports reef creation, observation storageand basic risk calculation using rule-based logic. 

# Project Overview:

Coral reefs are vulnerable to bleaching when ocean temperatures rise and environmental stress increases. This API allows users to store reef information, add reef observations, and calculate bleaching risk based on water temperature and bleaching percentage.

The project is designed as a learning-focused backend system using FastAPI, SQLite, and SQAlchemy.

# Tech Stack
Python
FastAPI
SQLite
SQLAlchemy
Pydantic
Uvicorn
Swagger UI

# Completed Features:
FastAPI app setup
SQLite database connection
SQLAlchemy models
Pydantic schemas
Reef CRUD basics
Observation endpoints
Rule-based bleaching risk calculator
Swagger API testing

# Project Structure
coral_backend/
├── main.py
├── database.py
├── models.py
├── schemas.py
├── reefs.py
├── observations.py
└── risk.py

# How to Run Locally
1. Clone the repository
    git clone https://github.com/praval2025
    /coral-bleaching-api.git
    cd coral-bleaching-api
2. Create a virtual environment
    python3 -m venv venv
    source venv/bin/activate
3. Install dependencies
    pip install -r requirements.txt
4. Run the server
    uvicorn coral_backend.main:app --reload
5. Open Swagger UI
    http://127.0.0.1:8000/docs

# API Endpoints
# General
GET /
GET /health
# Reefs
POST /reefs/
GET /reefs/
GET /reefs/{reef_id}
# Observations
POST /observations/
GET /observations/{observation_id}
GET /observations/reef/{reef_id}
# Risk
POST /risk/calculate
GET /risk/observation/{observation_id}

# Sample Reef Request
{
  "name": "Great Barrier Reef",
  "location": "Queensland, Australia",
  "latitude": -18.2871,
  "longitude": 147.6992
}

# Sample Observation Request
{
  "reef_id": 1,
  "water_temperature": 30.5,
  "bleaching_percent": 25,
  "notes": "Moderate bleaching visible"
}

# Sample Risk Calculation Request
{
  "water_temperature": 32.5,
  "bleaching_percent": 60
}

# Sample Risk Response
{
  "risk_level": "high",
  "risk_score": 100,
  "water_temperature": 32.5,
  "bleaching_percent": 60,
  "message": "High bleaching risk. The reef needs urgent monitoring."
}

# Risk Logic

The current risk system uses a simple rule-based scoring method.

Water temperature contributes to the risk score:

>= 31°C → +50
>= 29°C → +30
>= 27°C → +15

Bleaching percentage also contributes to the score:

>= 50% → +50
>= 25% → +30
>= 10% → +15

Final risk level:

70 or above → high
40 to 69    → medium
below 40    → low