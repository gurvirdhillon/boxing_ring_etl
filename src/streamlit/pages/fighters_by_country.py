import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.title("Fighter Performance Heatmap")

# Load fighter stats (replace with whatever table you're using)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.normpath(os.path.join(BASE_DIR, "../../../data/processed/final_processed_data/boxing-match-fighters.csv"))

df = pd.read_csv(CSV_PATH)

countries_A = df.rename(columns={"Country_A": "Country"})["Country"]
countries_B = df.rename(columns={"Country_B": "Country"})["Country"]

all_countries = pd.concat([countries_A, countries_B], ignore_index=True)
all_countries = all_countries.dropna()

# Count fighters per country
country_counts = all_countries.value_counts().reset_index()
country_counts.columns = ["Country", "Count"]

# -----------------------------------------
# Plotly Choropleth Map
# -----------------------------------------
fig = px.choropleth(
    country_counts,
    locations="Country",             # name of the column
    locationmode="country names",     # using actual country names
    color="Count",                    # color scale based on # fighters
    hover_name="Country",
    color_continuous_scale="Reds",
    title="World Map of Number of Fighters by Country"
)

fig.update_layout(
    geo=dict(showframe=False, showcoastlines=True, projection_type="natural earth")
)

# Display in Streamlit
st.plotly_chart(fig, use_container_width=True)