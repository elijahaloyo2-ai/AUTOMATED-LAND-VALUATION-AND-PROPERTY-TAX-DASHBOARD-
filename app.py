import os
import tempfile
import joblib
import streamlit as st
import geopandas as gpd
import pandas as pd
import folium
from streamlit_folium import st_folium
from sklearn.ensemble import RandomForestRegressor
from shapely.geometry import Polygon, mapping
import json

# Page configuration
st.set_page_config(page_title="County CAMA & Property Tax Dashboard", layout="wide")

st.title("Automated Land Valuation & Property Tax Dashboard")
st.markdown("Computer-Assisted Mass Appraisal (CAMA) prototype for optimizing county land revenue collection.")

# Load or auto-train the default valuation model
@st.cache_resource
def load_model():
    os.makedirs("model", exist_ok=True)
    model_path = "model/valuation_model.pkl"
    
    if os.path.exists(model_path):
        return joblib.load(model_path)
    else:
        base_coords = [(34.45, -0.95), (34.46, -0.95), (34.46, -0.96), (34.45, -0.96), (34.45, -0.95)]
        features = []
        for i in range(1, 11):
            offset = (i % 3) * 0.01
            shift = (i // 3) * 0.01
            poly_coords = [(lng + offset, lat - shift) for lng, lat in base_coords]
            features.append({
                "type": "Feature",
                "geometry": mapping(Polygon(poly_coords)),
                "properties": {
                    "parcel_id": f"PRC-10{i}",
                    "plot_size_m2": round(500 + (i * 120.5), 2),
                    "dist_to_urban_km": round(1.2 + (i * 0.4), 1),
                    "road_access_score": (i % 5) + 1,
                    "market_value": round(15000 + (i * 4200.0), 2)
                }
            })
        default_gdf = gpd.GeoDataFrame.from_features(features, crs="EPSG:4326")
        X = default_gdf[['plot_size_m2', 'dist_to_urban_km', 'road_access_score']]
        y = default_gdf['market_value']
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X, y)
        joblib.dump(model, model_path)
        return model

model = load_model()

# Sidebar Controls for File Upload and Tax Policy
st.sidebar.header("Data Input")
uploaded_file = st.sidebar.file_uploader("Upload Parcel GeoJSON File", type=["geojson", "json"])

st.sidebar.header("Tax Policy Settings")
tax_rate = st.sidebar.slider("Annual Property Tax Rate (%)", min_value=0.1, max_value=3.0, value=1.0, step=0.1)

# Load GeoJSON data (from uploaded file or fallback default sample)
def load_data(uploaded_file):
    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".geojson") as tmp:
            tmp.write(uploaded_file.getvalue())
            tmp_path = tmp.name
        gdf = gpd.read_file(tmp_path)
        os.unlink(tmp_path)
        st.sidebar.success("Custom GeoJSON loaded successfully!")
        return gdf
    else:
        st.sidebar.info("Using default sample parcels. Upload your GeoJSON above to test custom data.")
        base_coords = [(34.45, -0.95), (34.46, -0.95), (34.46, -0.96), (34.45, -0.96), (34.45, -0.95)]
        features = []
        for i in range(1, 11):
            offset = (i % 3) * 0.01
            shift = (i // 3) * 0.01
            poly_coords = [(lng + offset, lat - shift) for lng, lat in base_coords]
            features.append({
                "type": "Feature",
                "geometry": mapping(Polygon(poly_coords)),
                "properties": {
                    "parcel_id": f"PRC-10{i}",
                    "plot_size_m2": round(500 + (i * 120.5), 2),
                    "dist_to_urban_km": round(1.2 + (i * 0.4), 1),
                    "road_access_score": (i % 5) + 1,
                    "market_value": round(15000 + (i * 4200.0), 2)
                }
            })
        return gpd.GeoDataFrame.from_features(features, crs="EPSG:4326")

gdf = load_data(uploaded_file)

# Ensure required feature columns exist before prediction
required_cols = ['plot_size_m2', 'dist_to_urban_km', 'road_access_score']
missing_cols = [col for col in required_cols if col not in gdf.columns]

if missing_cols:
    st.error(f"Uploaded GeoJSON is missing required property columns: {missing_cols}. Please ensure your file includes: {required_cols}")
else:
    # Predict property values
    features = gdf[required_cols]
    gdf['predicted_value'] = model.predict(features)
    gdf['calculated_tax'] = gdf['predicted_value'] * (tax_rate / 100)

    # Summary metrics
    total_valuation = gdf['predicted_value'].sum()
    total_potential_revenue = gdf['calculated_tax'].sum()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Parcels Assessed", len(gdf))
    col2.metric("Total Estimated Land Value", f"${total_valuation:,.2f}")
    col3.metric("Projected Annual Revenue", f"${total_potential_revenue:,.2f}")

    # Create Folium Map centered on data centroid
    centroid = gdf.unary_union.centroid
    m = folium.Map(location=[centroid.y, centroid.x], zoom_start=13, tiles="CartoDB positron")

    # Add GeoJson layer
    folium.GeoJson(
        gdf,
        name="Land Parcels",
        style_function=lambda feature: {
            'fillColor': '#3186cc' if feature['properties'].get('road_access_score', 3) > 2 else '#ff7f0e',
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

    # Render map
    st.subheader("Interactive Parcel Valuation Map")
    st_data = st_folium(m, width=1100, height=550)

    # Detailed data view
    st.subheader("Parcel Assessment Records")
    display_cols = [c for c in ['parcel_id', 'plot_size_m2', 'dist_to_urban_km', 'predicted_value', 'calculated_tax'] if c in gdf.columns]
    st.dataframe(gdf[display_cols])
