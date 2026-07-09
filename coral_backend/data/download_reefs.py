from pathlib import Path

import certifi
import requests


WFS_URL = "https://www.cmar.csiro.au/geoserver/wfs"

PARAMS = {
    "service": "WFS",
    "version": "1.1.0",
    "request": "GetFeature",

    # Correct namespace from WFS capabilities
    "typeName": "ea-be:GBR_GBRMPA_GBR-features",

    "outputFormat": "application/json",
    "srsName": "EPSG:4326",
}

PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_FILE = PROJECT_ROOT / "gbr_features.geojson"


def main():
    try:
        print("Requesting GBR feature data...")

        response = requests.get(
            WFS_URL,
            params=PARAMS,
            timeout=180,
            verify=certifi.where(),
        )

        print(f"HTTP status: {response.status_code}")
        print(
            "Content-Type:",
            response.headers.get("Content-Type"),
        )

        response.raise_for_status()

        content_type = (
            response.headers
            .get("Content-Type", "")
            .lower()
        )

        # Prevent XML error responses from being
        # saved as fake GeoJSON
        if "json" not in content_type:
            print("\nServer did not return JSON.")
            print("\nFirst 1000 characters:")
            print(response.text[:1000])
            return

        data = response.json()

        if data.get("type") != "FeatureCollection":
            print(
                "\nJSON received, but it is not "
                "a GeoJSON FeatureCollection."
            )
            print(data)
            return

        features = data.get("features", [])

        OUTPUT_FILE.write_text(
            response.text,
            encoding="utf-8",
        )

        print("\nDownloaded successfully!")
        print(f"Number of features: {len(features)}")
        print(f"Saved to: {OUTPUT_FILE}")

    except requests.RequestException as error:
        print("\nRequest failed:")
        print(error)

    except ValueError as error:
        print("\nResponse was not valid JSON:")
        print(error)


if __name__ == "__main__":
    main()