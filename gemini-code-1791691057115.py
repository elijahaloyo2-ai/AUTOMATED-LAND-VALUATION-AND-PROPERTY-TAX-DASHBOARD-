import os
import json
import joblib
import streamlit as st
import geopandas asandas
import pandas as pd
import folium
from streamlit_folium import st_folium
from sklearn.ensemble import RandomForestRegressor
from shapely.geometry import Polygon, mapping

# Page configuration
st.set_page_config(page_title="County CAMA & Property Tax Dashboard", layout="wide")

st.title("Automated Land Valuation & Property Tax Dashboard")
st.markdown("Computer-Assisted Mass Appraisal (CAMA) prototype for optimizing county land revenue collection.")

# Load model and data with self-contained fallback generation
@st.cache_resource
def load_resources():
    os.makedirs("data", exist_ok=True)
    os.makedirs("model", exist_ok=True)
    
    data_path = "data/parcels.geojson"
    model_path = "model/valuation_model.pkl"
    
    # 1. Auto-generate mock GeoJSON data if missing
    if not os.path.exists(data_path):
        base_coords = [
            (34.45, -0.95),
            (34.46, -0.95),
            (34.46, -0.96),
            (34.45, -0.96),
            (34.45, -0.95)
        ]
        features = []
        for i in range(1, 11):
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
        with open(data_path, "w") as f:
            json.dump(geojson_data, f, indent=2)

    # 2. Auto-train and save the model if missing
    if not os.path.exists(model_path):
        df = gpd.read_file(data_path)
        X = df[['plot_size_m2', 'dist_to_urban_km', 'road_access_score']]
        y = df['market_value']
        
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X, y)
        joblib.dump(model, model_path)
        
    model = joblib.load(model_path)
    gdf = gpd.read_file(data_path)
    return model, gdf

model, gdf = load_resources()

# Predict values for all parcels
features = gdf[['plot_size_m2', 'dist_to_urban_km', 'road_access_score']]
gdf['predicted_value'] = model.predict(features)

# Sidebar controls for tax policy simulation
st.sidebar.header("Tax Policy Settings")
tax_rate = st.sidebar.slider("Annual Property Tax Rate (%)", min_value=0.1, max_value=3.0, value=1.0, step=0.1)
gdf['calculated_tax'] = gdf['predicted_value'] * (tax_rate / 100)

# Summary metrics
total_valuation = gdf['predicted_value'].sum()
total_potential_revenue = gdf['calculated_tax'].sum()

col1, col2, col3 = st.columns(3)
col1.metric("Total Parcels Assessed", len(gdf))
col2.metric("Total Estimated Land Value", f"${total_valuation:,.2f}")
col3.metric("Projected Annual Revenue", f"${total_potential_revenue:,.2f}")

# Create Folium Map centered on the data centroid
centroid = gdf.unary_union.centroid
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=13, tiles="CartoDB positron")

# Add GeoJson layer with conditional styling and tooltips
folium.GeoJson(
    gdf,
    name="Land Parcels",
    style_function=lambda feature: {
        'fillColor': '#3186cc' if feature['properties']['road_access_score'] > 2 else '#ff7f0e',
        'color': 'black',
        'weight': 1,
        'fillOpacity': 0.6,
    },
    tooltip=folium.GeoJsonTooltip(
        fields=['parcel_id', 'plot_size_m2', 'predicted_value', 'calculated_tax'],
        aliases=['Parcel ID:', 'Size (m²):', 'Est. Value ($):', 'Tax Due ($):'],
        localize=True
    )
).add_to(m)

# Render map in Streamlit
st.subheader("Interactive Parcel Valuation Map")
st_data = st_folium(m, width=1100, height=550)

# Detailed data view
st.subheader("Parcel Assessment Records")
st.dataframe(gdf[['parcel_id', 'plot_size_m2', 'dist_to_urban_km', 'predicted_value', 'calculated_tax']])