# Automated Land Valuation & Property Tax Dashboard 🗺️📊

Welcome! This repository contains a Computer-Assisted Mass Appraisal (CAMA) prototype that I built to solve a very practical problem: making land valuation and property tax estimation faster, fairer, and more transparent for local governments and urban planning agencies.

By combining **Geoinformatics** with **Data Science**, this tool moves away from manual, time-consuming appraisal spreadsheets. Instead, it uses spatial machine learning to predict property values and provides an interactive dashboard where policy decisions and tax adjustments can be visualized in real-time.

---

## 💡 Why I Built This

During my studies in Geoinformatics, I noticed that one of the biggest bottlenecks in local government administration—especially when optimizing revenue for county governments—is keeping land valuation rolls up to date. Manual appraisals often lag behind real market growth, leading to uneven taxation and lost public revenue.

I wanted to see how machine learning could take location data (like proximity to roads, town centers, and utility access) and automatically generate reliable valuation baselines. This project is my proof-of-concept for how digital tools can help modernize land administration.

---

## ✨ Key Features

* **Smart Valuation Engine:** Uses a trained Machine Learning model (Random Forest / Gradient Boosting) to estimate land values based on location, parcel size, and spatial features.
* **Interactive Map Interface:** A user-friendly map showing property boundaries, color-coded by value tiers and predicted property rates.
* **Live Tax Revenue Simulator:** Allows revenue officers or policy analysts to adjust tax percentages on the fly and immediately see projected county revenue changes.
* **Click-and-Inspect Details:** Users can click on any specific parcel to view its geometric properties, proximity metrics, and estimated valuation breakdown.

---

## 🧰 Tech Stack & Tools

* **Language:** Python 3.9+
* **Spatial & Data Handling:** `GeoPandas`, `Pandas`, `Shapely`
* **Machine Learning:** `Scikit-Learn`
* **Mapping & Visualizations:** `Folium`, `Streamlit-Folium`, `Plotly`
* **Dashboard Framework:** `Streamlit`

---

## 📂 Project Structure

```
land-valuation-dashboard/
│
├── data/
│   ├── raw/                  # Initial spatial data & sample GeoJSON parcels
│   └── processed/            # Cleaned spatial datasets ready for modeling
│
├── models/
│   └── valuation_model.pkl   # Saved machine learning model
│
├── src/
│   ├── data_preprocessing.py # Spatial cleaning & coordinate transformation
│   ├── feature_engineering.py# Distance and proximity calculations
│   └── train_model.py        # Model training script
│
├── app.py                    # Streamlit web application script
├── requirements.txt          # Required Python packages
└── README.md                 # Project documentation
```

---

## 🚀 Quickstart & Running Locally

Want to test the app on your local machine? Here is how to get set up:

1. **Clone this repository:**
   ```bash
   git clone https://github.com/your-username/land-valuation-dashboard.git
   cd land-valuation-dashboard
   ```

2. **Set up a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, run: venv\Scripts\activate
   ```

3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Launch the dashboard:**
   ```bash
   streamlit run app.py
   ```

---

## 📐 How It Works (The Methodology)

1. **Spatial Data Extraction:** Loads vector data (GeoJSON/Shapefiles) and calculates geometric properties like parcel size and location coordinates.
2. **Proximity Feature Engineering:** Calculates spatial relationships, such as how far each plot is from major roads, town centers, or public facilities.
3. **Model Training & Evaluation:** Trains a regression model on these spatial features to predict land prices, evaluating performance using $R^2$ and RMSE scores.
4. **Dashboard Integration:** Wraps everything into an intuitive Streamlit interface where users can query data and run scenario simulations.

---

## 🌍 Real-World Impact

* **For County Revenue Teams:** Helps create data-driven, fair, and consistent property valuation rolls.
* **For Urban Planners:** Highlights high-value expansion zones and helps plan where public infrastructure is needed most.
* **For Citizens:** Promotes transparency in property rate calculations and tax assessments.

---

## 👨‍💻 Author

**Elijah Aloyo**  
*BSc Geoinformatics | Geospatial Data Scientist & Developer*  

* 📧 Email: aloyoelija23@gmail.com
* 💼 [LinkedIn](https://linkedin.com/in/your-profile)
* 🐙 [GitHub](https://github.com/elijahaloyo2)
