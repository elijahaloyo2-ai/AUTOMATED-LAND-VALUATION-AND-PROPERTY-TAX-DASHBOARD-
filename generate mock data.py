import os
import json
from shapely.geometry import Polygon, mapping

os.makedirs("data", exist_ok=True)

# Define a few mock polygon coordinates (representing small adjacent land parcels)
base_coords = [
    (34.45, -0.95),
    (34.46, -0.95),
    (34.46, -0.96),
    (34.45, -0.96),
    (34.45, -0.95)
]

features = []
for i in range(1, 11):
    # Offset coordinates slightly for each parcel to spread them out on the map
    offset = (i % 3) * 0.01
    shift = (i // 3) * 0.01
    poly_coords = [(lng + offset, lat - shift) for lng, lat in base_coords]
    
    feature = {
        "type": "Feature",
        "geometry": mapping(Polygon(poly_coords)),
        "properties": {
            "parcel_id": f"PRC-10{i}",
            "plot_size_m2": round(500 + (i * 120.5), 2),
            "dist_to_urban_km": round(1.2 + (i * 0.4), 1),
            "road_access_score": (i % 5) + 1,
            "market_value": round(15000 + (i * 4200.0), 2)
        }
    }
    features.append(feature)

geojson_data = {
    "type": "FeatureCollection",
    "features": features
}

with open("data/parcels.geojson", "w") as f:
    json.dump(geojson_data, f, indent=2)

print("Mock parcels.geojson generated successfully inside the 'data/' folder.")
