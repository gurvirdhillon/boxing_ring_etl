import streamlit as st
import pandas as pd

st.title("hello streamlit")

df = pd.read_csv('../../data/processed/final_processed_data/boxing-match-fighters.csv')

st.write(df)
