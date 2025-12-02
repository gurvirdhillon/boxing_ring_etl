import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.title("Fighter Performance Heatmap")

# Load fighter stats (replace with whatever table you're using)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.normpath(os.path.join(BASE_DIR, "../../../data/processed/final_processed_data/boxing-match-fighters.csv"))

df = pd.read_csv(CSV_PATH)

tableau_graph = "https://public.tableau.com/views/BoxerInformation/Sheet1?:showVizHome=no&:embed=true"
st.components.v1.iframe(tableau_graph, width=1800, height=900)
