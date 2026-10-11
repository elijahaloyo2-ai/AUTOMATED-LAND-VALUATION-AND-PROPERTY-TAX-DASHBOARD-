import streamlit as st
import geopandas as gpd
import pandas as pd
import folium
from streamlit_folium import st_folium
import joblib

# Page configuration
st.set_page_config(page_title="County CAMA & Property Tax Dashboard", layout="wide")

st.title("Automated Land Valuation & Property Tax Dashboard")
st.markdown("Computer-Assisted Mass Appraisal (CAMA) prototype for optimizing county land revenue collection.")

# Load model and data
@st.cache_resource
def load_resources():
    model = joblib.load("model/valuation_model.pkl")
    gdf = gpd.read_file("data/parcels.geojson")
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
