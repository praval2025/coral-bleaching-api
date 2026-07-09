from pathlib import Path
import geopandas as gpd


print("1. Script started")

PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = PROJECT_ROOT / "gbr_features.geojson"
OUTPUT_FILE = (
    PROJECT_ROOT
    / "coral_backend"
    / "data"
    / "gbr_reefs.csv"
)

print(f"2. Input file: {INPUT_FILE}")
print(f"3. Input exists: {INPUT_FILE.exists()}")

print("4. Loading GeoJSON...")
gdf = gpd.read_file(INPUT_FILE)

print(f"5. Loaded {len(gdf)} rows")


reefs = gdf[(gdf["FEAT_NAME"] == "Reef") & (gdf["GBR_NAME"] != "U/N Reef")]
print(f"Total reef rows: {len(reefs)}")

reefs_dataframe = reefs[[
    "GBR_ID",
    "GBR_NAME",
    "X_COORD",
    "Y_COORD"
]]

print(reefs_dataframe)

reefs_dataframe.to_csv(OUTPUT_FILE, index = False,)

print("Missing X_COORD:", reefs_dataframe["X_COORD"].isna().sum())
print("Missing Y_COORD:", reefs_dataframe["Y_COORD"].isna().sum())
print("Dupilcated GBR_ID", reefs_dataframe["GBR_ID"].duplicated().sum())
print(len(reefs_dataframe))