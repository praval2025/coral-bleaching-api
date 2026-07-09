from pathlib import Path

print("1. Script started")

PROJECT_ROOT = Path(__file__).resolve().parents[2]
FILE_PATH = PROJECT_ROOT / "gbr_features.geojson"

print(f"2. Looking for: {FILE_PATH}")
print(f"3. File exists: {FILE_PATH.exists()}")

import geopandas as gpd

print("4. GeoPandas imported")
print("5. Reading GeoJSON...")

gdf = gpd.read_file(FILE_PATH)

print("6. GeoJSON loaded")
print(f"Number of rows: {len(gdf)}")
print(f"CRS: {gdf.crs}")
print(f"Columns: {gdf.columns.tolist()}")

print("\nFirst 5 rows:")
print(gdf.head().to_string())
