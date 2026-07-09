from coral_backend.database import SessionLocal
from coral_backend.models import Reef
import requests

db = SessionLocal()

reef = db.query(Reef).first()

latitude = reef.latitude
longitude = reef.longitude

print(latitude)
print(longitude)

SST_URL = "https://marine-api.open-meteo.com/v1/marine"

params = {
    "latitude": latitude,
    "longitude": longitude,
    "hourly": "sea_surface_temperature"
}

response = requests.get(SST_URL, params = params)

if response.status_code ==200:

    values = response.json()
    print(values.keys())
    print(values["hourly"].keys())

    time = values["hourly"]["time"][0]
    sst = values["hourly"]["sea_surface_temperature"][0]

    print(time)
    print(sst)
else: 
    print("Request failed:", response.status_code)

db.close()