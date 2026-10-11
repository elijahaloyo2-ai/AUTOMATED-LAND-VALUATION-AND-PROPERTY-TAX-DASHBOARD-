import geopandas as gpd
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib

# Load sample spatial data (GeoJSON containing polygons and features)
# Expected features: 'plot_size_m2', 'dist_to_urban_km', 'road_access_score', 'market_value'
df = gpd.read_file("data/parcels.geojson")

# Define features and target
X = df[['plot_size_m2', 'dist_to_urban_km', 'road_access_score']]
y = df['market_value']

# Train-test split and model fitting
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save the trained model
joblib.dump(model, "model/valuation_model.pkl")
print("Model trained and saved successfully.")
