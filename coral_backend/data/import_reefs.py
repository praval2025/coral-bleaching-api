from pathlib import Path
import pandas as pd
from coral_backend.models import Reef
from coral_backend.database import SessionLocal

PROJECT_ROOT = Path(__file__).resolve().parents[2]

CSV_FILE= (
    PROJECT_ROOT
    / "coral_backend"
    / "data"
    / "gbr_reefs.csv"
)

df = pd.read_csv(CSV_FILE)

DEFAULT_COUNTRY = "Australia"
DEFAULT_REGION = "Great Barrier Reef"
DEFAULT_SOURCE = "eAtlas/GBRMPA via CSIRO WFS"


db = SessionLocal()

inserted_count = 0
try:    
    for index, row in df.iterrows():
        external_site_id = str(row["GBR_ID"])

        existing_reef = (db.query(Reef).filter(Reef.external_site_id == external_site_id).first()
        )

        if existing_reef:
            continue

        reef = Reef(name = row["GBR_NAME"], country = DEFAULT_COUNTRY, region = DEFAULT_REGION, latitude = row["Y_COORD"], longitude = row["X_COORD"], source = DEFAULT_SOURCE, external_site_id = external_site_id)

        db.add(reef)
        inserted_count +=1

    db.commit()
    print(inserted_count)
    

finally:
    db.close()

print(db.query(Reef).count())

